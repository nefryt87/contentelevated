#!/usr/bin/env python3
"""Build a cover-image map for standard-queue products."""

from __future__ import annotations

import ast
import re
from datetime import date
from pathlib import Path

from standard_queue import ROOT, load_master, standard_queue_slugs


SITE_PATH = ROOT / "data/site.js"
OUT = ROOT / "content-elevated-product-os/internal/_global/standard-queue-cover-map.md"


def parse_raw_products() -> dict[str, dict[str, str]]:
    text = SITE_PATH.read_text(encoding="utf-8")
    block = re.search(r"const rawProducts = \[(.*?)]\s*;", text, re.S)
    if not block:
        return {}
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


TITLE_ALIASES = {
    "attorneys": "Attorney Growth Bundle",
    "bridal-hair-and-makeup-artists": "Bridal Hair & Makeup Artist Growth Bundle",
    "broker-toolkit": "Healthcare Broker Solo Toolkit",
    "car-wash-businesses": "Car Wash Growth Bundle",
    "chiropractors": "Chiropractor Growth Bundle",
    "electricians": "Electrician Growth Bundle",
    "financial-advisors": "Financial Advisor Growth Bundle",
    "interior-designers": "Interior Designer Growth Bundle",
    "makeup-artists": "Makeup Artist Growth Bundle",
    "massage-therapists": "Massage Therapist Growth Bundle",
    "mortgage-brokers": "Mortgage Broker Growth Bundle",
    "nail-technicians": "Nail Technician Growth Bundle",
    "party-planners": "Party Planner Growth Bundle",
    "physical-therapists": "Physical Therapist Growth Bundle",
    "plumbers": "Plumber Growth Bundle",
    "tattoo-artists": "Tattoo Artist Growth Bundle",
}


def likely_site_title(slug: str, product_name: str, titles: list[str]) -> str:
    alias = TITLE_ALIASES.get(slug)
    if alias in titles:
        return alias

    candidates = [
        product_name,
        product_name.replace("Businesses", "Business"),
        product_name.replace("Contractors", "Contractor"),
        product_name.replace("Therapists", "Therapist"),
        product_name.replace("Technicians", "Technician"),
        product_name.replace("Advisors", "Advisor"),
        product_name.replace("Brokers", "Broker"),
        product_name.replace("Attorneys", "Attorney"),
    ]
    for candidate in candidates:
        if candidate in titles:
            return candidate
    return ""


def main() -> None:
    master = load_master()
    site = parse_raw_products()
    titles = list(site)

    lines = [
        "# Standard Queue Cover Map",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Save these Payhip/website cover images locally under `content-elevated-product-os/assets/product-covers/`.",
        "",
        "| Internal Product | Matched Website/Payhip Product | Payhip URL | Cover URL | Local Asset Needed |",
        "|---|---|---|---|---|",
    ]
    for slug in standard_queue_slugs():
        row = master[slug]
        title = likely_site_title(slug, row["product_name"], titles)
        product = site.get(title, {})
        lines.append(
            f"| {row['product_name']} | {title or 'needs confirmation'} | "
            f"{product.get('product_url') or row.get('payhip_url') or 'needs confirmation'} | "
            f"{product.get('image') or 'needs confirmation'} | `assets/product-covers/{slug}-cover.png` |"
        )
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
