#!/usr/bin/env python3
"""Compare exported PDF page counts against source manifest counts."""

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
    parser = argparse.ArgumentParser(description="Audit exported PDFs for page-count/layout risk.")
    parser.add_argument("--batch", choices=["all", *BATCHES.keys()], default="phase-1")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--only",
        nargs="*",
        default=[],
        help="Optional product folder slugs to audit.",
    )
    parser.add_argument(
        "--files-per-product",
        type=int,
        default=0,
        help="Demo mode: audit only the first N expected PDFs per product.",
    )
    parser.add_argument(
        "--pdf-pattern",
        nargs="*",
        default=[],
        help="Optional glob pattern(s) for expected PDFs, such as '04-brand-kit*.pdf'.",
    )
    return parser.parse_args()


def selected_batches(key: str) -> list[str]:
    return list(BATCHES) if key == "all" else [key]


def expected_items(product_source: Path) -> list[tuple[str, int | None]]:
    manifest = product_source / "MANIFEST.md"
    if manifest.exists():
        text = manifest.read_text(encoding="utf-8")
        items: list[tuple[str, int | None]] = []
        pattern = re.compile(r"-> `([^`]+\.pdf)` — (?:(\d+) pages;)?")
        for match in pattern.finditer(text):
            pages = int(match.group(2)) if match.group(2) else None
            items.append((match.group(1), pages))
        if items:
            return items

    html_dir = product_source / "html"
    if not html_dir.exists():
        return []
    items = []
    for html in sorted(html_dir.glob("*.html")):
        page_count = len(re.findall(r'<section class="[^"]*\bpage\b', html.read_text(encoding="utf-8", errors="ignore")))
        items.append((html.with_suffix(".pdf").name, page_count or None))
    return items


def pdf_pages(pdf_path: Path) -> int | None:
    if not pdf_path.exists():
        return None
    data = pdf_path.read_bytes()
    matches = re.findall(rb"/Type\s*/Page\b", data)
    return len(matches) if matches else None


def main() -> None:
    args = parse_args()
    output = args.output.expanduser()
    only = set(args.only)
    rows: list[tuple[str, str, str, int | None, int | None, str]] = []

    for batch_key in selected_batches(args.batch):
        source_root = BATCHES[batch_key]
        if not source_root.exists():
            rows.append((batch_key, "missing-source-package", "", None, None, "missing source package"))
            continue

        for product_source in sorted(path for path in source_root.iterdir() if path.is_dir()):
            if only and product_source.name not in only:
                continue
            if not (product_source / "html").exists():
                continue
            items = expected_items(product_source)
            if args.pdf_pattern:
                items = [
                    item
                    for item in items
                    if any(Path(item[0]).match(pattern) for pattern in args.pdf_pattern)
                ]
            if args.files_per_product > 0:
                items = items[: args.files_per_product]
            for pdf_name, expected in items:
                pdf_path = output / batch_key / product_source.name / "pdfs" / pdf_name
                actual = pdf_pages(pdf_path)
                if actual is None:
                    status = "missing export"
                elif expected is None:
                    status = "no expected count"
                elif actual == expected:
                    status = "ok"
                elif actual > expected:
                    status = f"overflow risk: +{actual - expected} pages"
                else:
                    status = f"possible clipping: -{expected - actual} pages"
                rows.append((batch_key, product_source.name, pdf_name, expected, actual, status))

    risk_rows = [row for row in rows if row[5] != "ok"]
    lines = [
        "# PDF Layout Risk Report",
        "",
        f"Output folder: `{output}`",
        "",
        f"Files checked: {len(rows)}",
        f"Files needing attention: {len(risk_rows)}",
        "",
        "## Attention Items",
        "",
        "| Batch | Product | PDF | Expected Pages | Exported Pages | Status |",
        "|---|---|---|---:|---:|---|",
    ]
    for batch, product, pdf, expected, actual, status in risk_rows:
        lines.append(f"| {batch} | {product} | `{pdf}` | {expected or ''} | {actual or ''} | {status} |")

    lines += [
        "",
        "## All Files",
        "",
        "| Batch | Product | PDF | Expected Pages | Exported Pages | Status |",
        "|---|---|---|---:|---:|---|",
    ]
    for batch, product, pdf, expected, actual, status in rows:
        lines.append(f"| {batch} | {product} | `{pdf}` | {expected or ''} | {actual or ''} | {status} |")

    output.mkdir(parents=True, exist_ok=True)
    report = output / "PDF_LAYOUT_RISK_REPORT.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report)
    print(f"Files needing attention: {len(risk_rows)}")
    if risk_rows:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
