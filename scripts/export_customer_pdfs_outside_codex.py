#!/usr/bin/env python3
"""Export Content Elevated customer HTML packages to Payhip-ready PDFs.

This script is meant to be run from normal macOS Terminal, outside the Codex
sandbox. It uses the installed Google Chrome app to print the approved HTML
source packages as PDFs, then copies spreadsheets and writes an export report.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS_ROOT = ROOT / "content-elevated-product-os" / "exports"
DEFAULT_OUTPUT_ROOT = EXPORTS_ROOT / "customer-pdf-export"
DEFAULT_CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


@dataclass(frozen=True)
class Batch:
    key: str
    label: str
    source: Path


BATCHES = [
    Batch(
        key="phase-1",
        label="Phase 1",
        source=EXPORTS_ROOT / "phase-1-payhip-source-package",
    ),
    Batch(
        key="next",
        label="Next Batch",
        source=EXPORTS_ROOT / "next-batch-source-package",
    ),
    Batch(
        key="standard",
        label="Standard Queue",
        source=EXPORTS_ROOT / "standard-queue-source-package",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Content Elevated HTML product files to PDFs with Chrome."
    )
    parser.add_argument(
        "--batch",
        choices=["all", *[batch.key for batch in BATCHES]],
        default="phase-1",
        help="Which packaged batch to export. Default: phase-1.",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        default=[],
        help="Optional product folder slugs to export, such as hair-stylists med-spas.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Destination folder for PDFs and copied spreadsheets.",
    )
    parser.add_argument(
        "--chrome",
        type=Path,
        default=DEFAULT_CHROME,
        help="Path to Google Chrome.",
    )
    parser.add_argument(
        "--slow",
        action="store_true",
        help="Use a longer render wait for heavier files.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=45,
        help="Seconds before one PDF export is treated as stuck. Default: 45.",
    )
    parser.add_argument(
        "--files-per-product",
        type=int,
        default=0,
        help="Demo mode: export only the first N HTML files per product. Default: 0 means all files.",
    )
    parser.add_argument(
        "--html-pattern",
        default="",
        help="Optional glob pattern for HTML files inside each product, such as '04-brand-kit*.html'.",
    )
    return parser.parse_args()


def selected_batches(key: str) -> list[Batch]:
    if key == "all":
        return BATCHES
    return [batch for batch in BATCHES if batch.key == key]


def product_dirs(batch: Batch, only: set[str]) -> list[Path]:
    if not batch.source.exists():
        raise SystemExit(f"Missing source package: {batch.source}")

    dirs = [
        path
        for path in sorted(batch.source.iterdir())
        if path.is_dir() and (path / "html").exists()
    ]
    if only:
        dirs = [path for path in dirs if path.name in only]

    return dirs


def estimate_pdf_pages(pdf_path: Path) -> int | None:
    """Lightweight page-count fallback with no external dependencies."""
    try:
        data = pdf_path.read_bytes()
    except OSError:
        return None

    matches = re.findall(rb"/Type\s*/Page\b", data)
    if matches:
        return len(matches)
    return None


def pdf_ok(pdf_path: Path) -> bool:
    return pdf_path.exists() and pdf_path.stat().st_size > 10_000


def export_with_chrome(chrome: Path, html_path: Path, pdf_path: Path, profile_dir: Path, slow: bool, timeout: int) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    wait_ms = "3500" if slow else "1800"

    base_flags = [
        str(chrome),
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        f"--user-data-dir={profile_dir}",
        f"--virtual-time-budget={wait_ms}",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]

    attempts = [
        ["--headless=new", *base_flags[1:]],
        ["--headless", *base_flags[1:]],
    ]

    last_error = ""
    for flags in attempts:
        cmd = [str(chrome), *flags]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            if pdf_ok(pdf_path):
                return
            last_error = f"Timed out after {timeout}s"
            if exc.stderr:
                stderr = exc.stderr.decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else exc.stderr
                last_error += f": {stderr.strip()}"
            if pdf_path.exists() and not pdf_ok(pdf_path):
                pdf_path.unlink()
            continue
        if result.returncode == 0 and pdf_ok(pdf_path):
            return
        last_error = (result.stderr or result.stdout or "").strip()
        if pdf_path.exists() and not pdf_ok(pdf_path):
            pdf_path.unlink()

    raise RuntimeError(last_error or f"Chrome did not create a valid PDF for {html_path}")


def copy_spreadsheets(product_dir: Path, destination: Path) -> list[Path]:
    copied: list[Path] = []
    sheet_source = product_dir / "spreadsheets"
    if not sheet_source.exists():
        return copied

    sheet_destination = destination / "spreadsheets"
    sheet_destination.mkdir(parents=True, exist_ok=True)
    for sheet in sorted(sheet_source.glob("*.xlsx")):
        target = sheet_destination / sheet.name
        shutil.copy2(sheet, target)
        copied.append(target)
    return copied


def export_product(
    batch: Batch,
    product_dir: Path,
    output_root: Path,
    chrome: Path,
    profile_dir: Path,
    slow: bool,
    timeout: int,
    files_per_product: int,
    html_pattern: str,
) -> dict[str, object]:
    output_dir = output_root / batch.key / product_dir.name
    pdf_dir = output_dir / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    html_glob = html_pattern or "*.html"
    html_files = sorted((product_dir / "html").glob(html_glob))
    if files_per_product > 0:
        html_files = html_files[:files_per_product]
    exported: list[dict[str, object]] = []
    errors: list[str] = []

    for html_path in html_files:
        pdf_path = pdf_dir / html_path.with_suffix(".pdf").name
        print(f"  - {html_path.name} -> {pdf_path.name}", flush=True)
        try:
            export_with_chrome(chrome, html_path, pdf_path, profile_dir, slow, timeout)
            exported.append(
                {
                    "source": html_path.name,
                    "pdf": pdf_path.name,
                    "bytes": pdf_path.stat().st_size,
                    "pages": estimate_pdf_pages(pdf_path),
                }
            )
        except Exception as exc:  # noqa: BLE001 - report all export failures.
            print(f"    ERROR: {exc}", flush=True)
            errors.append(f"{html_path.name}: {exc}")

    spreadsheets = copy_spreadsheets(product_dir, output_dir)
    write_product_manifest(output_dir, batch, product_dir.name, exported, spreadsheets, errors)

    return {
        "batch": batch.key,
        "product": product_dir.name,
        "html_count": len(html_files),
        "pdf_count": len(exported),
        "spreadsheet_count": len(spreadsheets),
        "error_count": len(errors),
        "errors": errors,
    }


def write_product_manifest(
    output_dir: Path,
    batch: Batch,
    slug: str,
    exported: list[dict[str, object]],
    spreadsheets: list[Path],
    errors: list[str],
) -> None:
    lines = [
        f"# {slug} Export Manifest",
        "",
        f"Batch: {batch.label}",
        f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## PDFs",
        "",
    ]
    if exported:
        for item in exported:
            page_note = item["pages"] if item["pages"] is not None else "not counted"
            size_mb = int(item["bytes"]) / 1_000_000
            lines.append(
                f"- `pdfs/{item['pdf']}` from `{item['source']}` "
                f"({page_note} pages, {size_mb:.1f} MB)"
            )
    else:
        lines.append("- No PDFs exported.")

    lines += ["", "## Spreadsheets", ""]
    if spreadsheets:
        for sheet in spreadsheets:
            lines.append(f"- `spreadsheets/{sheet.name}`")
    else:
        lines.append("- None.")

    if errors:
        lines += ["", "## Export Errors", ""]
        for error in errors:
            lines.append(f"- {error}")

    (output_dir / "MANIFEST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_summary(output_root: Path, results: list[dict[str, object]]) -> None:
    lines = [
        "# Content Elevated Customer PDF Export",
        "",
        f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Summary",
        "",
    ]

    total_products = len(results)
    total_pdfs = sum(int(item["pdf_count"]) for item in results)
    total_html = sum(int(item["html_count"]) for item in results)
    total_sheets = sum(int(item["spreadsheet_count"]) for item in results)
    total_errors = sum(int(item["error_count"]) for item in results)

    lines += [
        f"- Products processed: {total_products}",
        f"- PDFs exported: {total_pdfs}/{total_html}",
        f"- Spreadsheets copied: {total_sheets}",
        f"- Errors: {total_errors}",
        "",
        "## Products",
        "",
    ]

    for item in results:
        status = "OK" if int(item["error_count"]) == 0 else "Needs review"
        lines.append(
            f"- {status}: `{item['batch']}/{item['product']}` "
            f"PDFs {item['pdf_count']}/{item['html_count']}, "
            f"spreadsheets {item['spreadsheet_count']}"
        )
        for error in item["errors"]:
            lines.append(f"  - {error}")

    (output_root / "EXPORT_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    chrome = args.chrome.expanduser()
    if not chrome.exists():
        raise SystemExit(f"Google Chrome was not found at: {chrome}")

    output_root = args.output.expanduser()
    output_root.mkdir(parents=True, exist_ok=True)

    only = set(args.only)
    results: list[dict[str, object]] = []

    with tempfile.TemporaryDirectory(prefix="content-elevated-chrome-") as tmp:
        profile_dir = Path(tmp) / "profile"
        for batch in selected_batches(args.batch):
            dirs = product_dirs(batch, only)
            if only and not dirs:
                print(f"No matching products found in {batch.label}.")
            for product_dir in dirs:
                print(f"Exporting {batch.label}: {product_dir.name}")
                results.append(
                    export_product(
                        batch=batch,
                        product_dir=product_dir,
                        output_root=output_root,
                        chrome=chrome,
                        profile_dir=profile_dir,
                        slow=args.slow,
                        timeout=args.timeout,
                        files_per_product=args.files_per_product,
                        html_pattern=args.html_pattern,
                    )
                )

    write_summary(output_root, results)

    errors = sum(int(item["error_count"]) for item in results)
    print("")
    print(f"Export folder: {output_root}")
    print(f"Products processed: {len(results)}")
    print(f"Errors: {errors}")
    if errors:
        print("Open EXPORT_SUMMARY.md for the files that need attention.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
