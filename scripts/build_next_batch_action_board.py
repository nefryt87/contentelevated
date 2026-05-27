#!/usr/bin/env python3
"""Create Payhip action board and cover map for the next approved batch."""

from __future__ import annotations

import ast
import csv
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_PATH = ROOT / "data/site.js"
INVENTORY_PATH = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
OUT_MD = ROOT / "content-elevated-product-os/internal/_global/next-batch-payhip-action-board.md"
OUT_CSV = ROOT / "content-elevated-product-os/internal/_global/next-batch-payhip-action-board.csv"
OUT_COVERS = ROOT / "content-elevated-product-os/internal/_global/next-batch-cover-map.md"

NEXT_BATCH = {
    "barbers": "Barber Growth Bundle",
    "dog-walkers-and-pet-sitters": "Dog Walker Growth Bundle",
    "personal-trainers": "Personal Trainer Growth Bundle",
    "personal-chefs": "Personal Chef Growth Bundle",
    "nannies-and-childcare-professionals": "Nanny Professional Bundle",
    "florists": "Florist Growth Bundle",
    "event-planners": "Event Planner Growth Bundle",
    "videographers": "Videographer Growth Bundle",
    "public-speakers": "Public Speaker Growth Bundle",
    "personal-stylists": "Personal Stylist Growth Bundle",
    "life-and-business-coaches": "Life Coach & Business Coach Growth Bundle",
}


def parse_raw_products() -> dict[str, dict[str, str]]:
    text = SITE_PATH.read_text(encoding="utf-8")
    block = re.search(r"const rawProducts = \[(.*?)]\s*;", text, re.S)
    if not block:
        raise SystemExit("Could not find rawProducts block")

    rows = re.findall(r"\[\s*([\s\S]*?)\s*\](?:,|\s*$)", block.group(1))
    products: dict[str, dict[str, str]] = {}
    for row in rows:
        values = ast.literal_eval("[" + row + "]")
        if len(values) >= 5:
            title, description, category, product_url, image = values[:5]
            products[title] = {
                "description": description,
                "category": category,
                "product_url": product_url,
                "image": image,
            }
    return products


def main() -> None:
    products = parse_raw_products()
    inventory = {item["slug"]: item for item in json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))}

    rows: list[dict[str, str | int]] = []
    for slug, website_title in NEXT_BATCH.items():
        inv = inventory[slug]
        product = products.get(website_title, {})
        payhip_url = product.get("product_url", "")
        rows.append(
            {
                "product": inv["product_name"],
                "internal_slug": slug,
                "website_title": website_title,
                "payhip_url": payhip_url,
                "price": "",
                "cover_saved_locally": "no",
                "customer_files": inv["customer_pdf_count"],
                "spreadsheets": inv["spreadsheet_count"],
                "customer_pages": inv["total_customer_pages"],
                "source_package": f"content-elevated-product-os/exports/next-batch-source-package/{slug}/",
                "final_pdf_export": "needed",
                "payhip_file_reupload": "needed",
                "website_copy_update": "needed",
                "status": "matched from website data" if payhip_url else "needs Payhip URL/title/cover confirmed",
            }
        )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md = [
        "# Next Batch Payhip Action Board",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Use this board after Phase 1 to export final PDFs, replace Payhip files, save covers locally, and connect final website copy.",
        "",
        "| Product | Payhip URL | Files | Sheets | Pages | Final PDF Export | Payhip Reupload | Website | Missing |",
        "|---|---|---:|---:|---:|---|---|---|---|",
    ]
    for row in rows:
        missing = []
        if not row["payhip_url"]:
            missing.append("Payhip URL")
        if not row["price"]:
            missing.append("price")
        if row["cover_saved_locally"] != "yes":
            missing.append("cover")
        payhip = row["payhip_url"] or "confirm"
        md.append(
            f"| {row['product']} | {payhip} | {row['customer_files']} | {row['spreadsheets']} | {row['customer_pages']} | needed | needed | needed | {', '.join(missing)} |"
        )

    md += [
        "",
        "## Source Package",
        "",
        "- Folder: `content-elevated-product-os/exports/next-batch-source-package/`",
        "- Archive: `content-elevated-product-os/exports/next-batch-source-package.zip`",
        "- Validation: `content-elevated-product-os/internal/_global/next-batch-readiness-audit.md`",
        "",
        "## Notes",
        "",
        "- Price and cover image are missing until confirmed from Payhip.",
        "- Final PDF export is blocked locally for the same reason as Phase 1; use the export SOP.",
        "",
    ]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    cover_lines = [
        "# Next Batch Cover Map",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Save these Payhip/website cover images locally under `content-elevated-product-os/assets/product-covers/`.",
        "",
        "| Internal Product | Website/Payhip Product | Cover URL | Local Asset Needed |",
        "|---|---|---|---|",
    ]
    for slug, website_title in NEXT_BATCH.items():
        inv = inventory[slug]
        product = products.get(website_title, {})
        cover = product.get("image", "confirm from Payhip")
        cover_lines.append(f"| {inv['product_name']} | {website_title} | {cover} | `assets/product-covers/{slug}-cover.png` |")
    cover_lines.append("")
    OUT_COVERS.write_text("\n".join(cover_lines), encoding="utf-8")

    print(OUT_MD)
    print(OUT_COVERS)


if __name__ == "__main__":
    main()
