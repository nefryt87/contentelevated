#!/usr/bin/env python3
"""Package Phase 1 buyer-facing HTML sources and spreadsheets for Payhip prep."""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
SOURCE_ROOT = ROOT / "rebranded-products-sample-direction"
PACKAGE_ROOT = ROOT / "content-elevated-product-os/exports/phase-1-payhip-source-package"

PHASE_1_SLUGS = [
    "hair-stylists",
    "med-spas",
    "dentists",
    "nutritionists",
    "hvac-contractors",
    "accountants-and-cpas",
    "wedding-photographers",
    "etsy-sellers",
]


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    products = {item["slug"]: item for item in inventory}

    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    PACKAGE_ROOT.mkdir(parents=True)

    summary = [
        "# Phase 1 Payhip Source Package",
        "",
        f"Packaged: {date.today().isoformat()}",
        "",
        "This folder contains the approved buyer-facing source files for the first launch batch.",
        "Use these HTML files as the source for final PDF export, then upload the generated PDFs plus any spreadsheets to Payhip.",
        "",
        "## PDF Export Note",
        "",
        "Automated PDF export was attempted locally, but the available headless browser tools are blocked in this desktop environment. The HTML sources are preserved here so final PDF export can be run through Chrome/print-to-PDF, a browser automation environment with Playwright browsers installed, or a design/export tool.",
        "",
    ]

    for slug in PHASE_1_SLUGS:
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
            pdf_name = target.with_suffix(".pdf").name
            manifest.append(
                f"- `html/{target.name}` -> `{pdf_name}` — {file_info.get('pages')} pages; {file_info.get('prompts')} prompts detected; {file_info.get('templates')} templates/scripts/systems estimated"
            )

        if copied_sheets:
            manifest += ["", "## Upload These Spreadsheets Too", ""]
            for sheet in copied_sheets:
                manifest.append(f"- `spreadsheets/{sheet.name}`")

        manifest += [
            "",
            "## Do Not Upload",
            "",
            "- Internal planning files",
            "- Product workspace files",
            "- Any `v2/` draft files unless they are separately approved",
            "",
        ]
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
