#!/usr/bin/env python3
"""Build a catalog-level operations coverage report."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "content-elevated-product-os/data/product-master.csv"
OUT = ROOT / "content-elevated-product-os/internal/_global/catalog-operations-coverage.md"

DESIGN_NEEDS_REVIEW = set()

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


def load_rows() -> list[dict[str, str]]:
    with MASTER.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def batch(row: dict[str, str]) -> str:
    slug = row["slug"]
    if slug in PHASE_1:
        return "Phase 1"
    if slug in NEXT_BATCH:
        return "Next approved batch"
    if slug in DESIGN_NEEDS_REVIEW:
        return "Design review needed"
    return "Standard queue"


def main() -> None:
    rows = load_rows()
    with_url = [r for r in rows if r.get("payhip_url")]
    without_url = [r for r in rows if not r.get("payhip_url")]
    phase1_ready = [r for r in rows if r["slug"] in PHASE_1 and r.get("payhip_url")]
    next_ready = [r for r in rows if r["slug"] in NEXT_BATCH and r.get("payhip_url")]

    lines = [
        "# Catalog Operations Coverage",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "This report tracks what is operationally ready for Payhip/website work and what still needs confirmation.",
        "",
        "## Summary",
        "",
        f"- Total products: {len(rows)}",
        f"- Products with Payhip URL recorded: {len(with_url)}",
        f"- Products missing Payhip URL: {len(without_url)}",
        f"- Phase 1 products with Payhip URL: {len(phase1_ready)} / {len(PHASE_1)}",
        f"- Next approved batch products with Payhip URL: {len(next_ready)} / {len(NEXT_BATCH)}",
        f"- Products parked for design review: {len(DESIGN_NEEDS_REVIEW)}",
        "",
        "## Missing Payhip URLs",
        "",
    ]
    if without_url:
        lines += ["| Product | Category | Batch |", "|---|---|---|"]
        for row in without_url:
            lines.append(f"| {row['product_name']} | {row['category']} | {batch(row)} |")
    else:
        lines.append("- None.")

    lines += [
        "",
        "## Design Review Needed",
        "",
        "| Product | Reason |",
        "|---|---|",
    ]
    reasons = {
    }
    for slug in sorted(DESIGN_NEEDS_REVIEW):
        row = next(r for r in rows if r["slug"] == slug)
        lines.append(f"| {row['product_name']} | {reasons[slug]} |")

    approved = [r for r in rows if r["slug"] in {"dog-walkers-and-pet-sitters", "personal-stylists", "life-and-business-coaches"}]
    if approved:
        lines += [
            "",
            "## Approved And Packaged",
            "",
            "| Product | Status |",
            "|---|---|",
        ]
        statuses = {
            "dog-walkers-and-pet-sitters": "Approved brighter trust-based pet-care direction applied to the full bundle and included in the next approved batch package.",
            "personal-stylists": "Approved fashion-editorial stylist direction applied to the full bundle and included in the next approved batch package.",
            "life-and-business-coaches": "Approved cool high-ticket coach strategy direction applied to the full bundle and included in the next approved batch package.",
        }
        for row in approved:
            lines.append(f"| {row['product_name']} | {statuses[row['slug']]} |")

    lines += [
        "",
        "## Price And Cover Status",
        "",
        "- Prices are not confirmed locally. Confirm in Payhip before final upload.",
        "- Cover images are mapped from website data for Phase 1 and the next approved batch, but still need to be saved locally under `assets/product-covers/`.",
        "- Hair Stylists still needs a confirmed standalone Payhip URL and cover source.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
