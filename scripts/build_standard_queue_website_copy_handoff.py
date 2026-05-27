#!/usr/bin/env python3
"""Build a structured website-copy handoff for standard-queue products."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from standard_queue import ROOT, load_master, standard_queue_slugs


INTERNAL = ROOT / "content-elevated-product-os/internal"
OUT_MD = ROOT / "content-elevated-product-os/internal/_global/standard-queue-website-copy-handoff.md"
OUT_JSON = ROOT / "content-elevated-product-os/internal/_global/standard-queue-website-copy-handoff.json"


def site_slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower().replace("&", "and")).strip("-")


def section(text: str, title: str) -> str:
    pattern = rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.S | re.M)
    return match.group(1).strip() if match else ""


def bullets(block: str) -> list[str]:
    return [line[2:].strip() for line in block.splitlines() if line.startswith("- ")]


def hero_fields(block: str) -> dict[str, str]:
    fields = {}
    for line in bullets(block):
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip().lower().replace(" ", "_")] = value.strip()
    return fields


def clean_niche(product_name: str) -> str:
    return (
        product_name
        .replace(" Growth Bundle", "")
        .replace("Businesses", "businesses")
        .replace("Business", "businesses")
    )


def fallback_subhead(product_name: str) -> str:
    niche = clean_niche(product_name)
    return f"A premium content, client, brand, and growth system built for {niche}."


def polish_generic_copy(value: str, product_name: str) -> str:
    niche = clean_niche(product_name)
    replacements = {
        "aestheticians businesses": "aestheticians",
        "attorneys businesses": "attorneys",
        "bridal hair & makeup artists businesses": "bridal hair and makeup artists",
        "broker toolkit businesses": "healthcare brokers",
        "car wash businesses businesses": "car wash businesses",
        "chiropractors businesses": "chiropractors",
        "electricians businesses": "electricians",
        "financial advisors businesses": "financial advisors",
        "insurance agents businesses": "insurance agents",
        "interior designers businesses": "interior designers",
        "lash technicians businesses": "lash technicians",
        "makeup artists businesses": "makeup artists",
        "massage therapists businesses": "massage therapists",
        "mortgage brokers businesses": "mortgage brokers",
        "nail technicians businesses": "nail technicians",
        "party planners businesses": "party planners",
        "physical therapists businesses": "physical therapists",
        "plumbers businesses": "plumbers",
        "tattoo artists businesses": "tattoo artists",
    }
    output = value
    for before, after in replacements.items():
        output = output.replace(before, after)
    output = output.replace(f"{niche} businesses", niche)
    return output


def concise_summary(product_name: str, summary: str) -> str:
    if summary:
        return polish_generic_copy(summary, product_name)
    niche = clean_niche(product_name)
    return (
        f"The {product_name} gives {niche} a practical growth system for content, AI prompts, "
        "client communication, brand direction, and repeatable marketing execution."
    )


def main() -> None:
    master = load_master()
    records = []

    for slug in standard_queue_slugs():
        product = master[slug]
        path = INTERNAL / slug / "website-product-copy.md"
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        hero = hero_fields(section(text, "Product Page Hero"))
        website_title = product["product_name"]
        summary = concise_summary(website_title, section(text, "Product Summary"))
        record = {
            "internal_slug": slug,
            "website_title": website_title,
            "website_slug": site_slug(website_title),
            "category": product["category"],
            "payhip_url": product.get("payhip_url", ""),
            "h1": hero.get("h1", website_title),
            "eyebrow": hero.get("eyebrow", product["category"]),
            "subhead": polish_generic_copy(hero.get("subhead", ""), website_title) or fallback_subhead(website_title),
            "summary": summary,
            "inventory": bullets(section(text, "Bundle Inventory")),
            "inside": bullets(section(text, "What's Inside")),
            "who_it_is_for": bullets(section(text, "Who It Is For")),
            "details": bullets(section(text, "Product Details")),
            "outcomes": bullets(section(text, "Outcomes")),
        }
        records.append(record)

    OUT_JSON.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Standard Queue Website Copy Handoff",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Use this as a working handoff for website product pages and future Payhip copy polish.",
        "",
    ]
    for record in records:
        lines += [
            f"## {record['h1'] or record['website_title']}",
            "",
            f"- Internal slug: `{record['internal_slug']}`",
            f"- Website title: {record['website_title']}",
            f"- Website slug: `{record['website_slug']}`",
            f"- Category: {record['category']}",
            f"- Payhip URL: {record['payhip_url'] or 'needs confirmation'}",
            f"- Subhead: {record['subhead'] or 'Needs final copy polish.'}",
            "",
            "### Summary",
            "",
            record["summary"],
            "",
            "### Inventory",
            "",
        ]
        if record["inventory"]:
            lines.extend(f"- {item}" for item in record["inventory"])
        else:
            lines.append("- Inventory needs confirmation from packaged source.")
        lines += ["", "### Outcomes", ""]
        if record["outcomes"]:
            lines.extend(f"- {item}" for item in record["outcomes"])
        else:
            lines.append("- Outcomes need final copy polish.")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)
    print(OUT_JSON)


if __name__ == "__main__":
    main()
