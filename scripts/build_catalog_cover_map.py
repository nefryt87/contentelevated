#!/usr/bin/env python3
"""Build a full catalog cover-image map from website product data."""

from __future__ import annotations

import ast
import csv
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_PATH = ROOT / "data/site.js"
MASTER = ROOT / "content-elevated-product-os/data/product-master.csv"
OUT = ROOT / "content-elevated-product-os/internal/_global/catalog-cover-map.md"

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


def parse_products() -> dict[str, dict[str, str]]:
    text = SITE_PATH.read_text(encoding="utf-8")
    block = re.search(r"const rawProducts = \[(.*?)]\s*;", text, re.S)
    if not block:
        raise SystemExit("Could not find rawProducts block")
    products: dict[str, dict[str, str]] = {}
    for row in re.findall(r"\[\s*([\s\S]*?)\s*\](?:,|\s*$)", block.group(1)):
        values = ast.literal_eval("[" + row + "]")
        if len(values) >= 5:
            title, _description, _category, product_url, image = values[:5]
            products[title] = {"payhip_url": product_url, "image": image}
    return products


def main() -> None:
    products = parse_products()
    with MASTER.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    lines = [
        "# Catalog Cover Map",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Use this to save all current storefront cover images locally under `content-elevated-product-os/assets/product-covers/`.",
        "",
        "| Product | Website/Payhip Product | Cover URL | Local Asset Needed |",
        "|---|---|---|---|",
    ]

    for row in rows:
        slug = row["slug"]
        title = TITLE_BY_SLUG.get(slug, "")
        product = products.get(title, {})
        cover = product.get("image", "confirm from Payhip")
        label = title or "confirm from Payhip"
        lines.append(f"| {row['product_name']} | {label} | {cover} | `assets/product-covers/{slug}-cover.png` |")

    lines += [
        "",
        "## Missing From Current Website Data",
        "",
        "- Aestheticians",
        "- Attorneys",
        "- Hair Stylists",
        "- Insurance Agents",
        "- Lash Technicians",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
