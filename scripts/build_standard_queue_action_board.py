#!/usr/bin/env python3
"""Build an action board for products outside Phase 1, next batch, and design review."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "content-elevated-product-os/data/product-master.csv"
INVENTORY = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
OUT_MD = ROOT / "content-elevated-product-os/internal/_global/standard-queue-action-board.md"
OUT_CSV = ROOT / "content-elevated-product-os/internal/_global/standard-queue-action-board.csv"

PHASE_1 = {
    "hair-stylists",
    "med-spas",
    "dentists",
    "nutritionists",
    "hvac-contractors",
    "accountants-and-cpas",
    "wedding-photographers",
    "etsy-sellers",
}

NEXT_BATCH = {
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
}

DESIGN_REVIEW = set()


def main() -> None:
    with MASTER.open(newline="", encoding="utf-8") as f:
        master = {row["slug"]: row for row in csv.DictReader(f)}
    inventory = {row["slug"]: row for row in json.loads(INVENTORY.read_text(encoding="utf-8"))}
    slugs = [
        slug for slug in master
        if slug not in PHASE_1 and slug not in NEXT_BATCH and slug not in DESIGN_REVIEW
    ]

    rows = []
    for slug in slugs:
        item = inventory[slug]
        product = master[slug]
        missing = []
        if not product.get("payhip_url"):
            missing.append("Payhip URL")
        missing += ["price", "cover", "final PDF export", "visual proof"]
        rows.append(
            {
                "product": product["product_name"],
                "category": product["category"],
                "payhip_url": product.get("payhip_url", ""),
                "files": item["customer_pdf_count"],
                "sheets": item["spreadsheet_count"],
                "pages": item["total_customer_pages"],
                "status": "needs final export/proof",
                "missing": ", ".join(missing),
            }
        )

    lines = [
        "# Standard Queue Action Board",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "These products sit after Phase 1 and the next approved batch.",
        "",
        "| Product | Category | Payhip URL | Files | Sheets | Pages | Status | Missing |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['product']} | {row['category']} | {row['payhip_url'] or 'missing'} | "
            f"{row['files']} | {row['sheets']} | {row['pages']} | {row['status']} | {row['missing']} |"
        )
    lines += [
        "",
        "## Notes",
        "",
        "- These products have internal copy, upload checklists, and standalone-product maps generated.",
        "- Some may still need niche-fit visual review before final upload even if the automated scan is clean.",
        "- Missing Payhip URLs must be confirmed directly from Payhip before website connection.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["product"])
        writer.writeheader()
        writer.writerows(rows)

    print(OUT_MD)
    print(OUT_CSV)


if __name__ == "__main__":
    main()
