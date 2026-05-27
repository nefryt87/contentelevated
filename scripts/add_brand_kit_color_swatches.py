#!/usr/bin/env python3
"""Add visual color swatches to Brand Kit palette cards."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "content-elevated-product-os" / "exports"
SOURCE_PACKAGES = [
    ROOT / "rebranded-products-sample-direction",
    EXPORTS / "phase-1-payhip-source-package",
    EXPORTS / "next-batch-source-package",
    EXPORTS / "standard-queue-source-package",
]

HEX_HEADING_RE = re.compile(
    r"<h3(?![^>]*\bswatch-heading\b)([^>]*)>\s*(#[0-9a-fA-F]{6})\s*</h3>"
)

SWATCH_CSS = """

    .swatch-heading {
      display: flex;
      align-items: center;
      gap: 0.12in;
      min-width: 0;
    }

    .color-swatch {
      width: 0.34in;
      height: 0.34in;
      flex: 0 0 0.34in;
      border-radius: 999px;
      background: var(--swatch);
      border: 1px solid rgba(15, 23, 42, 0.14);
      box-shadow:
        inset 0 0 0 1px rgba(255, 255, 255, 0.46),
        0 0.08in 0.22in rgba(15, 23, 42, 0.10);
    }

    .deep-page .color-swatch,
    .highlight-page .color-swatch,
    .feature-page .color-swatch,
    .private-page .color-swatch {
      border-color: rgba(255, 255, 255, 0.32);
      box-shadow:
        inset 0 0 0 1px rgba(255, 255, 255, 0.24),
        0 0.08in 0.22in rgba(0, 0, 0, 0.22);
    }
"""


def brand_kit_files() -> list[Path]:
    files: list[Path] = []
    for package in SOURCE_PACKAGES:
        if not package.exists():
            continue
        files.extend(sorted(package.glob("*/*brand-kit*.html")))
        files.extend(sorted(package.glob("*/*Brand_Kit*.html")))
        files.extend(sorted(package.glob("*/salon-brand-kit.html")))
        files.extend(sorted(package.glob("*/html/*brand-kit*.html")))
        files.extend(sorted(package.glob("*/html/*Brand_Kit*.html")))
        files.extend(sorted(package.glob("*/html/salon-brand-kit.html")))
    return sorted(set(files))


def add_css(text: str) -> str:
    if ".color-swatch" in text:
        return text
    if "</style>" not in text:
        return text
    return text.replace("</style>", f"{SWATCH_CSS}\n  </style>", 1)


def replace_heading(match: re.Match[str]) -> str:
    attrs = match.group(1)
    original_hex = match.group(2)
    display_hex = original_hex.upper()
    return (
        f'<h3 class="swatch-heading"{attrs}>'
        f'<span class="color-swatch" style="--swatch: {display_hex};"></span>'
        f"<span>{display_hex}</span>"
        "</h3>"
    )


def main() -> None:
    changed: list[tuple[Path, int]] = []
    for path in brand_kit_files():
        original = path.read_text(encoding="utf-8", errors="ignore")
        text = add_css(original)
        text, count = HEX_HEADING_RE.subn(replace_heading, text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append((path, count))

    print(f"Brand Kit files scanned: {len(brand_kit_files())}")
    print(f"Brand Kit files changed: {len(changed)}")
    print(f"Swatch headings added: {sum(count for _, count in changed)}")
    for path, count in changed:
        rel = path.relative_to(ROOT)
        print(f"- {rel} ({count})")


if __name__ == "__main__":
    main()
