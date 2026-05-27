#!/usr/bin/env python3
"""Validate exported Content Elevated customer PDFs against source manifests."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "content-elevated-product-os" / "exports"
DEFAULT_OUTPUT = EXPORTS / "customer-pdf-export"

BATCHES = {
    "phase-1": EXPORTS / "phase-1-payhip-source-package",
    "next": EXPORTS / "next-batch-source-package",
    "standard": EXPORTS / "standard-queue-source-package",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate exported customer PDFs.")
    parser.add_argument(
        "--batch",
        choices=["all", *BATCHES.keys()],
        default="phase-1",
        help="Which batch to validate. Default: phase-1.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Export output folder created by export_customer_pdfs_outside_codex.py.",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        default=[],
        help="Optional product folder slugs to validate.",
    )
    parser.add_argument(
        "--files-per-product",
        type=int,
        default=0,
        help="Demo mode: validate only the first N expected PDFs per product.",
    )
    parser.add_argument(
        "--pdf-pattern",
        nargs="*",
        default=[],
        help="Optional glob pattern(s) for expected PDFs, such as '04-brand-kit*.pdf'.",
    )
    return parser.parse_args()


def expected_pdfs(product_source: Path) -> list[str]:
    manifest = product_source / "MANIFEST.md"
    if manifest.exists():
        text = manifest.read_text(encoding="utf-8")
        names = re.findall(r"-> `([^`]+\.pdf)`", text)
        if names:
            return names
    html_dir = product_source / "html"
    if not html_dir.exists():
        return []
    return [path.with_suffix(".pdf").name for path in sorted(html_dir.glob("*.html"))]


def expected_sheets(product_source: Path) -> list[str]:
    sheet_dir = product_source / "spreadsheets"
    if not sheet_dir.exists():
        return []
    return [path.name for path in sorted(sheet_dir.glob("*.xlsx"))]


def pdf_pages(pdf_path: Path) -> int | None:
    try:
        data = pdf_path.read_bytes()
    except OSError:
        return None
    matches = re.findall(rb"/Type\s*/Page\b", data)
    return len(matches) if matches else None


def selected_batches(key: str) -> list[str]:
    if key == "all":
        return list(BATCHES)
    return [key]


def validate_batch(
    batch_key: str,
    output_root: Path,
    only: set[str],
    files_per_product: int,
    pdf_patterns: list[str],
) -> tuple[list[str], list[str]]:
    source_root = BATCHES[batch_key]
    errors: list[str] = []
    notes: list[str] = []

    if not source_root.exists():
        return [f"Missing source package: {source_root}"], notes

    for product_source in sorted(path for path in source_root.iterdir() if path.is_dir()):
        if only and product_source.name not in only:
            continue
        if not (product_source / "html").exists() and not (product_source / "spreadsheets").exists():
            continue

        product_output = output_root / batch_key / product_source.name
        if not product_output.exists():
            errors.append(f"{batch_key}/{product_source.name}: missing export folder")
            continue

        pdf_names = expected_pdfs(product_source)
        if pdf_patterns:
            pdf_names = [
                name
                for name in pdf_names
                if any(Path(name).match(pattern) for pattern in pdf_patterns)
            ]
        if files_per_product > 0:
            pdf_names = pdf_names[:files_per_product]

        for pdf_name in pdf_names:
            pdf_path = product_output / "pdfs" / pdf_name
            if not pdf_path.exists():
                errors.append(f"{batch_key}/{product_source.name}: missing PDF {pdf_name}")
                continue
            if pdf_path.stat().st_size < 10_000:
                errors.append(f"{batch_key}/{product_source.name}: PDF looks too small {pdf_name}")
            pages = pdf_pages(pdf_path)
            page_note = f"{pages} pages" if pages else "page count not read"
            notes.append(f"{batch_key}/{product_source.name}: {pdf_name} OK ({page_note})")

        for sheet_name in expected_sheets(product_source):
            sheet_path = product_output / "spreadsheets" / sheet_name
            if not sheet_path.exists():
                errors.append(f"{batch_key}/{product_source.name}: missing spreadsheet {sheet_name}")

    return errors, notes


def main() -> None:
    args = parse_args()
    output_root = args.output.expanduser()
    only = set(args.only)
    all_errors: list[str] = []
    all_notes: list[str] = []

    for batch_key in selected_batches(args.batch):
        errors, notes = validate_batch(
            batch_key,
            output_root,
            only,
            args.files_per_product,
            args.pdf_pattern,
        )
        all_errors.extend(errors)
        all_notes.extend(notes)

    report = [
        "# Customer PDF Export Validation",
        "",
        f"Output folder: `{output_root}`",
        "",
        f"PDFs checked: {len(all_notes)}",
        f"Errors: {len(all_errors)}",
        "",
    ]
    if all_errors:
        report += ["## Errors", ""]
        report.extend([f"- {error}" for error in all_errors])
        report.append("")
    report += ["## Checked Files", ""]
    report.extend([f"- {note}" for note in all_notes])

    report_path = output_root / "VALIDATION_REPORT.md"
    output_root.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(report_path)
    print(f"Errors: {len(all_errors)}")
    if all_errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
