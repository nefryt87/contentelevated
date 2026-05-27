#!/usr/bin/env python3
"""Create a Phase 1 cover-image map from website product data."""

from __future__ import annotations

import ast
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_PATH = ROOT / "data/site.js"
OUT = ROOT / "content-elevated-product-os/internal/_global/phase-1-cover-map.md"

PHASE_1_TITLE_MATCHES = {
    "Hair Stylists Growth Bundle": [],
    "Med Spas Growth Bundle": ["Med Spa Aesthetician Growth Bundle"],
    "Dentists Growth Bundle": ["Dental Practice Growth Bundle"],
    "Nutritionists Growth Bundle": ["Nutritionist & Dietitian Growth Bundle"],
    "HVAC Contractors Growth Bundle": ["HVAC Contractor Growth Bundle"],
    "Accountants & CPAs Growth Bundle": ["Accountant & CPA Growth Bundle"],
    "Wedding Photographers Growth Bundle": ["Wedding Photographer Growth Bundle"],
    "Etsy Sellers Growth Bundle": ["Etsy Seller Growth Bundle"],
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
    lines = [
        "# Phase 1 Cover Map",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Use this to download/save Payhip cover images locally under `content-elevated-product-os/assets/product-covers/`.",
        "",
        "| Internal Product | Website/Payhip Product | Cover URL | Local Asset Needed |",
        "|---|---|---|---|",
    ]

    for internal_title, website_titles in PHASE_1_TITLE_MATCHES.items():
        if not website_titles:
            lines.append(f"| {internal_title} | not found | confirm from Payhip | `assets/product-covers/hair-stylists-cover.png` |")
            continue
        website_title = website_titles[0]
        product = products.get(website_title)
        if not product:
            lines.append(f"| {internal_title} | {website_title} | not found in website data | confirm |")
            continue
        local_name = internal_title.lower().replace("&", "and")
        local_name = re.sub(r"[^a-z0-9]+", "-", local_name).strip("-")
        local_name = local_name.replace("-growth-bundle", "") + "-cover.png"
        lines.append(f"| {internal_title} | {website_title} | {product['image']} | `assets/product-covers/{local_name}` |")

    lines += [
        "",
        "## Notes",
        "",
        "- Hair Stylists does not currently have a matching standalone website product record.",
        "- Cover URLs are website image URLs from `data/site.js`; save local copies before final launch ops.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
