#!/usr/bin/env python3
"""Build a structured website-copy handoff for the next approved batch."""

from __future__ import annotations

import csv
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "content-elevated-product-os/internal"
MASTER = ROOT / "content-elevated-product-os/data/product-master.csv"
OUT_MD = ROOT / "content-elevated-product-os/internal/_global/next-batch-website-copy-handoff.md"
OUT_JSON = ROOT / "content-elevated-product-os/internal/_global/next-batch-website-copy-handoff.json"

NEXT_BATCH = [
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
]

WEBSITE_TITLE = {
    "barbers": "Barber Growth Bundle",
    "dog-walkers-and-pet-sitters": "Dog Walker Growth Bundle",
    "personal-trainers": "Personal Trainer Growth Bundle",
    "personal-chefs": "Personal Chef Growth Bundle",
    "nannies-and-childcare-professionals": "Nanny Professional Bundle",
    "florists": "Florist Growth Bundle",
    "event-planners": "Event Planner Growth Bundle",
    "videographers": "Videographer Growth Bundle",
    "public-speakers": "Public Speaker Growth Bundle",
    "personal-stylists": "Personal Stylist Growth Bundle",
    "life-and-business-coaches": "Life Coach & Business Coach Growth Bundle",
}

COPY_OVERRIDES = {
    "barbers": {
        "subhead": "A chair-filling content, booking, and client retention system for barbers and barbershops that want steadier demand.",
        "summary": "The Barbers Growth Bundle helps barbers turn attention into booked chairs. It combines content planning, AI prompts, client communication, intake assets, review requests, and brand direction so the shop can show up consistently, reduce no-shows, and build a client experience people recommend.",
        "outcomes": [
            "Fill the calendar with more consistent local demand.",
            "Improve booking, confirmation, review, and retention communication.",
            "Create sharper content without rebuilding every caption, offer, or client reply from scratch.",
        ],
    },
    "dog-walkers-and-pet-sitters": {
        "subhead": "A warm, polished content, client, brand, and repeat-booking system for local pet-care pros.",
        "summary": "The Dog Walkers & Pet Sitters Growth Bundle is built for trust-based local pet care. It brings together content planning, AI prompts, inquiry replies, care-update templates, client intake assets, review requests, referral prompts, and brand direction so the business can feel more organized before, during, and after every booking.",
        "outcomes": [
            "Create a warmer, more professional client experience from first inquiry to repeat booking.",
            "Improve inquiry replies, onboarding, care updates, follow-up, reviews, and referrals.",
            "Show up consistently with content that builds local trust and owner confidence.",
        ],
    },
    "personal-trainers": {
        "subhead": "A fitness growth system for trainers who want clearer content, stronger onboarding, and better client retention.",
        "summary": "The Personal Trainer Growth Bundle gives trainers a complete system for marketing, onboarding, follow-up, and client experience. It includes content calendars, AI prompts, email templates, brand direction, and onboarding scripts so trainers can sell their method with more clarity and keep clients moving.",
        "outcomes": [
            "Create trust-building fitness content faster.",
            "Improve lead follow-up, client onboarding, and retention touchpoints.",
            "Position coaching packages with more clarity and confidence.",
        ],
    },
    "personal-chefs": {
        "subhead": "A premium client experience and marketing system for personal chefs, private dining, and meal-prep services.",
        "summary": "The Personal Chef Growth Bundle helps culinary service providers look polished before the first call and stay organized after the booking. It includes proposal support, client questionnaires, content planning, email templates, brand direction, and AI prompts for premium client communication.",
        "outcomes": [
            "Convert inquiries with more polished proposals and follow-up.",
            "Clarify menus, preferences, and expectations before service begins.",
            "Build a refined brand presence for private dining and recurring clients.",
        ],
    },
    "nannies-and-childcare-professionals": {
        "subhead": "A trust-building professional toolkit for nannies and childcare providers who want stronger family inquiries and referrals.",
        "summary": "The Nanny Professional Bundle helps childcare professionals present their experience with clarity and confidence. It includes content guidance, AI prompts, family communication templates, professional toolkit assets, and brand direction designed for trust, safety, and long-term family relationships.",
        "outcomes": [
            "Present experience, rates, expectations, and availability more professionally.",
            "Improve family inquiries, onboarding, communication, and referral systems.",
            "Build trust before interviews and trial days.",
        ],
    },
    "florists": {
        "subhead": "A floral studio growth system for stronger inquiries, proposals, partnerships, and seasonal campaigns.",
        "summary": "The Florists Growth Bundle helps florists turn creative work into demand-building content and polished client communication. It includes a 90-day content calendar, AI playbook, email templates, brand kit, client questionnaire, and lead magnet for weddings, events, subscriptions, and local floral sales.",
        "outcomes": [
            "Create seasonal and event-driven content with less guesswork.",
            "Improve inquiry, questionnaire, proposal, and follow-up communication.",
            "Build a more premium floral brand across weddings, events, and everyday sales.",
        ],
    },
    "event-planners": {
        "subhead": "A planning business system for converting inquiries, managing expectations, and building referral-ready events.",
        "summary": "The Event Planners Growth Bundle gives planners a structured set of marketing and client experience assets. It includes content calendars, AI prompts, email templates, brand direction, vendor/timeline tools, and lead magnets to support premium inquiries and smoother event execution.",
        "outcomes": [
            "Convert inquiries with clearer positioning and follow-up.",
            "Create planning content that builds trust before the consultation.",
            "Strengthen vendor communication, timelines, and referral systems.",
        ],
    },
    "videographers": {
        "subhead": "A cinematic growth system for wedding, corporate, and commercial videographers who want better inquiries, clearer client communication, stronger content, and a more premium studio experience.",
        "summary": "The Videographers Growth Bundle turns the business side of video work into a clean operating system: inquiry responses, follow-ups, package presentation, pre-production questionnaires, delivery emails, review requests, vendor outreach, content calendars, AI prompts, and brand assets. It is built for creative video businesses that need polished systems without sounding generic.",
        "outcomes": [
            "Convert more inquiries into calls and bookings.",
            "Present packages with stronger language and clearer next steps.",
            "Improve pre-production, delivery, review, and referral communication.",
            "Build a repeatable content and partnership system for weddings, corporate work, and commercial projects.",
        ],
    },
    "public-speakers": {
        "subhead": "A speaker brand and booking system for paid talks, workshops, and authority-building content.",
        "summary": "The Public Speaker Growth Bundle helps speakers package their message, build authority, and pursue better opportunities. It includes content planning, AI prompts, email templates, brand direction, business development assets, and a speaker lead magnet.",
        "outcomes": [
            "Clarify speaker positioning, offers, and audience transformation.",
            "Create authority content and outreach assets faster.",
            "Support bookings, follow-up, and business development with stronger systems.",
        ],
    },
    "personal-stylists": {
        "subhead": "A boutique styling business system for consultations, wardrobe content, client follow-up, and premium personal-brand polish.",
        "summary": "The Personal Stylist Growth Bundle helps stylists turn taste into a clear client experience. It includes content calendars, AI prompts, email templates, brand direction, style questionnaires, and client communication assets so the business can attract better-fit clients, guide consultations, and follow up with polish.",
        "outcomes": [
            "Clarify the stylist's point of view and premium service positioning.",
            "Improve inquiry, consultation, questionnaire, post-session, and rebooking communication.",
            "Create refined wardrobe content and client touchpoints faster.",
        ],
    },
    "life-and-business-coaches": {
        "subhead": "A high-ticket coaching growth system for offer clarity, authority content, discovery calls, onboarding, and client experience.",
        "summary": "The Life Coach & Business Coach Growth Bundle helps coaches move from broad transformation language into a clear, bookable method. It includes content calendars, AI prompts, email templates, brand direction, discovery call assets, onboarding systems, and client experience tools so coaches can position their offer, nurture trust, and convert with more clarity.",
        "outcomes": [
            "Clarify coaching offers, audience tension, outcomes, and positioning.",
            "Create authority content, lead nurture, and discovery-call assets faster.",
            "Improve consult follow-up, onboarding, client communication, and premium delivery.",
        ],
    },
}


def site_slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower().replace("&", "and")).strip("-")


def load_master() -> dict[str, dict[str, str]]:
    with MASTER.open(newline="", encoding="utf-8") as f:
        return {row["slug"]: row for row in csv.DictReader(f)}


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
    master = load_master()
    records = []
    for slug in NEXT_BATCH:
        path = INTERNAL / slug / "website-product-copy.md"
        text = path.read_text(encoding="utf-8")
        hero = hero_fields(section(text, "Product Page Hero"))
        website_title = WEBSITE_TITLE[slug]
        override = COPY_OVERRIDES.get(slug, {})
        record = {
            "internal_slug": slug,
            "website_title": website_title,
            "website_slug": site_slug(website_title),
            "payhip_url": master[slug].get("payhip_url", ""),
            "h1": hero.get("h1", website_title),
            "eyebrow": hero.get("eyebrow", ""),
            "subhead": override.get("subhead", hero.get("subhead", "")),
            "primary_cta": hero.get("primary_cta", ""),
            "secondary_cta": hero.get("secondary_cta", ""),
            "summary": override.get("summary", section(text, "Product Summary")),
            "inventory": bullets(section(text, "Bundle Inventory")),
            "inside": bullets(section(text, "What's Inside")),
            "why_it_works": h3_sections(section(text, "Why It Works")),
            "who_it_is_for": bullets(section(text, "Who It Is For")),
            "details": bullets(section(text, "Product Details")),
            "outcomes": override.get("outcomes", bullets(section(text, "Outcomes"))),
        }
        records.append(record)

    OUT_JSON.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Next Batch Website Copy Handoff",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Use this as the source when enriching website product pages or any future CMS/import format.",
        "",
    ]
    for record in records:
        lines += [
            f"## {record['h1'] or record['website_title']}",
            "",
            f"- Internal slug: `{record['internal_slug']}`",
            f"- Website title: {record['website_title']}",
            f"- Website slug: `{record['website_slug']}`",
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
        if record["outcomes"]:
            lines.extend(f"- {item}" for item in record["outcomes"])
        else:
            lines.append("- Outcomes need final copy polish.")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)


if __name__ == "__main__":
    main()
