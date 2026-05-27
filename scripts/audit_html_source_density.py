#!/usr/bin/env python3
"""Audit fixed-page HTML source files for dense card stacks before PDF export."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "content-elevated-product-os" / "exports"
BATCHES = {
    "phase-1": EXPORTS / "phase-1-payhip-source-package",
    "next": EXPORTS / "next-batch-source-package",
    "standard": EXPORTS / "standard-queue-source-package",
}

SECTION_RE = re.compile(r'<section class="[^"]*\bpage\b[^"]*">.*?</section>', re.S)
CARD_RE = re.compile(r'<article class="(?:asset-card|data-card)">.*?</article>', re.S)
FOOTER_RE = re.compile(r'<div class="footer"><span>.*?</span><span>(\d+)</span></div>', re.S)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Content Elevated HTML source density.")
    parser.add_argument("--batch", choices=["all", *BATCHES.keys()], default="all")
    parser.add_argument("--max-cards", type=int, default=4)
    parser.add_argument("--only", nargs="*", default=[])
    return parser.parse_args()


def selected_batches(key: str) -> list[str]:
    return list(BATCHES) if key == "all" else [key]


def page_label(section: str, fallback: int) -> str:
    match = FOOTER_RE.search(section)
    return match.group(1) if match else f"{fallback:02d}"


def main() -> None:
    args = parse_args()
    only = set(args.only)
    rows: list[tuple[str, str, str, str, int]] = []

    for batch_key in selected_batches(args.batch):
        source_root = BATCHES[batch_key]
        if not source_root.exists():
            continue
        for product in sorted(path for path in source_root.iterdir() if path.is_dir()):
            if only and product.name not in only:
                continue
            html_dir = product / "html"
            if not html_dir.exists():
                continue
            for html_path in sorted(html_dir.glob("*.html")):
                text = html_path.read_text(encoding="utf-8", errors="ignore")
                for index, section in enumerate(SECTION_RE.findall(text), start=1):
                    card_count = len(CARD_RE.findall(section))
                    if card_count > args.max_cards:
                        rows.append(
                            (
                                batch_key,
                                product.name,
                                html_path.name,
                                page_label(section, index),
                                card_count,
                            )
                        )

    report_path = EXPORTS / "HTML_SOURCE_DENSITY_REPORT.md"
    lines = [
        "# HTML Source Density Report",
        "",
        f"Max allowed stacked cards per fixed page: {args.max_cards}",
        f"Files/pages needing attention: {len(rows)}",
        "",
        "| Batch | Product | HTML | Page | Cards |",
        "|---|---|---|---:|---:|",
    ]
    for batch, product, html_name, page, card_count in rows:
        lines.append(f"| {batch} | {product} | `{html_name}` | {page} | {card_count} |")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(report_path)
    print(f"Files/pages needing attention: {len(rows)}")
    if rows:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
