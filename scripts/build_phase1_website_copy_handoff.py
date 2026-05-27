#!/usr/bin/env python3
"""Build a structured website-copy handoff for Phase 1 products."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "content-elevated-product-os/internal"
OUT_MD = ROOT / "content-elevated-product-os/internal/_global/phase-1-website-copy-handoff.md"
OUT_JSON = ROOT / "content-elevated-product-os/internal/_global/phase-1-website-copy-handoff.json"

MAPPING = {
    "hair-stylists": {"website_title": "", "website_slug": "", "payhip_url": ""},
    "med-spas": {"website_title": "Med Spa Aesthetician Growth Bundle", "website_slug": "med-spa-aesthetician-growth-bundle", "payhip_url": "https://payhip.com/b/uRbgW"},
    "dentists": {"website_title": "Dental Practice Growth Bundle", "website_slug": "dental-practice-growth-bundle", "payhip_url": "https://payhip.com/b/RXUZc"},
    "nutritionists": {"website_title": "Nutritionist & Dietitian Growth Bundle", "website_slug": "nutritionist-and-dietitian-growth-bundle", "payhip_url": "https://payhip.com/b/xz0Tr"},
    "hvac-contractors": {"website_title": "HVAC Contractor Growth Bundle", "website_slug": "hvac-contractor-growth-bundle", "payhip_url": "https://payhip.com/b/r9Jay"},
    "accountants-and-cpas": {"website_title": "Accountant & CPA Growth Bundle", "website_slug": "accountant-and-cpa-growth-bundle", "payhip_url": "https://payhip.com/b/9zcAT"},
    "wedding-photographers": {"website_title": "Wedding Photographer Growth Bundle", "website_slug": "wedding-photographer-growth-bundle", "payhip_url": "https://payhip.com/b/r5HSz"},
    "etsy-sellers": {"website_title": "Etsy Seller Growth Bundle", "website_slug": "etsy-seller-growth-bundle", "payhip_url": "https://payhip.com/b/x7D4I"},
}

FALLBACK_OUTCOMES = {
    "hair-stylists": [
        "Plan 90 days of salon content with less weekly guesswork.",
        "Use AI prompts for captions, offers, emails, texts, reviews, and client experience.",
        "Improve rebooking, retention, follow-up, and review workflows.",
        "Build a more polished independent salon brand presence.",
    ],
    "med-spas": [
        "Plan 90 days of aesthetic practice content.",
        "Educate clients before and after treatments with more clarity.",
        "Improve inquiry, consultation, preparation, follow-up, and rebooking communication.",
        "Build a more premium and trustworthy client experience.",
    ],
}


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


def h3_sections(block: str) -> list[dict[str, str]]:
    parts = re.split(r"^### ", block, flags=re.M)
    output = []
    for part in parts[1:]:
        title, _, body = part.partition("\n")
        output.append({"title": title.strip(), "body": body.strip()})
    return output


def main() -> None:
    records = []
    for slug, mapping in MAPPING.items():
        path = INTERNAL / slug / "website-product-copy.md"
        text = path.read_text(encoding="utf-8")
        hero = hero_fields(section(text, "Product Page Hero"))
        record = {
            "internal_slug": slug,
            **mapping,
            "h1": hero.get("h1", ""),
            "eyebrow": hero.get("eyebrow", ""),
            "subhead": hero.get("subhead", ""),
            "primary_cta": hero.get("primary_cta", ""),
            "secondary_cta": hero.get("secondary_cta", ""),
            "summary": section(text, "Product Summary"),
            "inventory": bullets(section(text, "Bundle Inventory")),
            "inside": bullets(section(text, "What's Inside")),
            "why_it_works": h3_sections(section(text, "Why It Works")),
            "who_it_is_for": bullets(section(text, "Who It Is For")),
            "details": bullets(section(text, "Product Details")),
            "outcomes": bullets(section(text, "Outcomes")) or FALLBACK_OUTCOMES.get(slug, []),
        }
        records.append(record)

    OUT_JSON.write_text(json.dumps(records, indent=2), encoding="utf-8")

    lines = [
        "# Phase 1 Website Copy Handoff",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Use this as the source when enriching product pages in `data/site.js` or any future CMS/import format.",
        "",
    ]
    for record in records:
        lines += [
            f"## {record['h1'] or record['internal_slug']}",
            "",
            f"- Internal slug: `{record['internal_slug']}`",
            f"- Website title: {record['website_title'] or 'needs confirmed website product'}",
            f"- Website slug: `{record['website_slug']}`" if record["website_slug"] else "- Website slug: needs confirmation",
            f"- Payhip URL: {record['payhip_url'] or 'needs confirmation'}",
            f"- Subhead: {record['subhead']}",
            "",
            "### Summary",
            "",
            record["summary"],
            "",
            "### Inventory",
            "",
        ]
        lines.extend(f"- {item}" for item in record["inventory"])
        lines += ["", "### Outcomes", ""]
        lines.extend(f"- {item}" for item in record["outcomes"])
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)


if __name__ == "__main__":
    main()
