#!/usr/bin/env python3
"""Create internal standalone-product maps from the bundle inventory."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
OUT_ROOT = ROOT / "content-elevated-product-os/internal"


TYPE_RULES = [
    ("content calendar", ["calendar", "90 day", "90-day"]),
    ("AI playbook", ["ai playbook", "playbook"]),
    ("prompt library", ["prompt library"]),
    ("brand kit", ["brand kit"]),
    ("email / communication templates", ["email", "communication", "sms", "templates"]),
    ("client system", ["client", "intake", "onboarding", "retention", "rebooking", "questionnaire", "booking", "patient", "treatment"]),
    ("calculator / spreadsheet guide", ["calculator", "profit", "pricing"]),
    ("lead magnet", ["lead magnet", "free", "lm-"]),
]


def product_type(file_name: str, title: str) -> str:
    haystack = f"{file_name} {title}".lower()
    for label, needles in TYPE_RULES:
        if any(needle in haystack for needle in needles):
            return label
    return "growth asset"


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = title.replace(" · ", " - ")
    return title


def short_promise(product_name: str, item_type: str) -> str:
    base = product_name.replace(" Growth Bundle", "")
    if item_type == "content calendar":
        return f"A ready-to-use content planning asset for {base.lower()} who want more consistent marketing."
    if item_type == "AI playbook":
        return f"A niche-ready AI workflow asset for {base.lower()} who want sharper offers, content, and client communication."
    if item_type == "prompt library":
        return f"A copy-and-paste prompt set for faster niche-specific content, sales, and client experience work."
    if item_type == "brand kit":
        return f"A brand clarity asset built to help {base.lower()} look more polished and consistent."
    if item_type == "email / communication templates":
        return f"A communication asset built to help {base.lower()} follow up, nurture, and convert more professionally."
    if item_type == "client system":
        return f"A client experience asset for improving intake, onboarding, follow-up, retention, and referrals."
    if item_type == "calculator / spreadsheet guide":
        return f"A planning asset for making pricing, profit, and business decisions easier to manage."
    if item_type == "lead magnet":
        return f"A quick-win download designed to introduce the buyer to the full {product_name}."
    return f"A focused digital asset from the {product_name}."


def website_card(title: str, item_type: str) -> str:
    if item_type == "content calendar":
        return "Plan a full season of content with niche-ready themes, prompts, and weekly direction."
    if item_type == "AI playbook":
        return "Use niche-trained AI prompts to create sharper content, offers, scripts, and client systems."
    if item_type == "brand kit":
        return "Clarify the brand, message, visual direction, and client-facing presentation."
    if item_type == "email / communication templates":
        return "Copy, customize, and send professional messages for leads, clients, and follow-ups."
    if item_type == "client system":
        return "Improve the client journey with ready-to-use intake, onboarding, and retention assets."
    if item_type == "calculator / spreadsheet guide":
        return "Use structured planning tools to make business decisions easier and more consistent."
    return f"A focused, ready-to-use digital asset: {title}."


def suggested_price(item_type: str, pages: int, has_sheet: bool) -> str:
    if has_sheet or item_type == "calculator / spreadsheet guide":
        return "$17-$37"
    if item_type in {"content calendar", "AI playbook", "brand kit"}:
        return "$19-$39" if pages >= 8 else "$15-$29"
    if item_type in {"prompt library", "email / communication templates", "client system"}:
        return "$15-$29"
    if item_type == "lead magnet":
        return "free-$9"
    return "$9-$27"


def main() -> None:
    products = json.loads(INVENTORY.read_text(encoding="utf-8"))
    for product in products:
        slug = product["slug"]
        out = OUT_ROOT / slug / "standalone-products.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f"# {product['product_name']} Standalone Product Map",
            "",
            f"Generated: {date.today().isoformat()}",
            "",
            "Use this as an internal planning file for future individual Payhip products and website cards.",
            "",
        ]
        customer_files = [f for f in product["files"] if not f.get("internal")]
        for index, item in enumerate(customer_files, start=1):
            title = clean_title(item["title"])
            item_type = product_type(item["file"], title)
            pages = item.get("pages", 0)
            prompts = item.get("prompts", 0)
            templates = item.get("templates", 0)
            upload_files = [item["file"]]
            has_sheet = False
            if "calculator" in item_type and product.get("spreadsheet_files"):
                upload_files += product["spreadsheet_files"]
                has_sheet = True

            lines += [
                f"## {index}. {title}",
                "",
                f"- Product type: {item_type}",
                f"- Target buyer: {product['product_name'].replace(' Growth Bundle', '')}",
                f"- Short promise: {short_promise(product['product_name'], item_type)}",
                "- What is included:",
                f"  - 1 PDF source file: `{item['file']}`",
                f"  - {pages} pages",
                f"  - {prompts} prompts detected" if prompts else "  - Prompt count not detected",
                f"  - {templates} templates/scripts/systems detected" if templates else "  - Template count not detected",
                f"- Best use case: {website_card(title, item_type)}",
                f"- Payhip short description: {website_card(title, item_type)}",
                f"- Payhip long description: {short_promise(product['product_name'], item_type)} This standalone asset is designed as an instant digital download and can also work as an entry point into the complete bundle.",
                f"- Website card description: {website_card(title, item_type)}",
                f"- SEO title: {title} | Content Elevated",
                f"- SEO meta description: {website_card(title, item_type)}",
                f"- Suggested price range: {suggested_price(item_type, pages, has_sheet)}",
                "- Upload files:",
            ]
            lines += [f"  - `{file}`" for file in upload_files]
            lines += [
                "- Notes / dependencies:",
                "  - Needs final PDF export and visual proof before standalone publishing.",
                "  - Needs standalone cover image.",
                "  - Consider an upsell link to the complete bundle.",
                "",
            ]

        if product.get("spreadsheet_files") and not any("calculator" in product_type(f["file"], f["title"]) for f in customer_files):
            lines += [
                "## Spreadsheet Standalone Opportunity",
                "",
                "- Product type: calculator / spreadsheet",
                f"- Spreadsheet files: {', '.join(f'`{s}`' for s in product['spreadsheet_files'])}",
                "- Suggested price range: $17-$37",
                "- Notes / dependencies:",
                "  - Needs workbook QA, formula checks, and standalone cover image before publishing.",
                "",
            ]
        out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated standalone maps for {len(products)} products.")


if __name__ == "__main__":
    main()
