#!/usr/bin/env python3
"""Update known Payhip URLs in product-master.csv from data/site.js."""

from __future__ import annotations

import ast
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_PATH = ROOT / "data/site.js"
MASTER_PATH = ROOT / "content-elevated-product-os/data/product-master.csv"
INTERNAL = ROOT / "content-elevated-product-os/internal"

TITLE_BY_SLUG = {
    "accountants-and-cpas": "Accountant & CPA Growth Bundle",
    "barbers": "Barber Growth Bundle",
    "bridal-hair-and-makeup-artists": "Bridal Hair & Makeup Artist Growth Bundle",
    "broker-toolkit": "Healthcare Broker Solo Toolkit",
    "car-wash-businesses": "Car Wash Growth Bundle",
    "chiropractors": "Chiropractor Growth Bundle",
    "dentists": "Dental Practice Growth Bundle",
    "dog-walkers-and-pet-sitters": "Dog Walker Growth Bundle",
    "electricians": "Electrician Growth Bundle",
    "etsy-sellers": "Etsy Seller Growth Bundle",
    "event-planners": "Event Planner Growth Bundle",
    "financial-advisors": "Financial Advisor Growth Bundle",
    "florists": "Florist Growth Bundle",
    "hvac-contractors": "HVAC Contractor Growth Bundle",
    "interior-designers": "Interior Designer Growth Bundle",
    "life-and-business-coaches": "Life Coach & Business Coach Growth Bundle",
    "makeup-artists": "Makeup Artist Growth Bundle",
    "massage-therapists": "Massage Therapist Growth Bundle",
    "med-spas": "Med Spa Aesthetician Growth Bundle",
    "mortgage-brokers": "Mortgage Broker Growth Bundle",
    "nail-technicians": "Nail Technician Growth Bundle",
    "nannies-and-childcare-professionals": "Nanny Professional Bundle",
    "nutritionists": "Nutritionist & Dietitian Growth Bundle",
    "party-planners": "Party Planner Growth Bundle",
    "personal-chefs": "Personal Chef Growth Bundle",
    "personal-stylists": "Personal Stylist Growth Bundle",
    "personal-trainers": "Personal Trainer Growth Bundle",
    "physical-therapists": "Physical Therapist Growth Bundle",
    "plumbers": "Plumber Growth Bundle",
    "public-speakers": "Public Speaker Growth Bundle",
    "tattoo-artists": "Tattoo Artist Growth Bundle",
    "videographers": "Videographer Growth Bundle",
    "wedding-photographers": "Wedding Photographer Growth Bundle",
}


def parse_site_urls() -> dict[str, str]:
    text = SITE_PATH.read_text(encoding="utf-8")
    block = re.search(r"const rawProducts = \[(.*?)]\s*;", text, re.S)
    if not block:
        raise SystemExit("Could not find rawProducts block")

    urls: dict[str, str] = {}
    rows = re.findall(r"\[\s*([\s\S]*?)\s*\](?:,|\s*$)", block.group(1))
    for row in rows:
        values = ast.literal_eval("[" + row + "]")
        if len(values) >= 4:
            title, _description, _category, product_url = values[:4]
            urls[title] = product_url
    return urls


def main() -> None:
    urls = parse_site_urls()
    rows: list[dict[str, str]] = []
    updated = 0
    tracker_updated = 0
    with MASTER_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            title = TITLE_BY_SLUG.get(row["slug"])
            if title and urls.get(title):
                row["payhip_url"] = urls[title]
                note = row.get("notes", "").rstrip()
                if "Payhip URL pulled from current website data" not in note:
                    note = (note.rstrip(".") + ". Payhip URL pulled from current website data; price and cover still need confirmation.").lstrip(". ")
                row["notes"] = note
                tracker_path = INTERNAL / row["slug"] / "payhip-url-and-price.md"
                if tracker_path.exists():
                    token = urls[title].rstrip("/").split("/")[-1]
                    tracker_path.write_text(
                        "\n".join(
                            [
                                f"# {row['product_name']} Payhip URL + Price",
                                "",
                                f"- Payhip product URL: {urls[title]}",
                                f"- Checkout URL: https://payhip.com/buy?link={token}",
                                "- Current price: confirm in Payhip",
                                "- Sale/launch price: confirm in Payhip",
                                "- Cover image saved locally: no",
                                "- Notes: URL pulled from current website product data. Price and cover still need confirmation from Payhip.",
                                "",
                            ]
                        ),
                        encoding="utf-8",
                    )
                    tracker_updated += 1
                updated += 1
            rows.append(row)

    with MASTER_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {updated} product-master rows and {tracker_updated} per-product trackers from website data")


if __name__ == "__main__":
    main()
