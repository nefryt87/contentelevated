#!/usr/bin/env python3
"""Export Phase 1 Content Elevated HTML products into Payhip-ready PDFs."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
SOURCE_ROOT = ROOT / "rebranded-products-sample-direction"
EXPORT_ROOT = ROOT / "content-elevated-product-os/exports/phase-1-payhip-upload"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

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


def safe_pdf_name(html_file: str) -> str:
    return Path(html_file).with_suffix(".pdf").name


def run_chrome_export(html_path: Path, pdf_path: Path, user_data_dir: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-dev-shm-usage",
        f"--user-data-dir={user_data_dir}",
        "--virtual-time-budget=1200",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def maybe_pdf_page_count(pdf_path: Path) -> int | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except Exception:
            return None

    try:
        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        return None


def write_product_manifest(product_dir: Path, product: dict, exported: list[dict], copied_sheets: list[Path]) -> None:
    lines = [
        f"# {product['product_name']} Upload Files",
        "",
        f"Exported: {date.today().isoformat()}",
        "",
        "## PDFs",
        "",
    ]

    for item in exported:
        page_note = f"exported pages: {item['exported_pages']}" if item["exported_pages"] is not None else "exported pages: not verified"
        lines.append(f"- `pdfs/{item['pdf']}` — source `{item['source']}`; inventory pages: {item['inventory_pages']}; {page_note}")

    if copied_sheets:
        lines += ["", "## Spreadsheets", ""]
        for sheet in copied_sheets:
            lines.append(f"- `spreadsheets/{sheet.name}`")

    lines += [
        "",
        "## Payhip Upload Note",
        "",
        "Upload the PDFs and spreadsheets above as the replacement customer files for this bundle. Keep internal planning files out of Payhip.",
        "",
    ]
    (product_dir / "MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not CHROME.exists():
        raise SystemExit(f"Chrome was not found at {CHROME}")

    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    products = {item["slug"]: item for item in inventory}
    missing = [slug for slug in PHASE_1_SLUGS if slug not in products]
    if missing:
        raise SystemExit(f"Missing Phase 1 products from inventory: {', '.join(missing)}")

    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    summary: list[str] = [
        "# Phase 1 Payhip Export Summary",
        "",
        f"Exported: {date.today().isoformat()}",
        "",
        "This folder contains customer-facing PDFs and spreadsheets for the first launch batch.",
        "",
    ]

    with tempfile.TemporaryDirectory(prefix="ce-chrome-export-") as tmp:
        user_data_dir = Path(tmp) / "chrome-profile"
        for slug in PHASE_1_SLUGS:
            product = products[slug]
            source_dir = SOURCE_ROOT / slug
            product_dir = EXPORT_ROOT / slug
            pdf_dir = product_dir / "pdfs"
            sheet_dir = product_dir / "spreadsheets"
            product_dir.mkdir(parents=True, exist_ok=True)
            pdf_dir.mkdir(parents=True, exist_ok=True)

            exported: list[dict] = []
            for file_info in product["files"]:
                if file_info.get("internal"):
                    continue
                html_path = source_dir / file_info["file"]
                if not html_path.exists():
                    raise SystemExit(f"Missing source file: {html_path}")
                pdf_name = safe_pdf_name(file_info["file"])
                pdf_path = pdf_dir / pdf_name
                run_chrome_export(html_path, pdf_path, user_data_dir)
                exported.append(
                    {
                        "source": file_info["file"],
                        "pdf": pdf_name,
                        "inventory_pages": file_info.get("pages"),
                        "exported_pages": maybe_pdf_page_count(pdf_path),
                        "bytes": pdf_path.stat().st_size,
                    }
                )

            copied_sheets: list[Path] = []
            spreadsheet_source = source_dir / "spreadsheets"
            if spreadsheet_source.exists():
                sheet_dir.mkdir(parents=True, exist_ok=True)
                for sheet in sorted(spreadsheet_source.glob("*.xlsx")):
                    target = sheet_dir / sheet.name
                    shutil.copy2(sheet, target)
                    copied_sheets.append(target)

            write_product_manifest(product_dir, product, exported, copied_sheets)

            verified = sum(1 for item in exported if item["exported_pages"] is not None)
            summary += [
                f"## {product['product_name']}",
                "",
                f"- PDFs exported: {len(exported)}",
                f"- PDFs with page counts verified: {verified}",
                f"- Spreadsheets copied: {len(copied_sheets)}",
                f"- Folder: `{product_dir.relative_to(ROOT)}`",
                "",
            ]

    (EXPORT_ROOT / "EXPORT_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    print(f"Export complete: {EXPORT_ROOT}")


if __name__ == "__main__":
    main()
