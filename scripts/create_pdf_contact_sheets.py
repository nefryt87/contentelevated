#!/usr/bin/env python3
"""Create visual contact sheets for exported customer PDFs.

This is a proofing helper for Content Elevated. It splits each PDF into
single-page temporary PDFs, asks macOS `sips` to render those pages, and then
builds one PNG contact sheet per PDF.

Run with the bundled Codex Python runtime because it includes pypdf and PIL.
"""

from __future__ import annotations

import argparse
import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPORT_ROOT = ROOT / "content-elevated-product-os" / "exports" / "customer-pdf-export"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create visual contact sheets for exported PDFs.")
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_EXPORT_ROOT,
        help="Export root containing phase/product/pdfs folders.",
    )
    parser.add_argument(
        "--batch",
        default="phase-1",
        help="Batch folder to inspect, such as phase-1, next, or standard.",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        default=[],
        help="Optional product slugs to inspect.",
    )
    parser.add_argument(
        "--pdf",
        nargs="*",
        type=Path,
        default=[],
        help="Optional specific PDF paths to inspect instead of scanning the root.",
    )
    parser.add_argument(
        "--pdf-pattern",
        nargs="*",
        default=[],
        help="Optional filename glob(s) for scanned PDFs, such as '04-brand-kit*.pdf'.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=40,
        help="Skip contact sheet generation for PDFs above this page count.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output folder. Defaults to <root>/_visual-audit/<batch>.",
    )
    return parser.parse_args()


def find_pdfs(root: Path, batch: str, only: set[str]) -> list[Path]:
    batch_root = root / batch
    if not batch_root.exists():
        return []

    pdfs: list[Path] = []
    for product_dir in sorted(path for path in batch_root.iterdir() if path.is_dir()):
        if only and product_dir.name not in only:
            continue
        pdf_dir = product_dir / "pdfs"
        if pdf_dir.exists():
            pdfs.extend(sorted(pdf_dir.glob("*.pdf")))
    return pdfs


def render_pdf_page(split_pdf: Path, png_path: Path) -> bool:
    result = subprocess.run(
        ["sips", "-s", "format", "png", str(split_pdf), "--out", str(png_path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0 and png_path.exists()


def make_contact_sheet(pdf_path: Path, out_path: Path, max_pages: int) -> str:
    reader = PdfReader(str(pdf_path))
    page_count = len(reader.pages)
    if page_count > max_pages:
        return f"SKIPPED {pdf_path.name}: {page_count} pages exceeds --max-pages {max_pages}"

    cards: list[Image.Image] = []
    with tempfile.TemporaryDirectory(prefix="content-elevated-pdf-proof-") as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        for page_number, page in enumerate(reader.pages, start=1):
            split_pdf = tmp_dir / f"page-{page_number:03d}.pdf"
            writer = PdfWriter()
            writer.add_page(page)
            with split_pdf.open("wb") as handle:
                writer.write(handle)

            page_png = tmp_dir / f"page-{page_number:03d}.png"
            if not render_pdf_page(split_pdf, page_png):
                continue

            image = Image.open(page_png).convert("RGB")
            image.thumbnail((255, 330), Image.Resampling.LANCZOS)

            card = Image.new("RGB", (285, 375), "white")
            card.paste(image, ((285 - image.width) // 2, 16))
            draw = ImageDraw.Draw(card)
            draw.text((12, 350), f"Page {page_number}", fill=(20, 20, 20))
            cards.append(card)

    if not cards:
        return f"FAILED {pdf_path.name}: no pages rendered"

    columns = 4
    rows = math.ceil(len(cards) / columns)
    sheet = Image.new("RGB", (columns * 285, rows * 375), (232, 232, 232))
    for index, card in enumerate(cards):
        x = (index % columns) * 285
        y = (index // columns) * 375
        sheet.paste(card, (x, y))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, quality=92)
    return f"OK {pdf_path.name}: {page_count} pages -> {out_path}"


def output_path_for(root: Path, batch: str, out_root: Path, pdf_path: Path) -> Path:
    try:
        rel = pdf_path.relative_to(root / batch)
    except ValueError:
        rel = Path(pdf_path.stem)

    parts = rel.parts
    if len(parts) >= 3 and parts[-2] == "pdfs":
        product = parts[0]
        return out_root / product / f"{pdf_path.stem}-contact-sheet.png"
    return out_root / f"{pdf_path.stem}-contact-sheet.png"


def main() -> None:
    args = parse_args()
    root = args.root.expanduser().resolve()
    batch = args.batch
    out_root = (args.out or root / "_visual-audit" / batch).expanduser().resolve()

    pdfs = [path.expanduser().resolve() for path in args.pdf]
    if not pdfs:
        pdfs = find_pdfs(root, batch, set(args.only))
        if args.pdf_pattern:
            pdfs = [
                path
                for path in pdfs
                if any(path.match(pattern) or path.name == pattern for pattern in args.pdf_pattern)
            ]

    if not pdfs:
        raise SystemExit("No PDFs found to inspect.")

    report_lines = [
        "# PDF Visual Audit Contact Sheets",
        "",
        f"Root: `{root}`",
        f"Batch: `{batch}`",
        "",
    ]

    for pdf_path in pdfs:
        out_path = output_path_for(root, batch, out_root, pdf_path)
        status = make_contact_sheet(pdf_path, out_path, args.max_pages)
        print(status)
        report_lines.append(f"- {status}")

    (out_root / "CONTACT_SHEET_REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print("")
    print(f"Contact sheet folder: {out_root}")


if __name__ == "__main__":
    main()
