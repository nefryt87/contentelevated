#!/usr/bin/env python3
"""Build a sales-launch upload command sheet from packaged source files."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OS_ROOT = ROOT / "content-elevated-product-os"
EXPORTS = OS_ROOT / "exports"
GLOBAL = OS_ROOT / "internal" / "_global"
PRODUCT_MASTER = OS_ROOT / "data" / "product-master.json"


BATCHES = [
    {
        "key": "phase-1",
        "title": "Phase 1 Launch Batch",
        "package": EXPORTS / "phase-1-payhip-source-package",
        "handoff": GLOBAL / "phase-1-website-copy-handoff.json",
        "priority": "Upload first",
    },
    {
        "key": "next",
        "title": "Next Approved Batch",
        "package": EXPORTS / "next-batch-source-package",
        "handoff": GLOBAL / "next-batch-website-copy-handoff.json",
        "priority": "Upload after Phase 1",
    },
    {
        "key": "standard",
        "title": "Standard Queue",
        "package": EXPORTS / "standard-queue-source-package",
        "handoff": GLOBAL / "standard-queue-website-copy-handoff.json",
        "priority": "Upload after visual proof and missing URLs/covers",
    },
]


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_pdf_names(manifest_path: Path) -> list[str]:
    if not manifest_path.exists():
        return []
    text = manifest_path.read_text(encoding="utf-8")
    names: list[str] = []
    for match in re.finditer(r"-> `([^`]+\.pdf)`", text):
        names.append(match.group(1))
    return names


def spreadsheet_names(product_package: Path) -> list[str]:
    sheet_dir = product_package / "spreadsheets"
    if not sheet_dir.exists():
        return []
    return [path.name for path in sorted(sheet_dir.glob("*.xlsx"))]


def html_count(product_package: Path) -> int:
    return len(list((product_package / "html").glob("*.html"))) if (product_package / "html").exists() else 0


def product_lookup() -> dict[str, dict]:
    return {item["slug"]: item for item in load_json(PRODUCT_MASTER)}


def handoff_lookup(path: Path) -> dict[str, dict]:
    return {item["internal_slug"]: item for item in load_json(path)}


def checkbox(value: str | None) -> str:
    return value if value else "confirm"


def build_batch_section(batch: dict, products: dict[str, dict]) -> list[str]:
    package_root: Path = batch["package"]
    handoff = handoff_lookup(batch["handoff"])
    lines = [
        f"## {batch['title']}",
        "",
        f"Priority: {batch['priority']}",
        f"Source package: `{package_root.relative_to(ROOT)}`",
        "",
        "| Product | Payhip URL | Price | PDFs | Sheets | Missing Before Upload |",
        "|---|---|---|---:|---:|---|",
    ]

    product_dirs = [
        path
        for path in sorted(package_root.iterdir())
        if path.is_dir() and ((path / "html").exists() or (path / "spreadsheets").exists())
    ] if package_root.exists() else []

    for product_dir in product_dirs:
        slug = product_dir.name
        master = products.get(slug, {})
        handoff_item = handoff.get(slug, {})
        title = (
            master.get("product_name")
            or handoff_item.get("website_title")
            or handoff_item.get("h1")
            or slug
        )
        url = master.get("payhip_url") or handoff_item.get("payhip_url") or ""
        price = master.get("price") or ""
        pdfs = manifest_pdf_names(product_dir / "MANIFEST.md")
        if not pdfs:
            pdfs = [path.with_suffix(".pdf").name for path in sorted((product_dir / "html").glob("*.html"))]
        sheets = spreadsheet_names(product_dir)
        missing = []
        if not url:
            missing.append("Payhip URL")
        if not price:
            missing.append("price")
        missing.append("cover image")
        lines.append(
            f"| {title} | {checkbox(url)} | {checkbox(price)} | {len(pdfs)} | {len(sheets)} | {', '.join(missing)} |"
        )

    lines += ["", "### File-Level Upload List", ""]

    for product_dir in product_dirs:
        slug = product_dir.name
        master = products.get(slug, {})
        title = master.get("product_name") or slug
        pdfs = manifest_pdf_names(product_dir / "MANIFEST.md")
        if not pdfs:
            pdfs = [path.with_suffix(".pdf").name for path in sorted((product_dir / "html").glob("*.html"))]
        sheets = spreadsheet_names(product_dir)
        lines += [
            f"#### {title}",
            "",
            "Upload after external PDF export from:",
            f"`content-elevated-product-os/exports/customer-pdf-export/{batch['key']}/{slug}/`",
            "",
            "PDFs:",
        ]
        lines.extend([f"- `pdfs/{name}`" for name in pdfs] or ["- None"])
        lines += ["", "Spreadsheets:"]
        lines.extend([f"- `spreadsheets/{name}`" for name in sheets] or ["- None"])
        lines.append("")

    return lines


def main() -> None:
    products = product_lookup()
    lines = [
        "# Content Elevated Upload Execution Command Sheet",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Use this after running the external PDF exporter. It keeps Payhip upload execution focused and prevents internal files from being uploaded.",
        "",
        "External PDF export output:",
        "",
        "`content-elevated-product-os/exports/customer-pdf-export/`",
        "",
        "Never upload source HTML, manifests, internal notes, listing CSVs, or production planning docs to Payhip.",
        "",
    ]

    for batch in BATCHES:
        lines.extend(build_batch_section(batch, products))

    output = GLOBAL / "upload-execution-command-sheet.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
