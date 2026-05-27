#!/usr/bin/env python3
"""Package the recommended next batch of buyer-facing HTML sources."""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
SOURCE_ROOT = ROOT / "rebranded-products-sample-direction"
PACKAGE_ROOT = ROOT / "content-elevated-product-os/exports/next-batch-source-package"

NEXT_BATCH = [
    "barbers",
    "dog-walkers-and-pet-sitters",
    "personal-trainers",
    "personal-chefs",
    "nannies-and-childcare-professionals",
    "florists",
    "event-planners",
    "videographers",
    "public-speakers",
    "personal-stylists",
    "life-and-business-coaches",
]


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    products = {item["slug"]: item for item in json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))}

    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    PACKAGE_ROOT.mkdir(parents=True)

    summary = [
        "# Next Batch Source Package",
        "",
        f"Packaged: {date.today().isoformat()}",
        "",
        "This package contains buyer-facing HTML sources for the recommended next batch after Phase 1.",
        "",
    ]

    for slug in NEXT_BATCH:
        product = products[slug]
        source_dir = SOURCE_ROOT / slug
        product_dir = PACKAGE_ROOT / slug
        html_dir = product_dir / "html"
        sheet_dir = product_dir / "spreadsheets"

        copied_html = []
        for file_info in product["files"]:
            if file_info.get("internal"):
                continue
            source = source_dir / file_info["file"]
            target = html_dir / source.name
            copy_file(source, target)
            copied_html.append((file_info, target))

        copied_sheets = []
        spreadsheet_source = source_dir / "spreadsheets"
        if spreadsheet_source.exists():
            for sheet in sorted(spreadsheet_source.glob("*.xlsx")):
                target = sheet_dir / sheet.name
                copy_file(sheet, target)
                copied_sheets.append(target)

        manifest = [
            f"# {product['product_name']}",
            "",
            f"Packaged: {date.today().isoformat()}",
            "",
            "## Convert These HTML Files To PDF",
            "",
        ]
        for file_info, target in copied_html:
            manifest.append(f"- `html/{target.name}` — {file_info.get('pages')} pages")
        if copied_sheets:
            manifest += ["", "## Upload These Spreadsheets Too", ""]
            manifest.extend(f"- `spreadsheets/{sheet.name}`" for sheet in copied_sheets)
        manifest.append("")
        (product_dir / "MANIFEST.md").write_text("\n".join(manifest), encoding="utf-8")

        summary += [
            f"## {product['product_name']}",
            "",
            f"- HTML files packaged: {len(copied_html)}",
            f"- Spreadsheets packaged: {len(copied_sheets)}",
            f"- Customer-facing pages from inventory: {product['total_customer_pages']}",
            f"- Folder: `{product_dir.relative_to(ROOT)}`",
            "",
        ]

    (PACKAGE_ROOT / "README.md").write_text("\n".join(summary), encoding="utf-8")
    print(PACKAGE_ROOT)


if __name__ == "__main__":
    main()
