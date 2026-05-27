#!/usr/bin/env python3
"""Split overloaded fixed-page HTML sections into safer PDF pages.

Content Elevated print-ready PDFs use fixed 8.5x11in pages. When a section has
too many stacked `.asset-card` or `.data-card` blocks, Chrome can visually clip or overlay the
bottom cards even when page-count validation passes. This script splits dense
sections into multiple same-style pages and renumbers page footers.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = [
    ROOT / "content-elevated-product-os" / "exports" / "phase-1-payhip-source-package",
    ROOT / "content-elevated-product-os" / "exports" / "next-batch-source-package",
    ROOT / "content-elevated-product-os" / "exports" / "standard-queue-source-package",
    ROOT / "rebranded-products-sample-direction",
    ROOT / "rebranded-products-full-rebrand",
    ROOT / "rebranded-products",
    ROOT / "print-ready-pdfs",
]

SECTION_RE = re.compile(r'<section class="[^"]*\bpage\b[^"]*">.*?</section>', re.S)
CARD_RE = re.compile(r'<article class="(?:asset-card|data-card)">.*?</article>', re.S)
FOOTER_RE = re.compile(r'(<div class="footer"><span>.*?</span><span>)(\d+)(</span></div>)', re.S)
MANIFEST_RE = re.compile(
    r"(`html/([^`]+)\.html`(?: -> `[^`]+\.pdf`)? — )(\d+)( pages)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Split dense PDF HTML card stacks.")
    parser.add_argument(
        "--target",
        nargs="*",
        type=Path,
        default=DEFAULT_TARGETS,
        help="Root folders to scan. Defaults to active Content Elevated source folders.",
    )
    parser.add_argument(
        "--max-cards",
        type=int,
        default=4,
        help="Maximum stacked asset cards per fixed PDF page. Default: 4.",
    )
    parser.add_argument(
        "--pattern",
        default="*.html",
        help="HTML filename glob to scan. Default: *.html.",
    )
    return parser.parse_args()


def split_sections(text: str, max_cards: int) -> tuple[str, bool, list[int]]:
    changed = False
    split_groups: list[int] = []

    def replace_section(match: re.Match[str]) -> str:
        nonlocal changed
        section = match.group(0)
        stack_marker = '<div class="content-stack">'
        stack_start = section.find(stack_marker)
        footer_start = section.rfind('<div class="footer"')
        if stack_start == -1 or footer_start == -1:
            return section

        cards = CARD_RE.findall(section[stack_start:footer_start])
        if len(cards) <= max_cards:
            return section

        before_stack = section[:stack_start]
        footer_and_close = section[footer_start:]
        chunks = [cards[index : index + max_cards] for index in range(0, len(cards), max_cards)]
        rebuilt = []
        for chunk in chunks:
            rebuilt.append(
                before_stack
                + stack_marker
                + "\n"
                + "\n\n    ".join(chunk)
                + "</div>\n  "
                + footer_and_close
            )
        changed = True
        split_groups.append(len(cards))
        return "\n".join(rebuilt)

    new_text = SECTION_RE.sub(replace_section, text)
    if not changed:
        return text, False, []

    counter = 0

    def renumber_footer(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        return f"{match.group(1)}{counter:02d}{match.group(3)}"

    return FOOTER_RE.sub(renumber_footer, new_text), True, split_groups


def update_manifest(html_path: Path, page_count: int) -> None:
    if html_path.parent.name != "html":
        return
    manifest = html_path.parents[1] / "MANIFEST.md"
    if not manifest.exists():
        return

    stem = html_path.stem
    text = manifest.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        if match.group(2) == stem:
            return f"{match.group(1)}{page_count}{match.group(4)}"
        return match.group(0)

    manifest.write_text(MANIFEST_RE.sub(replace, text), encoding="utf-8")


def main() -> None:
    args = parse_args()
    changed_files: list[str] = []

    for root in args.target:
        root = root.expanduser().resolve()
        if not root.exists():
            continue
        for html_path in sorted(root.rglob(args.pattern)):
            if any(part.startswith("_") for part in html_path.relative_to(root).parts):
                continue
            text = html_path.read_text(encoding="utf-8", errors="ignore")
            new_text, changed, groups = split_sections(text, args.max_cards)
            if not changed:
                continue
            html_path.write_text(new_text, encoding="utf-8")
            page_count = len(SECTION_RE.findall(new_text))
            update_manifest(html_path, page_count)
            try:
                label = html_path.relative_to(ROOT)
            except ValueError:
                label = html_path
            changed_files.append(f"{label} -> {page_count} pages; split {groups}")

    print(f"Changed files: {len(changed_files)}")
    for item in changed_files:
        print(f"- {item}")


if __name__ == "__main__":
    main()
