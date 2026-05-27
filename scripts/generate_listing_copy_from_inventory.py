from __future__ import annotations

import csv
import json
from pathlib import Path


OS_ROOT = Path("content-elevated-product-os")
INV_JSON = OS_ROOT / "data" / "bundle-inventory.json"
MASTER_CSV = OS_ROOT / "data" / "product-master.csv"
INTERNAL = OS_ROOT / "internal"


CATEGORY_OUTCOMES = {
    "Beauty": [
        "Create consistent content without starting from a blank page.",
        "Improve inquiry, booking, follow-up, review, and retention communication.",
        "Build a more polished beauty brand across every client touchpoint.",
    ],
    "Health & Wellness": [
        "Create trust-building educational content faster.",
        "Improve client communication before, during, and after appointments.",
        "Support retention, referrals, and repeat visits with clearer systems.",
    ],
    "Home Services": [
        "Follow up with leads and estimates more consistently.",
        "Create local authority content that keeps the business visible.",
        "Improve reviews, referrals, seasonal campaigns, and repeat service opportunities.",
    ],
    "Professional Services": [
        "Communicate expertise with more clarity and confidence.",
        "Improve consultation, follow-up, referral, and client nurture workflows.",
        "Create authority content without sounding generic or salesy.",
    ],
    "Creatives & Events": [
        "Turn creative work into polished content and booking assets.",
        "Improve inquiry, proposal, follow-up, and referral communication.",
        "Build a more premium client experience from discovery through delivery.",
    ],
    "Local Services": [
        "Create local trust and repeat-client systems.",
        "Improve inquiries, onboarding, communication, follow-up, reviews, and referrals.",
        "Look more polished without building every asset from scratch.",
    ],
    "E-Commerce": [
        "Improve listings, launch messaging, product content, and customer follow-up.",
        "Create repeatable systems for traffic, trust, reviews, and retention.",
        "Use AI to write better product and shop copy faster.",
    ],
    "Coaches & Educators": [
        "Create authority content and lead nurture faster.",
        "Improve discovery calls, onboarding, client communication, and offer messaging.",
        "Turn expertise into repeatable systems and polished digital assets.",
    ],
    "Hospitality": [
        "Create polished content, client experience assets, and booking communication.",
        "Improve inquiry, follow-up, referrals, and repeat-client workflows.",
        "Make the service feel premium from the first touchpoint.",
    ],
    "Personal Services": [
        "Create polished client-facing content and communication faster.",
        "Improve consultation, onboarding, follow-up, and referral workflows.",
        "Build a more premium personal brand experience.",
    ],
}


CATEGORY_AUDIENCE = {
    "Beauty": "beauty professionals and appointment-based service brands",
    "Health & Wellness": "health, wellness, and care-based practices",
    "Home Services": "local home service businesses",
    "Professional Services": "trust-based professional service businesses",
    "Creatives & Events": "creative professionals and event-based brands",
    "Local Services": "local service providers",
    "E-Commerce": "online sellers and product-based businesses",
    "Coaches & Educators": "coaches, consultants, and educators",
    "Hospitality": "hospitality and experience-based service businesses",
    "Personal Services": "personal service providers",
}

NICHE_LABELS = {
    "accountants-and-cpas": {
        "business": "accounting and CPA firms",
        "owners": "accounting firm owners, CPAs, bookkeepers, and advisory teams",
        "display": "Accountants & CPAs",
    },
    "dentists": {
        "business": "dental practices",
        "owners": "dentists, dental practice owners, and patient care teams",
        "display": "Dentists",
    },
    "hvac-contractors": {
        "business": "HVAC companies",
        "owners": "HVAC contractors, owners, technicians, and office teams",
        "display": "HVAC Contractors",
    },
    "etsy-sellers": {
        "business": "Etsy shops",
        "owners": "Etsy sellers, handmade shop owners, and digital product sellers",
        "display": "Etsy Sellers",
    },
    "hair-stylists": {
        "business": "salon and hairstylist businesses",
        "owners": "independent stylists, salon owners, booth renters, and suite stylists",
        "display": "Hair Stylists",
    },
    "med-spas": {
        "business": "med spas and aesthetic practices",
        "owners": "med spa owners, injectors, aestheticians, and aesthetic practitioners",
        "display": "Med Spas",
    },
    "nutritionists": {
        "business": "nutrition practices",
        "owners": "nutritionists, health coaches, and wellness practitioners",
        "display": "Nutritionists",
    },
    "wedding-photographers": {
        "business": "wedding photography brands",
        "owners": "wedding photographers and photography studio owners",
        "display": "Wedding Photographers",
    },
}


def labels(slug: str, product: dict) -> dict[str, str]:
    if slug in NICHE_LABELS:
        return NICHE_LABELS[slug]
    niche = product["niche"]
    lower = niche.lower()
    return {
        "business": f"{lower} businesses",
        "owners": f"{lower} owners, operators, and teams",
        "display": niche,
    }


def clean_title(title: str) -> str:
    title = title.replace("90 Day", "90-Day")
    title = title.replace("Ai ", "AI ")
    return title


def load_master() -> dict[str, dict[str, str]]:
    with MASTER_CSV.open(newline="", encoding="utf-8") as f:
        return {row["slug"]: row for row in csv.DictReader(f)}


def file_list(inv: dict) -> list[str]:
    lines = []
    for file in inv["files"]:
        if file["internal"]:
            continue
        title = clean_title(file["title"])
        detail = f"{file['pages']} pages"
        extras = []
        if file["prompts"]:
            extras.append(f"{file['prompts']} prompts")
        if file["templates"]:
            extras.append(f"{file['templates']} templates/scripts/systems")
        if extras:
            detail += f"; {', '.join(extras)}"
        lines.append(f"- {title} ({detail})")
    for sheet in inv["spreadsheet_files"]:
        lines.append(f"- {sheet} spreadsheet")
    return lines


def inventory_line(inv: dict) -> str:
    pieces = [
        f"{inv['customer_pdf_count']} polished PDF guides/workbooks",
        f"{inv['total_customer_pages']} customer-facing pages",
    ]
    if inv["spreadsheet_count"]:
        pieces.append(f"{inv['spreadsheet_count']} spreadsheet{'s' if inv['spreadsheet_count'] != 1 else ''}")
    if inv["prompt_count"]:
        pieces.append(f"{inv['prompt_count']} AI prompts")
    if inv["template_count_estimate"]:
        pieces.append(f"{inv['template_count_estimate']} templates/scripts/systems")
    return "Includes " + ", ".join(pieces) + "."


def payhip_copy(inv: dict, product: dict) -> str:
    category = product["category"]
    label = labels(product["slug"], product)
    audience = CATEGORY_AUDIENCE.get(category, "service businesses and creators")
    outcomes = CATEGORY_OUTCOMES.get(category, CATEGORY_OUTCOMES["Local Services"])
    tags = [
        product["niche"].lower().replace("&", "and"),
        f"{product['niche'].lower()} templates".replace("&", "and"),
        f"{product['niche'].lower()} marketing".replace("&", "and"),
        "ai prompts",
        "content calendar",
        "brand kit",
        "client templates",
        "digital download",
    ]
    return "\n".join(
        [
            f"# Payhip Listing Copy: {product['product_name']}",
            "",
            "## Product Title",
            "",
            product["product_name"],
            "",
            "## Short Subtitle",
            "",
            f"Premium AI-powered content, client, brand, and growth systems for {label['business']}.",
            "",
            "## Opening Hook",
            "",
            f"{label['display']} need more than random content ideas. They need a polished system for visibility, trust, follow-up, and conversion.",
            "",
            f"The {product['product_name']} gives you ready-to-use digital guides, prompts, templates, calendars, and client systems built for the way this niche actually sells and serves clients.",
            "",
            "## What You Get",
            "",
            inventory_line(inv),
            "",
            *file_list(inv),
            "",
            "## Exact Bundle Inventory",
            "",
            f"- Total customer-facing files: {inv['customer_pdf_count'] + inv['spreadsheet_count']}",
            f"- PDF guides/workbooks: {inv['customer_pdf_count']}",
            f"- Total customer-facing pages: {inv['total_customer_pages']}",
            f"- Spreadsheets: {inv['spreadsheet_count']}",
            f"- AI prompts detected: {inv['prompt_count']}",
            f"- Templates/scripts/systems detected: {inv['template_count_estimate']}",
            f"- Internal files excluded from buyer upload: {inv['internal_file_count']}",
            "",
            "## Built For",
            "",
            f"- {label['owners']}",
            f"- Solo providers and small teams in {product['category'].lower()}",
            "- Businesses that want better content, client communication, and follow-up systems",
            "- Operators who want polished digital systems without building everything from scratch",
            "",
            "## Outcomes",
            "",
            *(f"- {outcome}" for outcome in outcomes),
            "- Reduce blank-page work and make the business feel more organized.",
            "",
            "## Instant Access Note",
            "",
            "Delivered as digital files after checkout. Secure checkout and instant delivery are handled by Payhip.",
            "",
            "## Refund / Use Note",
            "",
            "Because this is a digital product, all sales are final unless otherwise stated in the store policy.",
            "",
            "## SEO",
            "",
            f"- SEO title: {product['product_name']} | AI Prompts, Content Calendar & Client Templates",
            f"- Meta description: Premium digital growth bundle for {label['business']} with AI prompts, content calendars, brand assets, client templates, and growth systems.",
            f"- Tags: {', '.join(tags)}",
            "",
        ]
    )


def website_copy(inv: dict, product: dict) -> str:
    category = product["category"]
    label = labels(product["slug"], product)
    audience = CATEGORY_AUDIENCE.get(category, "service businesses and creators")
    outcomes = CATEGORY_OUTCOMES.get(category, CATEGORY_OUTCOMES["Local Services"])
    return "\n".join(
        [
            f"# Website Product Copy: {product['product_name']}",
            "",
            "## Product Page Hero",
            "",
            "- Eyebrow: AI-Powered Growth Bundle",
            f"- H1: {product['product_name']}",
            f"- Subhead: A premium content, client, brand, and growth system built for {label['business']}.",
            "- Primary CTA: Get the Bundle",
            "- Secondary CTA: See What's Inside",
            "",
            "## Product Summary",
            "",
            f"The {product['product_name']} is a digital growth system for {label['business']}. It brings together content planning, AI prompts, client communication, brand direction, and practical workflow assets so the business can show up more consistently and convert with more polish.",
            "",
            "## Bundle Inventory",
            "",
            f"- {inv['customer_pdf_count']} polished PDF guides/workbooks",
            f"- {inv['total_customer_pages']} customer-facing pages",
            f"- {inv['spreadsheet_count']} spreadsheet{'s' if inv['spreadsheet_count'] != 1 else ''}",
            f"- {inv['prompt_count']} AI prompts detected",
            f"- {inv['template_count_estimate']} templates/scripts/systems detected",
            "",
            "## What's Inside",
            "",
            *file_list(inv),
            "",
            "## Why It Works",
            "",
            "### Content System",
            "",
            "The calendar and content assets give the business a clearer rhythm for visibility, education, trust, and conversion.",
            "",
            "### AI Playbook",
            "",
            "The prompts help turn ideas, client questions, offers, and expertise into usable copy faster.",
            "",
            "### Client Conversion Templates",
            "",
            "The communication assets help with inquiries, follow-up, onboarding, reviews, referrals, and repeat-client workflows.",
            "",
            "### Brand System",
            "",
            "The brand assets help the business look more polished, consistent, and premium across client touchpoints.",
            "",
            "## Who It Is For",
            "",
            f"- {label['owners']}",
            "- Solo providers and small teams",
            "- Businesses that want stronger systems without hiring an agency",
            "- Operators who want to use AI without sounding generic",
            "",
            "## Product Details",
            "",
            "- Format: Digital download",
            "- Delivery: Payhip secure checkout",
            "- Access: Instant after purchase",
            "- Includes: Polished digital guides, templates, calendars, prompts, and systems",
            "",
            "## Outcomes",
            "",
            *(f"- {outcome}" for outcome in outcomes),
            "",
        ]
    )


def upload_checklist(inv: dict, product: dict) -> str:
    lines = [
        f"# {product['product_name']} Upload Checklist",
        "",
        "## Customer-Facing Files",
        "",
    ]
    for file in inv["files"]:
        if not file["internal"]:
            lines.append(f"- [ ] `{file['file']}`")
    for sheet in inv["spreadsheet_files"]:
        lines.append(f"- [ ] `spreadsheets/{sheet}`")
    lines += ["", "## Internal / Review Before Upload", ""]
    internal = [f for f in inv["files"] if f["internal"]]
    if internal:
        for file in internal:
            lines.append(f"- [ ] `{file['file']}` — {'; '.join(file['internal_reasons'])}")
    else:
        lines.append("- No internal files detected by the automated scan.")
    lines += [
        "",
        "## Payhip",
        "",
        "- [ ] Replace old/basic bundle files with redesigned files.",
        "- [ ] Add finalized product description.",
        "- [ ] Add SEO title, meta description, and tags.",
        "- [ ] Confirm price.",
        "- [ ] Add final cover image.",
        "- [ ] Confirm checkout and instant delivery.",
        "",
        "## Website",
        "",
        "- [ ] Add product-page copy.",
        "- [ ] Add final Payhip checkout URL.",
        "- [ ] Confirm product image/mockup.",
        "- [ ] Test desktop and mobile product page.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    products = load_master()
    inventory = json.loads(INV_JSON.read_text(encoding="utf-8"))
    created = []
    skipped = []
    for inv in inventory:
        slug = inv["slug"]
        product = products[slug]
        folder = INTERNAL / slug
        folder.mkdir(parents=True, exist_ok=True)
        outputs = {
            "payhip-listing-copy.md": payhip_copy(inv, product),
            "website-product-copy.md": website_copy(inv, product),
            "upload-checklist.md": upload_checklist(inv, product),
        }
        preserve_custom = slug in {"hair-stylists", "med-spas"}
        for name, content in outputs.items():
            path = folder / name
            if path.exists() and preserve_custom:
                skipped.append(str(path))
                continue
            path.write_text(content, encoding="utf-8")
            created.append(str(path))
    print(f"Created {len(created)} files.")
    print(f"Skipped {len(skipped)} existing files.")


if __name__ == "__main__":
    main()
