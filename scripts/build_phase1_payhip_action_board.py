#!/usr/bin/env python3
"""Create a human-friendly Payhip action board for the Phase 1 launch batch."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
OUT_MD = ROOT / "content-elevated-product-os/internal/_global/phase-1-payhip-action-board.md"
OUT_CSV = ROOT / "content-elevated-product-os/internal/_global/phase-1-payhip-action-board.csv"

PHASE_1 = {
    "hair-stylists": {
        "website_title": "",
        "website_slug": "",
        "payhip_url": "",
        "status": "missing from website data; needs Payhip URL/title/cover confirmed",
    },
    "med-spas": {
        "website_title": "Med Spa Aesthetician Growth Bundle",
        "website_slug": "med-spa-aesthetician-growth-bundle",
        "payhip_url": "https://payhip.com/b/uRbgW",
        "status": "matched from website data",
    },
    "dentists": {
        "website_title": "Dental Practice Growth Bundle",
        "website_slug": "dental-practice-growth-bundle",
        "payhip_url": "https://payhip.com/b/RXUZc",
        "status": "matched from website data",
    },
    "nutritionists": {
        "website_title": "Nutritionist & Dietitian Growth Bundle",
        "website_slug": "nutritionist-and-dietitian-growth-bundle",
        "payhip_url": "https://payhip.com/b/xz0Tr",
        "status": "matched from website data",
    },
    "hvac-contractors": {
        "website_title": "HVAC Contractor Growth Bundle",
        "website_slug": "hvac-contractor-growth-bundle",
        "payhip_url": "https://payhip.com/b/r9Jay",
        "status": "matched from website data",
    },
    "accountants-and-cpas": {
        "website_title": "Accountant & CPA Growth Bundle",
        "website_slug": "accountant-and-cpa-growth-bundle",
        "payhip_url": "https://payhip.com/b/9zcAT",
        "status": "matched from website data",
    },
    "wedding-photographers": {
        "website_title": "Wedding Photographer Growth Bundle",
        "website_slug": "wedding-photographer-growth-bundle",
        "payhip_url": "https://payhip.com/b/r5HSz",
        "status": "matched from website data",
    },
    "etsy-sellers": {
        "website_title": "Etsy Seller Growth Bundle",
        "website_slug": "etsy-seller-growth-bundle",
        "payhip_url": "https://payhip.com/b/x7D4I",
        "status": "matched from website data",
    },
}


def main() -> None:
    inventory = {item["slug"]: item for item in json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))}
    rows = []
    for slug, match in PHASE_1.items():
        product = inventory[slug]
        rows.append(
            {
                "product": product["product_name"],
                "internal_slug": slug,
                "website_title": match["website_title"],
                "website_slug": match["website_slug"],
                "payhip_url": match["payhip_url"],
                "price": "",
                "cover_saved_locally": "no",
                "customer_files": product["customer_pdf_count"],
                "spreadsheets": product["spreadsheet_count"],
                "customer_pages": product["total_customer_pages"],
                "source_package": f"content-elevated-product-os/exports/phase-1-payhip-source-package/{slug}/",
                "final_pdf_export": "needed",
                "payhip_file_reupload": "needed",
                "website_copy_update": "needed",
                "status": match["status"],
            }
        )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Phase 1 Payhip Action Board",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Use this board to finish the upload loop: export final PDFs, replace Payhip files, save cover images locally, then update the storefront product data.",
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
        missing_text = ", ".join(missing) if missing else "price, cover"
        payhip = row["payhip_url"] or "confirm"
        lines.append(
            f"| {row['product']} | {payhip} | {row['customer_files']} | {row['spreadsheets']} | {row['customer_pages']} | needed | needed | needed | {missing_text} |"
        )

    lines += [
        "",
        "## Source Package",
        "",
        "- Folder: `content-elevated-product-os/exports/phase-1-payhip-source-package/`",
        "- Archive: `content-elevated-product-os/exports/phase-1-payhip-source-package.zip`",
        "- Validation: `content-elevated-product-os/internal/_global/phase-1-package-validation.md`",
        "",
        "## Notes",
        "",
        "- Hair Stylists still needs a confirmed standalone Payhip URL and website product entry.",
        "- Price and cover image are missing for every Phase 1 row until confirmed from Payhip.",
        "- Do not upload internal Hair Stylists launch/reference files.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)


if __name__ == "__main__":
    main()
