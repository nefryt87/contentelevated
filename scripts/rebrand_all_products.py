from __future__ import annotations

import html
import os
import re
import shutil
from pathlib import Path

from pypdf import PdfReader
from create_all_niche_sample_documents import STYLE_BY_NICHE, css as sample_direction_css


SOURCE_ROOT = Path("/Users/tomasz/Documents/Content Elevated/Content Elevated Products")
WORKSPACE_ROOT = Path("/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for")
OUTPUT_ROOT = WORKSPACE_ROOT / "rebranded-products-sample-direction"

SKIP_DIR_NAMES = {"_SELLER MARKETING & INTERNAL DOCS", "Internal", "__MACOSX"}
SPREADSHEET_EXTENSIONS = {".xlsx", ".xls", ".csv", ".numbers"}
BEAUTY_NICHES = {
    "Aestheticians",
    "Bridal Hair & Makeup Artists",
    "Hair Stylists",
    "Lash Technicians",
    "Makeup Artists",
    "Med Spas",
    "Nail Technicians",
}
HOME_SERVICE_NICHES = {
    "Car Wash Businesses",
    "Electricians",
    "HVAC Contractors",
    "Landscapers",
    "Plumbers",
}
HEALTH_WELLNESS_NICHES = {
    "Chiropractors",
    "Dentists",
    "Massage Therapists",
    "Nutritionists",
    "Physical Therapists",
}
CREATIVE_STUDIO_NICHES = {
    "Interior Designers",
    "Tattoo Artists",
    "Videographers",
    "Wedding Photographers",
}
EVENT_ATELIER_NICHES = {
    "Event Planners",
    "Florists",
    "Party Planners",
    "Public Speakers",
}
CREATIVE_EVENT_COPY = {
    "Videographers": {
        "family": "studio",
        "kicker": "Cinematic demand · premium clients",
        "lead": "A cinematic growth system for turning portfolio work, inquiry follow-up, creative direction, and client communication into higher-value bookings.",
        "cells": [("01", "Frame the offer"), ("02", "Convert inquiries"), ("03", "Direct the story"), ("04", "Book premium projects")],
        "intro": "Start with the next client moment: inquiry reply, creative brief, proposal follow-up, production questionnaire, portfolio post, or referral ask.",
    },
    "Wedding Photographers": {
        "family": "studio",
        "kicker": "Editorial trust · booked calendars",
        "lead": "A refined wedding photography growth system for converting inquiries, presenting your style, guiding couples, and building referral-ready client experiences.",
        "cells": [("01", "Guide the inquiry"), ("02", "Show the style"), ("03", "Prepare the couple"), ("04", "Create referrals")],
        "intro": "Start with the next couple touchpoint: inquiry reply, consultation follow-up, wedding-day questionnaire, portfolio story, vendor referral, or review request.",
    },
    "Tattoo Artists": {
        "family": "studio",
        "kicker": "Studio demand · stronger bookings",
        "lead": "A bold studio growth system for turning flash, custom work, client intake, deposits, aftercare, and social demand into cleaner booking momentum.",
        "cells": [("01", "Shape demand"), ("02", "Qualify clients"), ("03", "Protect bookings"), ("04", "Build studio trust")],
        "intro": "Start with the next studio moment: booking inquiry, custom concept, deposit reminder, aftercare message, flash launch, or portfolio post.",
    },
    "Interior Designers": {
        "family": "interiors",
        "kicker": "Inspired spaces · premium projects",
        "lead": "A refined interior design business system for presenting your taste, guiding consultations, shaping client trust, and turning beautiful rooms into premium projects.",
        "cells": [("01", "Design point of view"), ("02", "Consultation flow"), ("03", "Project polish"), ("04", "Referral trust")],
        "intro": "Start with the next design-studio touchpoint: inquiry reply, discovery call, proposal follow-up, project onboarding, moodboard story, or referral partner outreach.",
    },
    "Florists": {
        "family": "atelier",
        "kicker": "Floral proposals · dream clients",
        "lead": "A romantic floral growth system for turning wedding inquiries, proposal polish, seasonal content, and vendor relationships into premium bookings.",
        "cells": [("01", "Shape the vision"), ("02", "Present beautifully"), ("03", "Nurture vendors"), ("04", "Book the season")],
        "intro": "Start with the next floral moment: wedding inquiry, proposal follow-up, moodboard support, vendor outreach, seasonal campaign, or client questionnaire.",
    },
    "Event Planners": {
        "family": "atelier",
        "kicker": "Polished plans · premium events",
        "lead": "A high-touch planning growth system for converting inquiries, managing vendor communication, presenting timelines, and creating a referral-worthy client experience.",
        "cells": [("01", "Clarify the vision"), ("02", "Guide the timeline"), ("03", "Coordinate vendors"), ("04", "Win referrals")],
        "intro": "Start with the next planning moment: inquiry reply, consultation follow-up, timeline prep, vendor communication, proposal polish, or post-event review.",
    },
    "Party Planners": {
        "family": "atelier",
        "kicker": "Joyful systems · booked celebrations",
        "lead": "A colorful event growth system for turning party inquiries, seasonal packages, client communication, and planning assets into more consistent bookings.",
        "cells": [("01", "Package the party"), ("02", "Guide the client"), ("03", "Plan with ease"), ("04", "Create repeat demand")],
        "intro": "Start with the next celebration moment: inquiry reply, theme package, planning checklist, vendor message, seasonal promo, or follow-up after the event.",
    },
    "Public Speakers": {
        "family": "speaker",
        "kicker": "Speak · inspire · lead",
        "lead": "A confident speaker brand system for clarifying your message, attracting event opportunities, packaging your authority, and turning your voice into lasting impact.",
        "cells": [("01", "Clarify the message"), ("02", "Package the talk"), ("03", "Pitch the room"), ("04", "Build authority")],
        "intro": "Start with the next stage-building touchpoint: speaker one-sheet, event pitch, organizer follow-up, talk description, authority post, or lead magnet.",
    },
}
HEALTH_WELLNESS_COPY = {
    "Chiropractors": {
        "kicker": "Alignment · retention · patient trust",
        "lead": "A calm, credible chiropractic growth system for patient education, reactivation, care-plan follow-up, reviews, and retention touchpoints.",
        "cells": [
            ("01", "Clarify care plans"),
            ("02", "Reduce no-shows"),
            ("03", "Reactivate patients"),
            ("04", "Build referral trust"),
        ],
        "intro": "Start with the next patient moment: new-patient inquiry, care-plan education, post-visit follow-up, reactivation, review request, or referral touchpoint.",
    },
    "Dentists": {
        "kicker": "Healthy smiles · confident care",
        "lead": "A clean, modern dental growth system for improving patient flow, follow-up, treatment communication, reviews, and trust-building content.",
        "cells": [
            ("01", "Improve patient flow"),
            ("02", "Educate with clarity"),
            ("03", "Strengthen reviews"),
            ("04", "Build lasting trust"),
        ],
        "intro": "Start with the next dental moment: new-patient inquiry, treatment explanation, hygiene recall, post-visit follow-up, review request, or case acceptance support.",
    },
    "Massage Therapists": {
        "kicker": "Calm retention · repeat bookings",
        "lead": "A grounded massage-practice growth system for nurturing repeat clients, explaining services clearly, selling memberships, and creating a calmer client experience.",
        "cells": [
            ("01", "Book repeat visits"),
            ("02", "Explain the benefits"),
            ("03", "Nurture memberships"),
            ("04", "Create calm trust"),
        ],
        "intro": "Start with the next client moment: new inquiry, post-session care, membership invitation, rebooking nudge, referral ask, or service education touchpoint.",
    },
    "Nutritionists": {
        "kicker": "Nourish · educate · lasting habits",
        "lead": "A fresh, whole-food inspired nutrition growth system for client education, meal-plan support, habit change, check-ins, and warm follow-up.",
        "cells": [
            ("01", "Personalize care"),
            ("02", "Support habits"),
            ("03", "Educate clearly"),
            ("04", "Nourish momentum"),
        ],
        "intro": "Start with the next client moment: consultation inquiry, onboarding, check-in, meal-plan guidance, recipe support, education post, progress celebration, or retention email.",
    },
    "Physical Therapists": {
        "kicker": "Recovery · education · follow-through",
        "lead": "A clear physical-therapy growth system for patient education, home-exercise support, discharge follow-up, retention, reviews, and referral-ready communication.",
        "cells": [
            ("01", "Support recovery"),
            ("02", "Improve follow-through"),
            ("03", "Guide discharge"),
            ("04", "Grow trusted referrals"),
        ],
        "intro": "Start with the next patient moment: new evaluation, plan-of-care education, home-exercise follow-up, discharge support, review request, or referral touchpoint.",
    },
}
PROFESSIONAL_SERVICE_NICHES = {
    "Accountants & CPAs",
    "Attorneys",
    "broker_toolkit",
    "Financial Advisors",
    "Insurance Agents",
    "Mortgage Brokers",
}

BESPOKE_NICHES = {
    "Barbers",
    "Dog Walkers & Pet Sitters",
    "Etsy Sellers",
    "Life & Business Coaches",
    "Nannies & Childcare Professionals",
    "Personal Chefs",
    "Personal Stylists",
    "Personal Trainers",
}

BESPOKE_COPY = {
    "Barbers": {
        "family": "barber",
        "kicker": "Chair demand · shop authority",
        "lead": "A sharp barbershop growth system for turning local attention, client follow-up, content, and rebooking prompts into a fuller chair and stronger shop presence.",
        "cells": [("01", "Fill the chair"), ("02", "Protect bookings"), ("03", "Build local trust"), ("04", "Create repeat visits")],
        "intro": "Start with the next chair-building moment: booking inquiry, rebooking text, review ask, referral prompt, local post, or client intake message.",
    },
    "Dog Walkers & Pet Sitters": {
        "family": "petcare",
        "kicker": "Neighborhood trust · repeat care",
        "lead": "A warm local pet-care growth system for building trust with owners, improving inquiry follow-up, communicating clearly, and turning happy clients into repeat bookings.",
        "cells": [("01", "Earn trust"), ("02", "Book recurring care"), ("03", "Communicate clearly"), ("04", "Grow referrals")],
        "intro": "Start with the next owner touchpoint: new inquiry, meet-and-greet follow-up, schedule confirmation, care update, review request, or referral ask.",
    },
    "Etsy Sellers": {
        "family": "etsy",
        "kicker": "Maker shop · polished listings",
        "lead": "A modern shop-growth system for improving listings, product stories, launch content, customer messages, reviews, and repeat-buyer momentum.",
        "cells": [("01", "Polish listings"), ("02", "Launch products"), ("03", "Convert shoppers"), ("04", "Grow repeat buyers")],
        "intro": "Start with the next shop moment: listing rewrite, product launch, customer reply, review request, seasonal promo, or retention email.",
    },
    "Life & Business Coaches": {
        "family": "coach",
        "kicker": "Clarity · authority · client trust",
        "lead": "A polished coaching growth system for clarifying your offer, nurturing leads, packaging your framework, and turning expertise into better client conversations.",
        "cells": [("01", "Clarify the offer"), ("02", "Nurture leads"), ("03", "Guide discovery"), ("04", "Convert with trust")],
        "intro": "Start with the next coaching touchpoint: discovery call follow-up, lead magnet, email nurture, framework post, client onboarding, or offer refinement.",
    },
    "Nannies & Childcare Professionals": {
        "family": "childcare",
        "kicker": "Gentle care · family confidence",
        "lead": "A bright, reassuring childcare growth system for communicating reliability, building parent confidence, improving inquiry flow, and presenting a polished care brand.",
        "cells": [("01", "Build family trust"), ("02", "Guide inquiries"), ("03", "Communicate care"), ("04", "Book confidently")],
        "intro": "Start with the next family touchpoint: inquiry reply, parent update, onboarding questionnaire, availability message, testimonial request, or care introduction.",
    },
    "Personal Chefs": {
        "family": "chef",
        "kicker": "Private dining · premium hospitality",
        "lead": "A culinary growth system for presenting menus, guiding client inquiries, creating polished hospitality touchpoints, and turning private dining into repeat bookings.",
        "cells": [("01", "Present the menu"), ("02", "Guide the inquiry"), ("03", "Elevate service"), ("04", "Book repeat tables")],
        "intro": "Start with the next dining touchpoint: menu inquiry, consultation reply, event follow-up, dietary questionnaire, seasonal offer, or referral ask.",
    },
    "Personal Stylists": {
        "family": "stylist",
        "kicker": "Wardrobe clarity · editorial confidence",
        "lead": "A fashion-forward styling growth system for shaping your offer, guiding client consultations, presenting taste, and turning style expertise into premium bookings.",
        "cells": [("01", "Define the style"), ("02", "Guide the consult"), ("03", "Present taste"), ("04", "Book premium clients")],
        "intro": "Start with the next style touchpoint: inquiry reply, style questionnaire, wardrobe audit follow-up, package pitch, seasonal content, or referral request.",
    },
    "Personal Trainers": {
        "family": "trainer",
        "kicker": "Performance · discipline · momentum",
        "lead": "A kinetic fitness growth system for improving onboarding, client accountability, content, retention, sales follow-up, and the trust needed to book more training.",
        "cells": [("01", "Book assessments"), ("02", "Build accountability"), ("03", "Show progress"), ("04", "Retain clients")],
        "intro": "Start with the next training touchpoint: assessment inquiry, onboarding script, check-in message, transformation post, reactivation, or referral ask.",
    },
}


SECTION_RE = re.compile(
    r"^(SECTION|TEMPLATE|PROMPT|CHAPTER|WEEK|MONTH|DAY|BONUS|WHY|HOW TO|INTRODUCTION|"
    r"CONCLUSION|SUBJECT|EMAIL|SCRIPT|CHECKLIST|PALETTE|TYPOGRAPHY|CANVA|REFERRAL|"
    r"ADVISORY|TAX|CLIENT|NEW CLIENT|YEAR-END|IRS|PHONE|SOCIAL|CONTENT|BRAND|INTAKE|"
    r"BOOKING|SYSTEM|PARTNERSHIP|OFFER|FOLLOW-UP|RETENTION|REACTIVATION|WORKSHEET|"
    r"QUESTIONNAIRE|PRICING|CALCULATOR|PLAN|PLAYBOOK|PROMPT)\b",
    re.I,
)


THEMES = {
    "beauty": {
        "accent": "#c78f8d",
        "accent2": "#f0c6b6",
        "paper": "#fff8f5",
        "tint": "#f7ece8",
        "ink": "#171214",
        "muted": "#736366",
        "dark": "#201619",
        "label": "Appointment growth system",
        "tone": "soft studio polish",
    },
    "barber": {
        "accent": "#c4954f",
        "accent2": "#efcc8d",
        "paper": "#0d0a08",
        "tint": "#16100c",
        "ink": "#f8f1e7",
        "muted": "#c5b7a6",
        "dark": "#070504",
        "label": "Chair growth system",
        "tone": "dark shop authority",
    },
    "tattoo": {
        "accent": "#b37a6c",
        "accent2": "#d6a065",
        "paper": "#0b0909",
        "tint": "#161111",
        "ink": "#f8f0ea",
        "muted": "#c7b4aa",
        "dark": "#060505",
        "label": "Studio demand system",
        "tone": "portfolio-led conversion",
    },
    "professional": {
        "accent": "#6e8892",
        "accent2": "#b6c6c4",
        "paper": "#faf8f1",
        "tint": "#ece9df",
        "ink": "#14181b",
        "muted": "#636a6e",
        "dark": "#192127",
        "label": "Trust operating system",
        "tone": "advisory-grade clarity",
    },
    "trades": {
        "accent": "#55bde8",
        "accent2": "#ff9b5c",
        "paper": "#f4faff",
        "tint": "#e8f1f7",
        "ink": "#081421",
        "muted": "#536475",
        "dark": "#0d1b29",
        "label": "Local service system",
        "tone": "field-ready precision",
    },
    "wellness": {
        "accent": "#789881",
        "accent2": "#c5d3b8",
        "paper": "#fbfcf6",
        "tint": "#edf4ea",
        "ink": "#151d18",
        "muted": "#617066",
        "dark": "#17231b",
        "label": "Care growth system",
        "tone": "calm clinical trust",
    },
    "creative": {
        "accent": "#9b7d8d",
        "accent2": "#d4b989",
        "paper": "#fff8f1",
        "tint": "#f0e7de",
        "ink": "#171211",
        "muted": "#71635d",
        "dark": "#1c1615",
        "label": "Creative demand system",
        "tone": "editorial business polish",
    },
    "commerce": {
        "accent": "#3e9a9f",
        "accent2": "#ff946d",
        "paper": "#fbfdfc",
        "tint": "#edf5f4",
        "ink": "#111618",
        "muted": "#5c6668",
        "dark": "#11191c",
        "label": "Shop growth system",
        "tone": "commerce-ready momentum",
    },
    "hospitality": {
        "accent": "#9b7657",
        "accent2": "#d6b888",
        "paper": "#fff8ef",
        "tint": "#f2e8dc",
        "ink": "#18130f",
        "muted": "#6c6256",
        "dark": "#211810",
        "label": "Client experience system",
        "tone": "warm service polish",
    },
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower().replace("&", "and")).strip("-")


def title_case(value: str) -> str:
    titled = (
        value.title()
        .replace("Ai", "AI")
        .replace("Cpa", "CPA")
        .replace("Cpas", "CPAs")
        .replace("Hvac", "HVAC")
        .replace("Seo", "SEO")
        .replace("Hmua", "HMUA")
    )
    return re.sub(r"'([A-Z])", lambda match: "'" + match.group(1).lower(), titled)


def theme_for(niche: str) -> dict[str, str]:
    if niche == "Chiropractors":
        return {
            "headline": "5 AI Prompts for Patient Retention",
            "mood": "Wellness clinic trust",
            "accent": "#718d78",
            "accent2": "#dce9d8",
            "paper": "#fbfdf8",
            "dark": "#18231c",
            "layout": "protocol",
            "tag": "Chiro",
        }
    if niche == "Dentists":
        return {
            "headline": "5 AI Prompts for a Better Patient Flow",
            "mood": "Clean clinical confidence",
            "accent": "#6aaec7",
            "accent2": "#e4f5fb",
            "paper": "#fbfdff",
            "dark": "#102432",
            "layout": "protocol",
            "tag": "Dental",
        }
    if niche == "Massage Therapists":
        return {
            "headline": "5 AI Prompts for Repeat Massage Clients",
            "mood": "Calm retention wellness",
            "accent": "#7f9173",
            "accent2": "#e7e4d3",
            "paper": "#fcfbf4",
            "dark": "#20251b",
            "layout": "protocol",
            "tag": "Massage",
        }
    if niche == "Nutritionists":
        return {
            "headline": "5 AI Prompts for Better Client Plans",
            "mood": "Fresh wellness clarity",
            "accent": "#55773f",
            "accent2": "#edf1df",
            "paper": "#fffdf5",
            "dark": "#223119",
            "layout": "protocol",
            "tag": "Nutrition",
        }
    if niche == "Physical Therapists":
        return {
            "headline": "5 AI Prompts for Patient Follow-Up",
            "mood": "Rehab clarity and trust",
            "accent": "#5f9995",
            "accent2": "#d7ece7",
            "paper": "#fbfdfb",
            "dark": "#172524",
            "layout": "protocol",
            "tag": "PT",
        }
    creative_themes = {
        "Videographers": ("#5f7ee6", "#1ad6c7", "#070910", "#f5f6fb", "Film"),
        "Wedding Photographers": ("#b99a78", "#e8d6c6", "#100d0c", "#fffaf6", "Wedding"),
        "Tattoo Artists": ("#c16b5a", "#d7a15c", "#0b0808", "#fff7f2", "Ink"),
        "Interior Designers": ("#1f4f49", "#d9c7ae", "#183734", "#fbf7ef", "Interiors"),
        "Florists": ("#8b9c5f", "#e6c6cf", "#211b18", "#fff9f2", "Floral"),
        "Event Planners": ("#a98b68", "#ead9bf", "#1f1915", "#fff8ef", "Event"),
        "Party Planners": ("#b56fa5", "#f0c76d", "#1d1520", "#fff8fb", "Party"),
        "Public Speakers": ("#0d2f5b", "#d39a36", "#071426", "#f8fbff", "Speaker"),
    }
    if niche in creative_themes:
        accent, accent2, dark, paper, tag = creative_themes[niche]
        return {
            "headline": f"{niche} Growth System",
            "mood": "Premium creative growth system",
            "accent": accent,
            "accent2": accent2,
            "paper": paper,
            "dark": dark,
            "layout": "editorial",
            "tag": tag,
        }
    if niche in STYLE_BY_NICHE:
        return STYLE_BY_NICHE[niche]
    return {
        "headline": f"{niche} Growth System",
        "mood": "Premium business operating system",
        "accent": "#5f7f86",
        "accent2": "#a8bab5",
        "paper": "#fbfaf4",
        "dark": "#161b1f",
        "layout": "ledger",
        "tag": "Growth",
    }


def is_dark(theme: dict[str, str]) -> bool:
    return theme["paper"].startswith("#0")


def is_beauty_niche(niche: str) -> bool:
    return niche in BEAUTY_NICHES


def is_home_service_niche(niche: str) -> bool:
    return niche in HOME_SERVICE_NICHES


def is_health_wellness_niche(niche: str) -> bool:
    return niche in HEALTH_WELLNESS_NICHES


def is_creative_event_niche(niche: str) -> bool:
    return niche in CREATIVE_STUDIO_NICHES or niche in EVENT_ATELIER_NICHES


def is_professional_service_niche(niche: str) -> bool:
    return niche in PROFESSIONAL_SERVICE_NICHES or "Broker" in niche or "Advisor" in niche


def is_bespoke_niche(niche: str) -> bool:
    return niche in BESPOKE_NICHES


def css(theme: dict[str, str]) -> str:
    return sample_direction_css(theme) + f"""
.direction-page .section-head {{ margin-top: .18in; }}
.direction-page .prompt-grid {{ margin-top: .32in; }}
.direction-page .prompt-card {{ grid-template-columns: .44in 1fr; }}
.direction-page .prompt-card p {{ font-size: 9.3px; }}
.direction-page .content-stack {{ position: relative; z-index: 3; margin-top: .32in; display: grid; gap: 13px; }}
.direction-page .content-stack .prompt-card h3 {{ font-size: 15px; }}
.direction-page .content-stack .prompt-card .eyebrow {{ font-size: 7.5px; }}
.direction-page .section-label {{ margin: 10px 0 4px; color: {theme['accent']}; font-size: 8px; font-weight: 950; letter-spacing: .2em; text-transform: uppercase; }}
.direction-page .plain-copy {{ margin: 0; color: rgba(248,243,233,.72); font-size: 9.5px; line-height: 1.48; }}
.direction-page .template-line {{ border-left: 1px solid color-mix(in srgb,{theme['accent']} 56%,transparent); padding-left: 10px; background: linear-gradient(90deg,color-mix(in srgb,{theme['accent']} 10%,transparent),transparent 70%); }}
"""


def beauty_css(theme: dict[str, str]) -> str:
    accent = theme["accent"]
    accent2 = theme["accent2"]
    dark = theme["dark"]
    paper = theme["paper"]

    return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --ink:#17110f;
  --soft-ink:#5d504b;
  --muted:#8e7a72;
  --paper:{paper};
  --paper-2:#f6e8de;
  --blush:{accent2};
  --rose:{accent};
  --cream:#fffaf4;
  --dark:{dark};
  --line:rgba(91,67,58,.16);
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#e8d7ca;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;overflow:hidden;page-break-after:always;background:radial-gradient(circle at 14% 8%,color-mix(in srgb,var(--blush) 34%,transparent),transparent 2.2in),radial-gradient(circle at 90% 12%,color-mix(in srgb,var(--rose) 18%,transparent),transparent 2.5in),linear-gradient(135deg,var(--paper),var(--cream) 52%,var(--paper-2));padding:.62in}}
.page::before{{content:"";position:absolute;inset:.28in;border:1px solid rgba(91,67,58,.12);border-radius:28px;pointer-events:none}}
.page::after{{content:"";position:absolute;right:-1.1in;top:-.3in;width:3.2in;height:9.8in;background:linear-gradient(180deg,rgba(23,17,15,.06),transparent 58%),radial-gradient(ellipse at center,color-mix(in srgb,var(--blush) 26%,transparent),transparent 64%);transform:rotate(-10deg);border-radius:999px;pointer-events:none}}
.brand{{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:flex-start}}
.wordmark{{font-size:12px;font-weight:900;letter-spacing:.2em;text-transform:uppercase}}
.wordmark small{{display:block;margin-top:8px;color:var(--rose);font-size:9px;font-weight:700;letter-spacing:.18em}}
.badge{{border:1px solid color-mix(in srgb,var(--rose) 26%,transparent);border-radius:999px;padding:10px 14px;color:var(--rose);font-size:10px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;background:rgba(255,250,244,.64)}}
.kicker{{position:relative;z-index:2;display:flex;align-items:center;gap:12px;color:var(--rose);font-size:10px;font-weight:800;letter-spacing:.22em;text-transform:uppercase}}
.kicker::before{{content:"";width:42px;height:1px;background:var(--rose)}}
h1,h2,h3{{position:relative;z-index:2;margin:0;font-family:"Didot","Bodoni 72","Times New Roman",serif;font-weight:400;letter-spacing:-.045em}}
h1{{max-width:5.85in;margin-top:.82in;font-size:66px;line-height:.93}}
h2{{font-size:42px;line-height:.96}}
h3{{font-size:24px;line-height:1}}
h1 span,h2 span,h1 em,h2 em{{color:var(--rose);font-style:italic}}
p{{position:relative;z-index:2;margin:0;color:var(--soft-ink);font-size:12.5px;line-height:1.62}}
.lead{{max-width:4.85in;margin-top:.28in;font-size:16px;line-height:1.55}}
.cover-meta{{position:absolute;left:.62in;right:.62in;bottom:.74in;z-index:2;display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.meta-item{{padding:18px 16px;border-left:1px solid var(--line)}}
.meta-item:first-child{{border-left:0;padding-left:0}}
.meta-item strong{{display:block;font-family:"Didot","Bodoni 72","Times New Roman",serif;color:var(--rose);font-size:28px;font-weight:400;line-height:1}}
.meta-item span{{display:block;margin-top:8px;color:var(--muted);font-size:9px;font-weight:800;letter-spacing:.16em;line-height:1.45;text-transform:uppercase}}
.footer{{position:absolute;left:.62in;right:.62in;bottom:.34in;z-index:2;display:flex;justify-content:space-between;color:rgba(93,80,75,.72);font-size:8px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}}
.intro-grid{{position:relative;z-index:2;display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:.42in}}
.panel{{position:relative;z-index:2;border:1px solid var(--line);border-radius:22px;background:rgba(255,250,244,.66);padding:22px;box-shadow:0 18px 52px rgba(95,61,51,.08)}}
.panel.dark{{background:rgba(255,250,244,.66);color:var(--ink)}}
.panel.dark p{{color:var(--soft-ink)}}
.panel.dark .label{{color:var(--rose)}}
.label{{margin-bottom:12px;color:var(--rose);font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}}
.rule{{position:relative;z-index:2;height:1px;margin:28px 0;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--rose) 38%,transparent),transparent)}}
.template{{position:relative;z-index:2;display:grid;grid-template-columns:.78in 1fr;gap:18px;margin-top:22px;padding-top:22px;border-top:1px solid var(--line)}}
.template:first-of-type{{border-top:0;padding-top:0}}
.num{{width:.58in;height:.58in;display:grid;place-items:center;border:1px solid color-mix(in srgb,var(--rose) 24%,transparent);border-radius:50%;color:var(--rose);font-family:"Didot","Bodoni 72","Times New Roman",serif;font-size:22px;background:rgba(255,250,244,.66)}}
.when{{margin:10px 0 14px;color:var(--muted);font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}}
.script{{border-radius:18px;background:linear-gradient(135deg,rgba(255,255,255,.72),rgba(255,250,244,.82)),radial-gradient(circle at 8% 12%,color-mix(in srgb,var(--blush) 18%,transparent),transparent 45%);border:1px solid color-mix(in srgb,var(--rose) 14%,transparent);padding:18px;color:#2a201d;font-size:13px;line-height:1.55}}
.tip{{margin-top:12px;border-left:3px solid var(--rose);padding-left:12px;color:var(--soft-ink);font-size:11px;line-height:1.5}}
.cta-page{{background:radial-gradient(circle at 18% 18%,color-mix(in srgb,var(--blush) 22%,transparent),transparent 2.6in),linear-gradient(135deg,#1b1412,color-mix(in srgb,var(--rose) 72%,#251413));color:#fff7ef}}
.cta-page::before{{border-color:rgba(255,250,244,.14)}}
.cta-page p,.cta-page .footer,.cta-page .wordmark small{{color:rgba(255,247,239,.74)}}
.cta-page h2,.cta-page .wordmark{{color:#fff7ef}}
.cta-button{{display:inline-block;margin-top:28px;border-radius:999px;background:#fff7ef;color:color-mix(in srgb,var(--rose) 78%,#2a1716);padding:16px 22px;font-size:10px;font-weight:900;letter-spacing:.16em;text-transform:uppercase}}
@media print{{body{{background:white}}.book{{width:auto;margin:0}}}}
"""


def home_service_css(theme: dict[str, str]) -> str:
    accent = theme["accent"]
    accent2 = theme["accent2"]
    dark = theme["dark"]
    return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --ink:#f5f8fb;
  --muted:#9fb1c2;
  --quiet:#647688;
  --paper:#07111b;
  --panel:#0b1825;
  --panel-2:#101f2f;
  --line:rgba(157,206,255,.18);
  --accent:{accent};
  --accent-2:{accent2};
  --orange:#ff9b5c;
  --dark:{dark};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#0a1017;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;overflow:hidden;page-break-after:always;padding:.54in;background:linear-gradient(135deg,#050b12 0%,#0b1724 58%,#08131f 100%)}}
.page::before{{content:"";position:absolute;inset:0;background:
  radial-gradient(circle at 76% 18%,color-mix(in srgb,var(--accent) 20%,transparent),transparent 2.2in),
  radial-gradient(circle at 15% 92%,rgba(255,155,92,.12),transparent 2.5in),
  linear-gradient(135deg,rgba(255,255,255,.035),transparent 44%);
  pointer-events:none}}
.page::after{{content:"";position:absolute;right:-1.15in;top:.75in;width:3.8in;height:8.2in;border:1px solid rgba(157,206,255,.1);background:linear-gradient(180deg,rgba(255,255,255,.03),transparent 65%);transform:skewX(-9deg);opacity:.42;pointer-events:none}}
.brand{{position:relative;z-index:3;display:flex;align-items:flex-start;justify-content:space-between;color:rgba(245,248,251,.82);font-size:9px;font-weight:900;letter-spacing:.24em;text-transform:uppercase}}
.brand small{{display:block;margin-top:7px;color:var(--accent);font-size:8px;letter-spacing:.2em}}
.badge{{border:1px solid rgba(157,206,255,.18);border-radius:999px;background:rgba(255,255,255,.045);padding:10px 13px;color:#cfe9ff;font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}}
.cover-kicker{{position:relative;z-index:3;margin-top:.76in;color:var(--accent);font-size:10px;font-weight:950;letter-spacing:.28em;text-transform:uppercase}}
h1,h2,h3{{position:relative;z-index:3;margin:0}}
h1{{max-width:6.6in;margin-top:.16in;font-family:"Arial Narrow","Helvetica Neue",Arial,sans-serif;font-size:72px;line-height:.86;font-weight:950;letter-spacing:-.055em;text-transform:uppercase}}
h1 em{{font-style:normal;color:#d9f3ff;text-shadow:0 0 28px color-mix(in srgb,var(--accent) 35%,transparent)}}
.lead{{position:relative;z-index:3;max-width:5.55in;margin-top:.28in;color:rgba(239,246,252,.9);font-size:16px;line-height:1.58}}
.system-strip{{position:absolute;z-index:3;left:.54in;right:.54in;bottom:.86in;display:grid;grid-template-columns:1.1fr .9fr .9fr .9fr;border:1px solid rgba(157,206,255,.24);background:rgba(5,12,20,.82);box-shadow:0 22px 70px rgba(0,0,0,.22)}}
.system-cell{{min-height:.98in;padding:17px 15px;border-left:1px solid var(--line)}}
.system-cell:first-child{{border-left:0}}
.system-cell b{{display:block;color:#f5f8fb;font-size:20px;line-height:1;font-weight:950;letter-spacing:-.02em}}
.system-cell span{{display:block;margin-top:10px;color:#c6d5e4;font-size:8.4px;font-weight:850;letter-spacing:.14em;line-height:1.55;text-transform:uppercase}}
.footer{{position:absolute;z-index:3;left:.54in;right:.54in;bottom:.31in;display:flex;justify-content:space-between;color:rgba(159,177,194,.72);font-size:8px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}}
.work{{background:#f7fafc;color:#0b1420}}
.work::before{{background:
  radial-gradient(circle at 85% 8%,color-mix(in srgb,var(--accent) 10%,transparent),transparent 2.4in),
  linear-gradient(135deg,rgba(255,255,255,.92),rgba(231,239,246,.62));
  background-size:auto,auto}}
.work::after{{display:none}}
.section-head{{position:relative;z-index:3;display:grid;grid-template-columns:.95fr 1.05fr;gap:.36in;align-items:end;margin-top:.25in;padding-bottom:.22in;border-bottom:1px solid rgba(16,31,47,.14)}}
.eyebrow{{margin:0 0 10px;color:var(--accent);font-size:8px;font-weight:950;letter-spacing:.23em;text-transform:uppercase}}
h2{{font-family:"Arial Narrow","Helvetica Neue",Arial,sans-serif;font-size:39px;line-height:.94;font-weight:950;letter-spacing:-.04em;text-transform:uppercase;color:#0b1420}}
.intro{{margin:0;color:#314255;font-size:12.2px;line-height:1.6}}
.command-grid{{position:relative;z-index:3;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:.34in}}
.command-card{{position:relative;min-height:1.82in;border:1px solid rgba(16,31,47,.12);background:linear-gradient(145deg,#fff,rgba(239,245,249,.9));padding:18px;box-shadow:0 14px 34px rgba(7,17,27,.055)}}
.command-card::before{{content:"";position:absolute;left:0;top:0;width:4px;height:100%;background:linear-gradient(180deg,var(--accent),var(--orange))}}
.num{{display:inline-grid;width:.42in;height:.42in;place-items:center;margin-bottom:12px;border:1px solid color-mix(in srgb,var(--accent) 42%,transparent);border-radius:6px;color:var(--accent);font-size:12px;font-weight:950}}
h3{{font-size:15px;line-height:1.12;color:#0b1420;font-weight:850;letter-spacing:-.01em}}
.command-card p,.data-card p{{margin:9px 0 0;color:#26384a;font-size:10.6px;line-height:1.55}}
.content-stack{{position:relative;z-index:3;display:grid;gap:12px;margin-top:.31in}}
.data-card{{display:grid;grid-template-columns:.48in 1fr;gap:15px;padding:17px 18px;border:1px solid rgba(16,31,47,.12);background:linear-gradient(135deg,#fff,rgba(240,246,250,.92));box-shadow:0 12px 30px rgba(7,17,27,.055)}}
.data-card .eyebrow{{margin-bottom:7px;color:#52687d;font-size:7.5px;letter-spacing:.18em}}
.data-card h3{{font-size:16.5px}}
.data-card .num{{margin:0;background:#0b1825;color:#d9f3ff;border-color:rgba(55,168,230,.42)}}
.highlight-page{{background:linear-gradient(135deg,#07111b,#102033)}}
.highlight-page::before{{background:radial-gradient(circle at 78% 20%,color-mix(in srgb,var(--accent) 18%,transparent),transparent 2.4in),linear-gradient(135deg,rgba(255,255,255,.035),transparent 48%);background-size:auto,auto}}
.highlight-page h2{{color:#f5f8fb}}
.highlight-page .intro,.highlight-page .lead{{color:rgba(239,246,252,.86)}}
.highlight-page .data-card,.highlight-page .command-card{{background:rgba(245,250,255,.08);border-color:rgba(157,206,255,.2);box-shadow:none}}
.highlight-page h3{{color:#f5f8fb}}
.highlight-page .data-card p,.highlight-page .command-card p{{color:rgba(232,241,249,.82)}}
.highlight-page .data-card .eyebrow{{color:#a9dfff}}
.highlight-page .footer{{color:rgba(226,236,246,.5)}}
@media print{{body{{background:white}}.book{{width:auto;margin:0}}}}
"""


def professional_service_css(theme: dict[str, str]) -> str:
    accent = theme["accent"]
    dark = theme["dark"]
    return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --ink:#171b1f;
  --muted:#5d6870;
  --quiet:#8a9399;
  --paper:#fbfaf5;
  --paper-2:#f1eee6;
  --panel:#ffffff;
  --line:rgba(23,27,31,.13);
  --accent:{accent};
  --dark:{dark};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#d9d7d1;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;overflow:hidden;page-break-after:always;padding:.62in;background:linear-gradient(135deg,var(--paper),#fff 50%,var(--paper-2))}}
.page::before{{content:"";position:absolute;inset:.34in;border:1px solid rgba(23,27,31,.1);pointer-events:none}}
.page::after{{display:none}}
.brand{{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-start;color:rgba(23,27,31,.7);font-size:9px;font-weight:900;letter-spacing:.24em;text-transform:uppercase}}
.brand small{{display:block;margin-top:7px;color:var(--accent);font-size:8px;letter-spacing:.2em}}
.badge{{border:1px solid rgba(23,27,31,.14);background:rgba(255,255,255,.64);padding:9px 13px;color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}}
.cover-kicker{{position:relative;z-index:3;margin-top:.84in;display:flex;align-items:center;gap:12px;color:var(--accent);font-size:10px;font-weight:900;letter-spacing:.24em;text-transform:uppercase}}
.cover-kicker::before{{content:"";width:.48in;height:1px;background:var(--accent)}}
h1,h2,h3{{position:relative;z-index:3;margin:0;font-family:Georgia,"Times New Roman",serif;font-weight:400;letter-spacing:-.045em}}
h1{{max-width:5.65in;margin-top:.22in;font-size:58px;line-height:.96}}
h1 em,h2 em{{font-style:italic;color:var(--accent)}}
.lead{{position:relative;z-index:3;max-width:4.9in;margin-top:.32in;color:#384149;font-size:15.5px;line-height:1.62}}
.memo-strip{{position:absolute;z-index:3;left:.62in;right:.62in;bottom:1.08in;display:grid;grid-template-columns:1fr 1fr 1fr;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.memo-cell{{min-height:.96in;padding:17px 18px;border-left:1px solid var(--line)}}
.memo-cell:first-child{{border-left:0;padding-left:0}}
.memo-cell b{{display:block;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:24px;font-weight:400;line-height:1}}
.memo-cell span{{display:block;margin-top:9px;color:#5f6870;font-size:8.5px;font-weight:850;letter-spacing:.14em;line-height:1.55;text-transform:uppercase}}
.footer{{position:absolute;z-index:3;left:.62in;right:.62in;bottom:.34in;display:flex;justify-content:space-between;color:rgba(23,27,31,.55);font-size:8px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}}
.professional-cover .footer{{bottom:.56in}}
.work{{background:#fbfaf5;color:var(--ink)}}
.work::before{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 85% 8%,color-mix(in srgb,var(--accent) 10%,transparent),transparent 2.4in),linear-gradient(135deg,#fff,var(--paper-2));pointer-events:none}}
.work::after{{display:none}}
.section-head{{position:relative;z-index:3;display:grid;grid-template-columns:.88fr 1.12fr;gap:.42in;align-items:end;margin-top:.28in;padding-bottom:.24in;border-bottom:1px solid var(--line)}}
.eyebrow{{margin:0 0 10px;color:var(--accent);font-size:8px;font-weight:950;letter-spacing:.22em;text-transform:uppercase}}
h2{{font-size:39px;line-height:.98;color:var(--ink)}}
.intro{{margin:0;color:#46515a;font-size:12px;line-height:1.62}}
.advisory-grid{{position:relative;z-index:3;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:.34in}}
.advisory-card{{position:relative;min-height:1.78in;border:1px solid var(--line);background:rgba(255,255,255,.72);padding:18px;box-shadow:0 14px 34px rgba(23,27,31,.045)}}
.advisory-card::before{{content:"";position:absolute;left:18px;right:18px;top:0;height:3px;background:var(--accent);opacity:.72}}
.num{{display:inline-grid;width:.42in;height:.42in;place-items:center;margin-bottom:13px;border:1px solid color-mix(in srgb,var(--accent) 36%,transparent);border-radius:50%;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:14px}}
h3{{font-family:Inter,"Helvetica Neue",Arial,sans-serif;font-size:15px;line-height:1.16;letter-spacing:-.01em;font-weight:800;color:var(--ink)}}
.advisory-card p,.dossier-card p{{margin:9px 0 0;color:#46515a;font-size:10.2px;line-height:1.55}}
.content-stack{{position:relative;z-index:3;display:grid;gap:12px;margin-top:.31in}}
.dossier-card{{display:grid;grid-template-columns:.48in 1fr;gap:15px;padding:17px 18px;border:1px solid var(--line);background:rgba(255,255,255,.74);box-shadow:0 12px 28px rgba(23,27,31,.045)}}
.dossier-card .eyebrow{{margin-bottom:7px;color:#778088;font-size:7.4px;letter-spacing:.17em}}
.dossier-card h3{{font-size:15.8px}}
.dossier-card .num{{margin:0;background:#f5f4ee}}
.private-page{{background:#171b1f;color:#f7f4ed}}
.private-page::before{{background:radial-gradient(circle at 78% 18%,color-mix(in srgb,var(--accent) 18%,transparent),transparent 2.45in),linear-gradient(135deg,#171b1f,#101317)}}
.private-page::after{{display:none}}
.private-page .brand,.private-page .footer{{color:rgba(247,244,237,.58)}}
.private-page h2,.private-page h3{{color:#f7f4ed}}
.private-page .intro{{color:rgba(247,244,237,.74)}}
.private-page .dossier-card,.private-page .advisory-card{{background:rgba(255,255,255,.055);border-color:rgba(255,255,255,.13);box-shadow:none}}
.private-page .dossier-card p,.private-page .advisory-card p{{color:rgba(247,244,237,.74)}}
.private-page .dossier-card .eyebrow{{color:color-mix(in srgb,var(--accent) 72%,#fff)}}
@media print{{body{{background:white}}.book{{width:auto;margin:0}}}}
"""


def clean_lines(text: str, niche: str) -> list[str]:
    blocked = {niche.upper(), "CONTENT ELEVATED", "CONTENT ELEVATED HQ"}
    lines = []
    for line in text.splitlines():
        line = " ".join(line.strip().split())
        if not line or line.upper() in blocked:
            continue
        lines.append(line)
    return lines


def pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def paragraphize(lines: list[str]) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    buffer: list[str] = []
    for line in lines:
        is_heading = (
            len(line) < 105
            and (line.isupper() or SECTION_RE.match(line) or re.match(r"^(Template|Prompt|Chapter|Day|Week|Month)\s+\d+", line, re.I))
        )
        if is_heading:
            if buffer:
                blocks.append(("p", " ".join(buffer)))
                buffer = []
            blocks.append(("h", line))
        elif line.startswith(("✓", "•", "- ")):
            if buffer:
                blocks.append(("p", " ".join(buffer)))
                buffer = []
            blocks.append(("bullet", line))
        else:
            if len(" ".join(buffer + [line])) > 280:
                blocks.append(("p", " ".join(buffer)))
                buffer = [line]
            else:
                buffer.append(line)
    if buffer:
        blocks.append(("p", " ".join(buffer)))
    return blocks


def split_card_body(text: str, limit: int = 640) -> list[str]:
    if len(text) <= limit:
        return [text]
    pieces: list[str] = []
    remaining = text
    while remaining:
        if len(remaining) <= limit:
            pieces.append(remaining)
            break
        cut = max(remaining.rfind(". ", 0, limit), remaining.rfind("; ", 0, limit), remaining.rfind(", ", 0, limit))
        if cut < limit * 0.55:
            cut = remaining.rfind(" ", 0, limit)
        if cut < limit * 0.55:
            cut = limit
        pieces.append(remaining[: cut + 1].strip())
        remaining = remaining[cut + 1 :].strip()
    return [piece for piece in pieces if piece]


def chunk_blocks(blocks: list[tuple[str, str]], max_chars: int = 2900) -> list[list[tuple[str, str]]]:
    pages: list[list[tuple[str, str]]] = []
    current: list[tuple[str, str]] = []
    count = 0
    for kind, text in blocks:
        cost = len(text) + (80 if kind == "h" else 35)
        if current and count + cost > max_chars:
            pages.append(current)
            current = []
            count = 0
        current.append((kind, text))
        count += cost
    if current:
        pages.append(current)
    return pages


def render_blocks(blocks: list[tuple[str, str]]) -> str:
    parts = []
    for kind, text in blocks:
        escaped = html.escape(text)
        if kind == "h":
            parts.append(f"<h3>{escaped}</h3>" if len(text) < 56 else f'<div class="section-label">{escaped}</div>')
        elif kind == "bullet":
            parts.append(f'<p class="template-line">{escaped}</p>')
        else:
            class_name = ' class="template-line"' if text.lower().startswith(("subject", "write a", "copy and paste", "dear ")) else ""
            parts.append(f"<p{class_name}>{escaped}</p>")
    return "\n".join(parts)


def render_content_cards(blocks: list[tuple[str, str]]) -> str:
    cards: list[tuple[str, str]] = []
    current_title = "Action System"
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_body
        if current_body:
            for piece in split_card_body(" ".join(current_body)):
                cards.append((current_title, piece))
            current_body = []

    for kind, text in blocks:
        if kind == "h":
            flush()
            current_title = title_case(text)
            if current_title == "Advisory System":
                current_title = "Client Advisory System"
        else:
            current_body.append(text)
    flush()
    if not cards:
        cards = [("Action System", "Review this section and customize the language for your business before using it with clients.")]

    pieces = []
    for index, (card_title, body) in enumerate(cards, start=1):
        pieces.append(
            f"""
    <article class="prompt-card">
      <div class="num">{index:02d}</div>
      <div>
        <p class="eyebrow">Working page</p>
        <h3>{html.escape(card_title)}</h3>
        <p>{html.escape(body)}</p>
      </div>
    </article>
"""
        )
    return "\n".join(pieces)


def render_beauty_templates(blocks: list[tuple[str, str]], start_index: int = 1) -> str:
    cards: list[tuple[str, str, str]] = []
    current_title = "Action Template"
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_body
        if current_body:
            body = " ".join(current_body)
            for piece in split_card_body(body):
                cards.append((current_title, piece, ""))
            current_body = []

    for kind, text in blocks:
        if kind == "h":
            flush()
            current_title = title_case(text)
        else:
            current_body.append(text)
    flush()

    if not cards:
        cards = [("Action Template", "Customize this section with your client, offer, service, and brand details before sending or publishing.", "")]

    pieces = []
    for offset, (card_title, body, tip) in enumerate(cards, start=start_index):
        tip_text = tip.strip() or "Use this as a polished starting point, then add one real detail so the finished asset feels personal."
        pieces.append(
            f"""
      <div class="template">
        <div class="num">{offset:02d}</div>
        <div>
          <h3>{html.escape(card_title)}</h3>
          <div class="when">Customize before use</div>
          <div class="script">{html.escape(body)}</div>
          <div class="tip"><strong>Studio note:</strong> {html.escape(tip_text)}</div>
        </div>
      </div>"""
        )
    return "\n".join(pieces)


def build_beauty_html(niche: str, title: str, descriptor: str, theme: dict[str, str], blocks: list[tuple[str, str]]) -> str:
    title_html = html.escape(title).replace("AI", "<span>AI</span>")
    chunks = chunk_blocks(blocks, max_chars=2300)
    brand = html.escape(niche)
    bundle_label = f"{brand} Complete Growth Bundle"
    pages = [
        f"""<section class="page">
        <div class="brand">
          <div class="wordmark">{brand}<small>Complete Growth Bundle</small></div>
          <div class="badge">{html.escape(descriptor)}</div>
        </div>

        <p class="kicker" style="margin-top: 0.78in;">Copy · Customize · Launch</p>
        <h1>{title_html}</h1>
        <p class="lead">A polished, niche-specific growth system designed to help you turn client communication, content, and brand direction into a more consistent beauty business.</p>

        <div class="cover-meta">
          <div class="meta-item"><strong>01</strong><span>Ready-to-use system</span></div>
          <div class="meta-item"><strong>Studio</strong><span>Beauty-specific system</span></div>
          <div class="meta-item"><strong>Fast</strong><span>Customize and launch</span></div>
        </div>
        <div class="footer"><span>{bundle_label}</span><span>01</span></div>
      </section>""",
        f"""<section class="page">
        <div class="brand">
          <div class="wordmark">{brand}<small>Implementation System</small></div>
          <div class="badge">How to Use</div>
        </div>

        <p class="kicker" style="margin-top: 0.72in;">Before You Use It</p>
        <h2>Make the system feel <span>personal.</span></h2>
        <p class="lead">Use this file as the polished base. Replace brackets, offers, services, client details, and local language so every asset sounds like the business using it.</p>

        <div class="intro-grid">
          <div class="panel">
            <div class="label">The Rule</div>
            <p>Keep the strategy intact, but make every client-facing line specific. Beauty buyers respond to trust, taste, timing, and a sense that the experience was designed for them.</p>
          </div>
          <div class="panel dark">
            <div class="label">Best Practice</div>
            <p>Batch the assets weekly. Turn prompts into posts, templates into follow-ups, and brand direction into a consistent client experience across every touchpoint.</p>
          </div>
        </div>

        <div class="rule"></div>
        {render_beauty_templates(chunks[0] if chunks else blocks, 1)}

        <div class="footer"><span>{bundle_label}</span><span>02</span></div>
      </section>""",
    ]

    next_number = 1 + len(chunks[0]) if chunks else 1
    for page_index, chunk in enumerate(chunks[1:], start=3):
        pages.append(
            f"""<section class="page">
        <div class="brand">
          <div class="wordmark">{brand}<small>{html.escape(descriptor)}</small></div>
          <div class="badge">Working Pages</div>
        </div>

        <p class="kicker" style="margin-top: 0.42in;">{html.escape(descriptor)}</p>
        {render_beauty_templates(chunk, next_number)}

        <div class="footer"><span>{bundle_label}</span><span>{page_index:02d}</span></div>
      </section>"""
        )
        next_number += len(chunk)

    pages.append(
        f"""<section class="page cta-page">
        <div class="brand">
          <div class="wordmark">{brand}<small>Complete Growth Bundle</small></div>
          <div class="badge" style="color:#fff7ef;border-color:rgba(255,247,239,.24);background:rgba(255,247,239,.08)">Next Step</div>
        </div>

        <p class="kicker" style="margin-top: 1.15in; color:#f2c8c7;">Want the full system?</p>
        <h2 style="max-width: 5.7in;">Build a beauty brand experience that looks polished before it ever feels complicated.</h2>
        <p class="lead">Pair this file with the rest of the {brand} bundle: calendars, prompts, client systems, brand assets, templates, and launch materials.</p>
        <a class="cta-button">Content Elevated</a>
        <div class="footer"><span>{bundle_label}</span><span>{len(pages) + 1:02d}</span></div>
      </section>"""
    )

    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{html.escape(title)}</title><style>{beauty_css(theme)}</style></head><body><main class=\"book\">"
        + "\n".join(pages)
        + "</main></body></html>"
    )


def render_home_service_cards(blocks: list[tuple[str, str]], start_index: int = 1) -> str:
    cards: list[tuple[str, str]] = []
    current_title = "Field System"
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_body
        if current_body:
            for piece in split_card_body(" ".join(current_body)):
                cards.append((current_title, piece))
            current_body = []

    for kind, text in blocks:
        if kind == "h":
            flush()
            current_title = title_case(text)
        else:
            current_body.append(text)
    flush()

    if not cards:
        cards = [("Field System", "Customize this section for the service area, offer, client type, and next operational step.")]

    pieces = []
    for offset, (card_title, body) in enumerate(cards, start=start_index):
        pieces.append(
            f"""
    <article class="data-card">
      <div class="num">{offset:02d}</div>
      <div>
        <p class="eyebrow">Operator asset</p>
        <h3>{html.escape(card_title)}</h3>
        <p>{html.escape(body)}</p>
      </div>
    </article>"""
        )
    return "\n".join(pieces)


def build_home_service_html(niche: str, title: str, descriptor: str, theme: dict[str, str], blocks: list[tuple[str, str]]) -> str:
    title_html = html.escape(title).replace("AI", "<em>AI</em>")
    chunks = chunk_blocks(blocks, max_chars=2550)
    brand = html.escape(niche)
    pages = [
        f"""<section class="page">
  <div class="brand">
    <div>CONTENT ELEVATED<small>{brand} Growth System</small></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <p class="cover-kicker">Local authority · follow-up · booked jobs</p>
  <h1>{title_html}</h1>
  <p class="lead">A high-clarity operating file for turning estimates, service calls, reviews, reminders, and seasonal demand into a cleaner growth workflow.</p>
  <div class="system-strip">
    <div class="system-cell"><b>Field</b><span>Built for real service operators</span></div>
    <div class="system-cell"><b>Fast</b><span>Customize before the next job</span></div>
    <div class="system-cell"><b>Local</b><span>Sharper trust in your market</span></div>
    <div class="system-cell"><b>Repeat</b><span>Systems for steady demand</span></div>
  </div>
  <div class="footer"><span>{brand} growth system</span><span>01</span></div>
</section>""",
        f"""<section class="page work">
  <div class="brand">
    <div>CONTENT ELEVATED<small>{brand}</small></div>
    <div class="badge">Operator Notes</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">Use the system</p><h2>Make every lead easier to convert.</h2></div>
    <p class="intro">Start with the asset closest to the next revenue moment: estimate follow-up, maintenance reminder, review request, service agreement, seasonal campaign, or referral ask.</p>
  </div>
  <div class="command-grid">
    <article class="command-card"><div class="num">01</div><h3>Match the job type</h3><p>Adjust the language for install, repair, quote, maintenance, emergency call, membership, or repeat service.</p></article>
    <article class="command-card"><div class="num">02</div><h3>Localize the trust</h3><p>Add the city, service area, homeowner concern, business context, and proof points that make the message credible.</p></article>
    <article class="command-card"><div class="num">03</div><h3>Move fast</h3><p>Use the finished asset in the same week: send the follow-up, post the content, request the review, or launch the campaign.</p></article>
  </div>
  <div class="footer"><span>{html.escape(title)}</span><span>02</span></div>
</section>""",
    ]

    for page_index, chunk in enumerate(chunks, start=3):
        page_class = "page work highlight-page" if page_index % 3 == 0 else "page work"
        pages.append(
            f"""<section class="{page_class}">
  <div class="brand">
    <div>CONTENT ELEVATED<small>{brand}</small></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">{html.escape(descriptor)}</p><h2>{html.escape(title)}</h2></div>
    <p class="intro">Use these assets to tighten communication, increase trust, and create more consistent demand from the service area.</p>
  </div>
  <div class="content-stack">{render_home_service_cards(chunk)}</div>
  <div class="footer"><span>{html.escape(title)}</span><span>{page_index:02d}</span></div>
</section>"""
        )

    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{html.escape(title)}</title><style>{home_service_css(theme)}</style></head><body><main class=\"book\">"
        + "\n".join(pages)
        + "</main></body></html>"
    )


def render_professional_cards(blocks: list[tuple[str, str]], start_index: int = 1) -> str:
    cards: list[tuple[str, str]] = []
    current_title = "Client Communication Asset"
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_body
        if current_body:
            for piece in split_card_body(" ".join(current_body)):
                cards.append((current_title, piece))
            current_body = []

    for kind, text in blocks:
        if kind == "h":
            flush()
            current_title = title_case(text)
        else:
            current_body.append(text)
    flush()

    if not cards:
        cards = [("Client Communication Asset", "Customize this section for the client type, engagement, compliance context, and next professional touchpoint.")]

    pieces = []
    for offset, (card_title, body) in enumerate(cards, start=start_index):
        pieces.append(
            f"""
    <article class="dossier-card">
      <div class="num">{offset:02d}</div>
      <div>
        <p class="eyebrow">Client system</p>
        <h3>{html.escape(card_title)}</h3>
        <p>{html.escape(body)}</p>
      </div>
    </article>"""
        )
    return "\n".join(pieces)


def health_wellness_css(theme: dict[str, str]) -> str:
    accent = theme["accent"]
    accent2 = theme["accent2"]
    dark = theme["dark"]
    dental_deep_css = ""
    if theme.get("tag") == "Dental":
        dental_deep_css = """
.deep-page{background:linear-gradient(135deg,#f4fbff,#e8f6fb 54%,#dff0ee);color:#16323b}
.deep-page::before{background:
  radial-gradient(circle at 78% 16%,rgba(106,174,199,.26),transparent 2.55in),
  radial-gradient(circle at 14% 90%,rgba(154,209,184,.18),transparent 2.35in),
  linear-gradient(135deg,#fbfeff,#e8f6fb)}
.deep-page::after{background:linear-gradient(180deg,rgba(106,174,199,.12),transparent 68%);opacity:.82}
.deep-page h2,.deep-page h3{color:#15313a}
.deep-page .intro,.deep-page .care-card p,.deep-page .pathway-card p{color:#3f5f68}
.deep-page .care-card,.deep-page .pathway-card{background:rgba(255,255,255,.78);border-color:rgba(106,174,199,.2);box-shadow:0 14px 36px rgba(66,128,148,.075)}
.deep-page .brand,.deep-page .footer{color:rgba(31,72,84,.56)}
.deep-page .care-card .eyebrow{color:#6aaec7}
"""
    if theme.get("tag") == "Nutrition":
        dental_deep_css = """
.page{background:
  radial-gradient(circle at 84% 12%,rgba(237,241,223,.58),transparent 2.2in),
  radial-gradient(circle at 8% 82%,rgba(244,224,190,.26),transparent 2.55in),
  linear-gradient(135deg,#fffdf5,#ffffff 54%,#f4f7ea)}
.page::before{border-color:rgba(85,119,63,.16);border-radius:24px}
.cover-kicker{color:#55773f}
h1,h2{font-family:Georgia,"Times New Roman",serif;color:#263f25}
h1 em,h2 em{color:#7f934e}
.lead{color:#314433}
.badge{color:#55773f;border-color:rgba(85,119,63,.22);background:rgba(255,255,255,.72)}
.care-strip{background:rgba(255,255,255,.66);border-color:rgba(85,119,63,.16)}
.care-cell b,.num{color:#55773f}
.care-card .num{background:#f3f6e8}
.deep-page{background:linear-gradient(135deg,#fffdf5,#f3f7e8 52%,#edf1df);color:#243823}
.deep-page::before{background:
  radial-gradient(circle at 76% 14%,rgba(205,221,169,.38),transparent 2.45in),
  radial-gradient(circle at 16% 88%,rgba(224,190,133,.16),transparent 2.25in),
  linear-gradient(135deg,#fffdf5,#f3f7e8)}
.deep-page::after{background:linear-gradient(180deg,rgba(85,119,63,.09),transparent 68%);opacity:.78}
.deep-page h2,.deep-page h3{color:#263f25}
.deep-page .intro,.deep-page .care-card p,.deep-page .pathway-card p{color:#4d6046}
.deep-page .care-card,.deep-page .pathway-card{background:rgba(255,255,255,.82);border-color:rgba(85,119,63,.18);box-shadow:0 14px 36px rgba(88,116,66,.07)}
.deep-page .brand,.deep-page .footer{color:rgba(58,86,43,.56)}
.deep-page .care-card .eyebrow{color:#55773f}
"""
    return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --ink:#17201c;
  --muted:#607068;
  --quiet:#8b9992;
  --paper:#fbfcf7;
  --paper-2:#edf4ea;
  --panel:#ffffff;
  --line:rgba(28,55,43,.13);
  --accent:{accent};
  --accent-2:{accent2};
  --deep:{dark};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#dfe8df;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;overflow:hidden;page-break-after:always;padding:.58in;background:
  radial-gradient(circle at 82% 10%,color-mix(in srgb,var(--accent-2) 34%,transparent),transparent 2.15in),
  radial-gradient(circle at 8% 82%,rgba(255,255,255,.78),transparent 2.6in),
  linear-gradient(135deg,var(--paper),#fff 54%,var(--paper-2))}}
.page::before{{content:"";position:absolute;inset:.32in;border:1px solid var(--line);border-radius:30px;pointer-events:none}}
.page::after{{content:"";position:absolute;right:-1.1in;top:.3in;width:3.8in;height:9.8in;border-radius:999px;background:linear-gradient(180deg,color-mix(in srgb,var(--accent) 13%,transparent),transparent 66%);opacity:.72;pointer-events:none}}
.brand{{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-start;color:rgba(23,32,28,.68);font-size:9px;font-weight:900;letter-spacing:.23em;text-transform:uppercase}}
.brand small{{display:block;margin-top:7px;color:var(--accent);font-size:8px;letter-spacing:.18em}}
.badge{{border:1px solid color-mix(in srgb,var(--accent) 22%,transparent);border-radius:999px;background:rgba(255,255,255,.64);padding:10px 14px;color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}}
.cover-kicker{{position:relative;z-index:3;margin-top:.82in;display:flex;align-items:center;gap:12px;color:var(--accent);font-size:10px;font-weight:900;letter-spacing:.25em;text-transform:uppercase}}
.cover-kicker::before{{content:"";width:.48in;height:1px;background:var(--accent)}}
h1,h2,h3{{position:relative;z-index:3;margin:0;font-family:Georgia,"Times New Roman",serif;font-weight:400;letter-spacing:-.045em}}
h1{{max-width:5.9in;margin-top:.2in;font-size:62px;line-height:.95}}
h1 em,h2 em{{font-style:italic;color:var(--accent)}}
.lead{{position:relative;z-index:3;max-width:5.05in;margin-top:.32in;color:#3f4f48;font-size:15.5px;line-height:1.62}}
.care-strip{{position:absolute;z-index:3;left:.58in;right:.58in;bottom:.82in;display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);background:rgba(255,255,255,.58);backdrop-filter:blur(10px)}}
.care-cell{{min-height:.92in;padding:16px 15px;border-left:1px solid var(--line)}}
.care-cell:first-child{{border-left:0}}
.care-cell b{{display:block;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:25px;font-weight:400;line-height:1}}
.care-cell span{{display:block;margin-top:8px;color:#64746d;font-size:8.4px;font-weight:850;letter-spacing:.14em;line-height:1.5;text-transform:uppercase}}
.footer{{position:absolute;z-index:3;left:.58in;right:.58in;bottom:.34in;display:flex;justify-content:space-between;color:rgba(57,74,66,.58);font-size:8px;font-weight:850;letter-spacing:.15em;text-transform:uppercase}}
.health-cover .footer{{bottom:.56in}}
.work{{background:#fbfcf7;color:var(--ink)}}
.work::before{{content:"";position:absolute;inset:0;background:
  radial-gradient(circle at 82% 8%,color-mix(in srgb,var(--accent-2) 22%,transparent),transparent 2.35in),
  linear-gradient(135deg,#fff,var(--paper-2));pointer-events:none}}
.work::after{{display:none}}
.section-head{{position:relative;z-index:3;display:grid;grid-template-columns:.92fr 1.08fr;gap:.38in;align-items:end;margin-top:.28in;padding-bottom:.24in;border-bottom:1px solid var(--line)}}
.eyebrow{{margin:0 0 10px;color:var(--accent);font-size:8px;font-weight:950;letter-spacing:.22em;text-transform:uppercase}}
h2{{font-size:41px;line-height:.98;color:var(--ink)}}
.intro{{margin:0;color:#4d5d56;font-size:12.2px;line-height:1.62}}
.pathway-grid{{position:relative;z-index:3;display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-top:.34in}}
.pathway-card{{position:relative;min-height:1.88in;border:1px solid var(--line);border-radius:20px;background:rgba(255,255,255,.72);padding:18px;box-shadow:0 16px 42px rgba(28,55,43,.055)}}
.pathway-card::before{{content:"";position:absolute;left:18px;right:18px;top:0;height:3px;border-radius:999px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent-2) 82%,#fff));opacity:.76}}
.num{{display:inline-grid;width:.42in;height:.42in;place-items:center;margin-bottom:13px;border:1px solid color-mix(in srgb,var(--accent) 34%,transparent);border-radius:50%;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:14px;background:rgba(255,255,255,.7)}}
h3{{font-family:Inter,"Helvetica Neue",Arial,sans-serif;font-size:15.4px;line-height:1.16;letter-spacing:-.01em;font-weight:850;color:var(--ink)}}
.pathway-card p,.care-card p{{margin:9px 0 0;color:#485a52;font-size:10.4px;line-height:1.56}}
.content-stack{{position:relative;z-index:3;display:grid;gap:12px;margin-top:.31in}}
.care-card{{display:grid;grid-template-columns:.48in 1fr;gap:15px;padding:17px 18px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.74);box-shadow:0 12px 30px rgba(28,55,43,.045)}}
.care-card .eyebrow{{margin-bottom:7px;color:#718179;font-size:7.4px;letter-spacing:.17em}}
.care-card h3{{font-size:16px}}
.care-card .num{{margin:0;background:#f4f8f2}}
.deep-page{{background:linear-gradient(135deg,var(--deep),#101914);color:#f7fbf5}}
.deep-page::before{{background:radial-gradient(circle at 78% 18%,color-mix(in srgb,var(--accent) 22%,transparent),transparent 2.45in),linear-gradient(135deg,var(--deep),#101914)}}
.deep-page h2,.deep-page h3{{color:#f7fbf5}}
.deep-page .intro,.deep-page .care-card p,.deep-page .pathway-card p{{color:rgba(238,247,236,.82)}}
.deep-page .care-card,.deep-page .pathway-card{{background:rgba(255,255,255,.075);border-color:rgba(216,235,211,.18);box-shadow:none}}
.deep-page .brand,.deep-page .footer{{color:rgba(238,247,236,.58)}}
.deep-page .care-card .eyebrow{{color:#cfe2c8}}
{dental_deep_css}
@media print{{body{{background:white}}.book{{width:auto;margin:0}}}}
"""


def render_health_wellness_cards(blocks: list[tuple[str, str]], start_index: int = 1) -> str:
    cards: list[tuple[str, str]] = []
    current_title = "Care System"
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_body
        if current_body:
            for piece in split_card_body(" ".join(current_body)):
                cards.append((current_title, piece))
            current_body = []

    for kind, text in blocks:
        if kind == "h":
            flush()
            current_title = title_case(text)
        else:
            current_body.append(text)
    flush()

    if not cards:
        cards = [("Care System", "Customize this section for the patient/client type, appointment stage, care plan, and next trust-building touchpoint.")]

    pieces = []
    for offset, (card_title, body) in enumerate(cards, start=start_index):
        pieces.append(
            f"""
    <article class="care-card">
      <div class="num">{offset:02d}</div>
      <div>
        <p class="eyebrow">Care asset</p>
        <h3>{html.escape(card_title)}</h3>
        <p>{html.escape(body)}</p>
      </div>
    </article>"""
        )
    return "\n".join(pieces)


def build_health_wellness_html(niche: str, title: str, descriptor: str, theme: dict[str, str], blocks: list[tuple[str, str]]) -> str:
    title_html = html.escape(title).replace("AI", "<em>AI</em>")
    chunks = chunk_blocks(blocks, max_chars=2550)
    brand = html.escape(niche)
    niche_copy = HEALTH_WELLNESS_COPY.get(
        niche,
        {
            "kicker": "Care · trust · consistent growth",
            "lead": "A calm, credible growth system for turning education, follow-up, retention, referrals, and patient/client communication into a more trusted care experience.",
            "cells": [("01", "Educate with clarity"), ("02", "Nurture between visits"), ("03", "Strengthen retention"), ("04", "Grow through trust")],
            "intro": "Start with the next care moment: new inquiry, post-visit follow-up, reactivation, review request, education post, treatment plan support, or referral touchpoint.",
        },
    )
    cover_kicker = niche_copy["kicker"]
    cover_lead = niche_copy["lead"]
    care_cells = niche_copy["cells"]
    care_intro = niche_copy["intro"]
    care_cells_html = "\n    ".join(
        f'<div class="care-cell"><b>{number}</b><span>{html.escape(label)}</span></div>' for number, label in care_cells
    )
    pages = [
        f"""<section class="page health-cover">
  <div class="brand">
    <div></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <p class="cover-kicker">{cover_kicker}</p>
  <h1>{title_html}</h1>
  <p class="lead">{cover_lead}</p>
  <div class="care-strip">
    {care_cells_html}
  </div>
  <div class="footer"><span>Content Elevated</span><span>01</span></div>
</section>""",
        f"""<section class="page work">
  <div class="brand">
    <div></div>
    <div class="badge">Care Notes</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">Use the system</p><h2>Make care easier to understand and act on.</h2></div>
    <p class="intro">{care_intro}</p>
  </div>
  <div class="pathway-grid">
    <article class="pathway-card"><div class="num">01</div><h3>Lead with reassurance</h3><p>Use calm, specific language that helps people feel informed before they take the next step.</p></article>
    <article class="pathway-card"><div class="num">02</div><h3>Support the journey</h3><p>Connect content and templates to real care stages: consult, appointment, plan, follow-up, and return visit.</p></article>
    <article class="pathway-card"><div class="num">03</div><h3>Keep trust consistent</h3><p>Review every asset for accuracy, warmth, compliance awareness, and the tone of a premium practice.</p></article>
  </div>
  <div class="footer"><span>{html.escape(title)}</span><span>02</span></div>
</section>""",
    ]

    for page_index, chunk in enumerate(chunks, start=3):
        page_class = "page work deep-page" if page_index % 3 == 0 else "page work"
        pages.append(
            f"""<section class="{page_class}">
  <div class="brand">
    <div></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">{html.escape(descriptor)}</p><h2>{html.escape(title)}</h2></div>
    <p class="intro">Use these assets to make education, communication, retention, and reactivation feel clear, polished, and easier to implement.</p>
  </div>
  <div class="content-stack">{render_health_wellness_cards(chunk)}</div>
  <div class="footer"><span>{html.escape(title)}</span><span>{page_index:02d}</span></div>
</section>"""
        )

    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{html.escape(title)}</title><style>{health_wellness_css(theme)}</style></head><body><main class=\"book\">"
        + "\n".join(pages)
        + "</main></body></html>"
    )


def creative_event_css(theme: dict[str, str], family: str) -> str:
    accent = theme["accent"]
    accent2 = theme["accent2"]
    dark = theme["dark"]
    paper = theme["paper"]
    if family == "interiors":
        return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --ink:#173a36;
  --muted:#66756f;
  --quiet:#8d8174;
  --paper:#fbf7ef;
  --paper-2:#efe5d8;
  --line:rgba(31,79,73,.14);
  --accent:{accent};
  --accent-2:{accent2};
  --clay:#bb7855;
  --brass:#b88754;
  --deep:{dark};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#e7dfd4;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;overflow:hidden;page-break-after:always;padding:.58in;background:
  radial-gradient(circle at 84% 10%,rgba(217,199,174,.42),transparent 2.65in),
  radial-gradient(circle at 10% 88%,rgba(31,79,73,.07),transparent 2.25in),
  linear-gradient(135deg,#fffdf8,#fbf7ef 56%,#f2eadf)}}
.page::before{{content:"";position:absolute;inset:.28in .34in .46in;border:1px solid rgba(31,79,73,.13);pointer-events:none}}
.page::after{{content:"";position:absolute;right:.66in;top:1.05in;width:2.1in;height:2.1in;border-radius:50%;border:1px solid rgba(31,79,73,.12);background:radial-gradient(circle,rgba(255,255,255,.5),rgba(217,199,174,.18) 62%,transparent 63%);opacity:.72;pointer-events:none}}
.brand{{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-start;color:rgba(23,58,54,.66);font-size:9px;font-weight:900;letter-spacing:.28em;text-transform:uppercase}}
.badge{{position:relative;z-index:3;border:1px solid rgba(31,79,73,.18);background:rgba(255,255,255,.72);padding:10px 14px;color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}}
.cover-kicker{{position:relative;z-index:3;margin-top:.86in;display:flex;align-items:center;gap:12px;color:var(--brass);font-size:10px;font-weight:900;letter-spacing:.28em;text-transform:uppercase}}
.cover-kicker::before{{content:"";width:.5in;height:1px;background:var(--brass)}}
h1,h2,h3{{position:relative;z-index:3;margin:0;font-family:Georgia,"Times New Roman",serif;font-weight:400;letter-spacing:-.05em;color:var(--ink)}}
h1{{max-width:5.8in;margin-top:.22in;font-size:58px;line-height:.98}}
h1 em,h2 em{{font-style:normal;color:var(--clay)}}
.lead{{position:relative;z-index:3;max-width:5.12in;margin-top:.3in;color:#42544f;font-size:14.5px;line-height:1.66}}
.signature-strip{{position:absolute;z-index:3;left:.58in;right:.58in;bottom:.86in;display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:rgba(255,255,255,.56)}}
.signature-cell{{min-height:.92in;padding:16px 15px;border-left:1px solid var(--line)}}
.signature-cell:first-child{{border-left:0}}
.signature-cell b{{display:block;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:23px;font-weight:400;line-height:1}}
.signature-cell span{{display:block;margin-top:9px;color:#6f7d76;font-size:8.3px;font-weight:850;letter-spacing:.14em;line-height:1.5;text-transform:uppercase}}
.footer{{position:absolute;z-index:3;left:.58in;right:.58in;bottom:.52in;display:flex;justify-content:space-between;color:rgba(23,58,54,.55);font-size:8px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}}
.work{{background:#fbf7ef;color:var(--ink);padding:.58in}}
.work::before{{content:"";position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(255,255,255,.86),rgba(255,255,255,.52)),
  radial-gradient(circle at 86% 10%,rgba(217,199,174,.34),transparent 2.35in),
  radial-gradient(circle at 8% 88%,rgba(31,79,73,.06),transparent 2.25in);pointer-events:none}}
.work::after{{display:none}}
.section-head{{position:relative;z-index:3;display:grid;grid-template-columns:.92fr 1.08fr;gap:.38in;align-items:end;margin-top:.25in;padding-bottom:.23in;border-bottom:1px solid var(--line)}}
.eyebrow{{margin:0 0 10px;color:var(--clay);font-size:8px;font-weight:950;letter-spacing:.24em;text-transform:uppercase}}
h2{{font-size:39px;line-height:.98}}
.intro{{margin:0;color:#4e605b;font-size:12px;line-height:1.62}}
.creative-grid{{position:relative;z-index:3;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:.34in}}
.creative-card{{position:relative;min-height:1.82in;border:1px solid var(--line);background:rgba(255,255,255,.84);padding:18px;box-shadow:0 10px 24px rgba(64,68,58,.035)}}
.creative-card::before{{content:"";position:absolute;left:18px;right:18px;top:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--brass));opacity:.62}}
.num{{display:inline-grid;width:.42in;height:.42in;place-items:center;margin-bottom:12px;border:1px solid rgba(31,79,73,.25);background:#fffaf2;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:13px;font-weight:400}}
h3{{font-family:Inter,"Helvetica Neue",Arial,sans-serif;color:var(--ink);font-size:15px;line-height:1.14;font-weight:850;letter-spacing:-.01em}}
.creative-card p,.asset-card p{{margin:9px 0 0;color:#4e605b;font-size:10.35px;line-height:1.56}}
.content-stack{{position:relative;z-index:3;display:grid;gap:12px;margin-top:.31in}}
.asset-card{{display:grid;grid-template-columns:.48in 1fr;gap:15px;padding:17px 18px;border:1px solid var(--line);background:rgba(255,255,255,.88);box-shadow:0 10px 22px rgba(64,68,58,.035)}}
.asset-card .eyebrow{{margin-bottom:7px;color:#8b7d6d;font-size:7.4px;letter-spacing:.17em}}
.asset-card h3{{font-size:16px}}
.asset-card .num{{margin:0;background:#173a36;color:#fff;border-color:rgba(31,79,73,.22)}}
.feature-page{{background:
  radial-gradient(circle at 80% 12%,rgba(31,79,73,.09),transparent 2.5in),
  radial-gradient(circle at 8% 90%,rgba(187,120,85,.08),transparent 2.25in),
  linear-gradient(135deg,#fffdf8,#f2eadf);color:#173a36}}
.feature-page::before{{inset:.28in .34in .46in;border:1px solid rgba(31,79,73,.13);background:transparent}}
.feature-page .section-head{{border-color:rgba(31,79,73,.16)}}
.feature-page .eyebrow{{color:#b88754}}
.feature-page h2{{color:#173a36;max-width:none}}
.feature-page .intro{{color:#4e605b}}
.feature-page .asset-card,.feature-page .creative-card{{background:rgba(255,255,255,.78);border-color:rgba(31,79,73,.14);box-shadow:0 14px 34px rgba(31,79,73,.05)}}
.feature-page .asset-card p,.feature-page .creative-card p{{color:#4e605b}}
.feature-page .asset-card h3,.feature-page .creative-card h3{{color:#173a36}}
.feature-page .brand,.feature-page .footer{{color:rgba(23,58,54,.55)}}
@media print{{body{{background:white}}.book{{width:auto;margin:0}}}}
"""
    if family == "speaker":
        return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --ink:#071426;
  --muted:#536171;
  --paper:#f8fbff;
  --paper-2:#eef4fb;
  --line:rgba(7,20,38,.13);
  --accent:{accent};
  --accent-2:{accent2};
  --deep:{dark};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#e8eef5;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;overflow:hidden;page-break-after:always;padding:.58in;background:
  radial-gradient(circle at 82% 12%,rgba(13,47,91,.12),transparent 2.45in),
  radial-gradient(circle at 10% 90%,rgba(211,154,54,.12),transparent 2.2in),
  linear-gradient(135deg,#fff,#f8fbff 52%,#edf4fb)}}
.page::before{{content:"";position:absolute;inset:0;background:
  linear-gradient(90deg,rgba(13,47,91,.09),transparent 28%),
  radial-gradient(ellipse at 82% 20%,rgba(13,47,91,.18),transparent 2.9in);pointer-events:none}}
.page::after{{content:"";position:absolute;right:-.65in;top:.25in;width:3.2in;height:9.4in;background:linear-gradient(180deg,rgba(7,20,38,.1),transparent 62%);border-left:1px solid rgba(13,47,91,.12);transform:skewX(-6deg);pointer-events:none}}
.brand{{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-start;color:rgba(7,20,38,.72);font-size:9px;font-weight:950;letter-spacing:.26em;text-transform:uppercase}}
.badge{{position:relative;z-index:3;border:1px solid rgba(13,47,91,.18);border-radius:999px;background:rgba(255,255,255,.78);padding:10px 14px;color:#0d2f5b;font-size:9px;font-weight:950;letter-spacing:.18em;text-transform:uppercase}}
.cover-kicker{{position:relative;z-index:3;margin-top:.72in;display:flex;align-items:center;gap:12px;color:#d39a36;font-size:10px;font-weight:950;letter-spacing:.28em;text-transform:uppercase}}
.cover-kicker::before{{content:"";width:.48in;height:1px;background:#d39a36}}
h1,h2,h3{{position:relative;z-index:3;margin:0}}
h1{{max-width:6.45in;margin-top:.16in;color:#071426;font-family:"Arial Narrow","Helvetica Neue",Arial,sans-serif;font-size:72px;line-height:.86;font-weight:950;letter-spacing:-.055em;text-transform:uppercase}}
h1 em{{font-style:normal;color:#d39a36;text-shadow:none}}
.lead{{position:relative;z-index:3;max-width:5.35in;margin-top:.26in;color:#243449;font-size:15.5px;line-height:1.6}}
.signature-strip{{position:absolute;z-index:3;left:.58in;right:.58in;bottom:.86in;display:grid;grid-template-columns:repeat(4,1fr);border:1px solid rgba(13,47,91,.13);background:rgba(255,255,255,.76);box-shadow:0 20px 60px rgba(7,20,38,.08)}}
.signature-cell{{min-height:.96in;padding:16px 15px;border-left:1px solid rgba(13,47,91,.12)}}
.signature-cell:first-child{{border-left:0}}
.signature-cell b{{display:block;color:#0d2f5b;font-family:"Arial Narrow","Helvetica Neue",Arial,sans-serif;font-size:23px;font-weight:950;line-height:1}}
.signature-cell span{{display:block;margin-top:9px;color:#536171;font-size:8.3px;font-weight:900;letter-spacing:.14em;line-height:1.5;text-transform:uppercase}}
.footer{{position:absolute;z-index:3;left:.58in;right:.58in;bottom:.34in;display:flex;justify-content:space-between;color:rgba(7,20,38,.55);font-size:8px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}}
.work{{background:#f8fbff;color:#071426}}
.work::before{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 84% 8%,rgba(13,47,91,.1),transparent 2.35in),linear-gradient(135deg,#fff,#edf4fb);pointer-events:none}}
.work::after{{display:none}}
.section-head{{position:relative;z-index:3;display:grid;grid-template-columns:.92fr 1.08fr;gap:.36in;align-items:end;margin-top:.25in;padding-bottom:.22in;border-bottom:1px solid var(--line)}}
.eyebrow{{margin:0 0 10px;color:#d39a36;font-size:8px;font-weight:950;letter-spacing:.23em;text-transform:uppercase}}
h2{{color:#071426;font-family:"Arial Narrow","Helvetica Neue",Arial,sans-serif;font-size:42px;line-height:.94;font-weight:950;letter-spacing:-.045em;text-transform:uppercase}}
.intro{{margin:0;color:#425163;font-size:12px;line-height:1.62}}
.creative-grid{{position:relative;z-index:3;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:.34in}}
.creative-card{{position:relative;min-height:1.84in;border:1px solid rgba(13,47,91,.13);background:linear-gradient(145deg,#fff,rgba(240,246,252,.94));padding:18px;box-shadow:0 14px 34px rgba(7,20,38,.055)}}
.creative-card::before{{content:"";position:absolute;left:0;top:0;width:4px;height:100%;background:linear-gradient(180deg,#0d2f5b,#d39a36)}}
.num{{display:inline-grid;width:.42in;height:.42in;place-items:center;margin-bottom:12px;border:1px solid rgba(13,47,91,.24);border-radius:50%;color:#d39a36;background:#fff;font-size:12px;font-weight:950}}
h3{{color:#071426;font-size:15px;line-height:1.13;font-weight:900;letter-spacing:-.01em}}
.creative-card p,.asset-card p{{margin:9px 0 0;color:#34465b;font-size:10.45px;line-height:1.55}}
.content-stack{{position:relative;z-index:3;display:grid;gap:12px;margin-top:.31in}}
.asset-card{{display:grid;grid-template-columns:.48in 1fr;gap:15px;padding:17px 18px;border:1px solid rgba(13,47,91,.13);background:rgba(255,255,255,.78);box-shadow:0 12px 30px rgba(7,20,38,.05)}}
.asset-card .eyebrow{{margin-bottom:7px;color:#617186;font-size:7.4px;letter-spacing:.17em}}
.asset-card h3{{font-size:16.2px}}
.asset-card .num{{margin:0;background:#0d2f5b;color:#fff;border-color:rgba(13,47,91,.2)}}
.feature-page{{background:linear-gradient(135deg,#071426,#0d2f5b 58%,#06101f);color:#fff}}
.feature-page::before{{background:radial-gradient(circle at 76% 14%,rgba(211,154,54,.22),transparent 2.45in),linear-gradient(135deg,rgba(255,255,255,.04),transparent 48%)}}
.feature-page h2,.feature-page h3{{color:#fff}}
.feature-page .intro,.feature-page .asset-card p,.feature-page .creative-card p{{color:rgba(255,255,255,.78)}}
.feature-page .asset-card,.feature-page .creative-card{{background:rgba(255,255,255,.075);border-color:rgba(255,255,255,.16);box-shadow:none}}
.feature-page .asset-card .eyebrow{{color:#f2c46d}}
.feature-page .brand,.feature-page .footer{{color:rgba(255,255,255,.56)}}
@media print{{body{{background:white}}.book{{width:auto;margin:0}}}}
"""
    if family == "atelier":
        return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --ink:#201917;
  --muted:#76665f;
  --paper:{paper};
  --paper-2:#f4e9dd;
  --line:rgba(74,55,45,.14);
  --accent:{accent};
  --accent-2:{accent2};
  --deep:{dark};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#e9ded2;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;overflow:hidden;page-break-after:always;padding:.6in;background:
  radial-gradient(circle at 80% 10%,color-mix(in srgb,var(--accent-2) 32%,transparent),transparent 2.35in),
  radial-gradient(circle at 8% 84%,rgba(255,255,255,.72),transparent 2.5in),
  linear-gradient(135deg,var(--paper),#fff 54%,var(--paper-2))}}
.page::before{{content:"";position:absolute;inset:.32in;border:1px solid var(--line);border-radius:28px;pointer-events:none}}
.page::after{{content:"";position:absolute;right:-1.2in;top:.25in;width:3.6in;height:9.4in;border-radius:999px;background:linear-gradient(180deg,color-mix(in srgb,var(--accent-2) 24%,transparent),transparent 68%);opacity:.72;pointer-events:none}}
.brand{{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-start;color:rgba(32,25,23,.66);font-size:9px;font-weight:900;letter-spacing:.24em;text-transform:uppercase}}
.badge{{border:1px solid color-mix(in srgb,var(--accent) 24%,transparent);border-radius:999px;background:rgba(255,255,255,.66);padding:10px 14px;color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}}
.cover-kicker{{position:relative;z-index:3;margin-top:.84in;display:flex;align-items:center;gap:12px;color:var(--accent);font-size:10px;font-weight:900;letter-spacing:.24em;text-transform:uppercase}}
.cover-kicker::before{{content:"";width:.5in;height:1px;background:var(--accent)}}
h1,h2,h3{{position:relative;z-index:3;margin:0;font-family:Georgia,"Times New Roman",serif;font-weight:400;letter-spacing:-.045em}}
h1{{max-width:6.1in;margin-top:.2in;font-size:64px;line-height:.94;color:#211916}}
h1 em,h2 em{{font-style:italic;color:var(--accent)}}
.lead{{position:relative;z-index:3;max-width:5.2in;margin-top:.3in;color:#51443e;font-size:15.5px;line-height:1.62}}
.signature-strip{{position:absolute;z-index:3;left:.6in;right:.6in;bottom:.84in;display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);background:rgba(255,255,255,.62);backdrop-filter:blur(10px)}}
.signature-cell{{min-height:.94in;padding:16px 15px;border-left:1px solid var(--line)}}
.signature-cell:first-child{{border-left:0}}
.signature-cell b{{display:block;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:25px;font-weight:400;line-height:1}}
.signature-cell span{{display:block;margin-top:8px;color:#7a6a60;font-size:8.4px;font-weight:850;letter-spacing:.14em;line-height:1.5;text-transform:uppercase}}
.footer{{position:absolute;z-index:3;left:.6in;right:.6in;bottom:.56in;display:flex;justify-content:space-between;color:rgba(66,51,45,.58);font-size:8px;font-weight:850;letter-spacing:.15em;text-transform:uppercase}}
.work{{background:var(--paper);color:var(--ink)}}
.work::before{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 84% 8%,color-mix(in srgb,var(--accent-2) 20%,transparent),transparent 2.35in),linear-gradient(135deg,#fff,var(--paper-2));pointer-events:none}}
.work::after{{display:none}}
.section-head{{position:relative;z-index:3;display:grid;grid-template-columns:.9fr 1.1fr;gap:.38in;align-items:end;margin-top:.28in;padding-bottom:.24in;border-bottom:1px solid var(--line)}}
.eyebrow{{margin:0 0 10px;color:var(--accent);font-size:8px;font-weight:950;letter-spacing:.22em;text-transform:uppercase}}
h2{{font-size:41px;line-height:.98;color:var(--ink)}}
.intro{{margin:0;color:#5a4c45;font-size:12.2px;line-height:1.62}}
.creative-grid{{position:relative;z-index:3;display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-top:.34in}}
.creative-card{{position:relative;min-height:1.88in;border:1px solid var(--line);border-radius:20px;background:rgba(255,255,255,.72);padding:18px;box-shadow:0 16px 42px rgba(74,55,45,.055)}}
.creative-card::before{{content:"";position:absolute;left:18px;right:18px;top:0;height:3px;border-radius:999px;background:linear-gradient(90deg,var(--accent),var(--accent-2));opacity:.78}}
.num{{display:inline-grid;width:.42in;height:.42in;place-items:center;margin-bottom:13px;border:1px solid color-mix(in srgb,var(--accent) 34%,transparent);border-radius:50%;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:14px;background:rgba(255,255,255,.7)}}
h3{{font-family:Inter,"Helvetica Neue",Arial,sans-serif;font-size:15.3px;line-height:1.16;letter-spacing:-.01em;font-weight:850;color:var(--ink)}}
.creative-card p,.asset-card p{{margin:9px 0 0;color:#5a4c45;font-size:10.4px;line-height:1.56}}
.content-stack{{position:relative;z-index:3;display:grid;gap:12px;margin-top:.31in}}
.asset-card{{display:grid;grid-template-columns:.48in 1fr;gap:15px;padding:17px 18px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.74);box-shadow:0 12px 30px rgba(74,55,45,.045)}}
.asset-card .eyebrow{{margin-bottom:7px;color:#85736a;font-size:7.4px;letter-spacing:.17em}}
.asset-card h3{{font-size:16px}}
.asset-card .num{{margin:0;background:#f7f1ea}}
.feature-page{{background:linear-gradient(135deg,#fffaf4,#f2e6d9 54%,color-mix(in srgb,var(--accent-2) 24%,#f8f0e7));color:#2a201c}}
.feature-page::before{{background:radial-gradient(circle at 76% 14%,color-mix(in srgb,var(--accent-2) 26%,transparent),transparent 2.45in),linear-gradient(135deg,#fffaf4,#f2e6d9)}}
.feature-page h2,.feature-page h3{{color:#2a201c}}
.feature-page .asset-card,.feature-page .creative-card{{background:rgba(255,255,255,.78);border-color:rgba(74,55,45,.14);box-shadow:0 14px 36px rgba(74,55,45,.055)}}
@media print{{body{{background:white}}.book{{width:auto;margin:0}}}}
"""

    return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --ink:#f8f5ef;
  --muted:#b9b0a6;
  --paper:#08090d;
  --panel:#11131a;
  --line:rgba(248,245,239,.14);
  --accent:{accent};
  --accent-2:{accent2};
  --deep:{dark};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#08090d;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;overflow:hidden;page-break-after:always;padding:.56in;background:linear-gradient(135deg,#05060a,var(--deep) 58%,#08090d)}}
.page::before{{content:"";position:absolute;inset:0;background:
  radial-gradient(circle at 78% 16%,color-mix(in srgb,var(--accent) 24%,transparent),transparent 2.35in),
  radial-gradient(circle at 15% 92%,color-mix(in srgb,var(--accent-2) 12%,transparent),transparent 2.55in),
  linear-gradient(135deg,rgba(255,255,255,.035),transparent 44%);pointer-events:none}}
.page::after{{content:"";position:absolute;right:-1.2in;top:.55in;width:4.1in;height:8.8in;border:1px solid rgba(248,245,239,.08);background:linear-gradient(180deg,rgba(255,255,255,.035),transparent 65%);transform:skewX(-8deg);opacity:.5;pointer-events:none}}
.brand{{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-start;color:rgba(248,245,239,.66);font-size:9px;font-weight:900;letter-spacing:.25em;text-transform:uppercase}}
.badge{{border:1px solid rgba(248,245,239,.15);border-radius:999px;background:rgba(255,255,255,.045);padding:10px 14px;color:color-mix(in srgb,var(--accent) 78%,#fff);font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}}
.cover-kicker{{position:relative;z-index:3;margin-top:.82in;color:color-mix(in srgb,var(--accent) 82%,#fff);font-size:10px;font-weight:950;letter-spacing:.28em;text-transform:uppercase}}
h1,h2,h3{{position:relative;z-index:3;margin:0}}
h1{{max-width:6.7in;margin-top:.16in;font-family:"Arial Narrow","Helvetica Neue",Arial,sans-serif;font-size:72px;line-height:.86;font-weight:950;letter-spacing:-.055em;text-transform:uppercase}}
h1 em{{font-style:normal;color:#fff;text-shadow:0 0 30px color-mix(in srgb,var(--accent) 36%,transparent)}}
.lead{{position:relative;z-index:3;max-width:5.5in;margin-top:.28in;color:rgba(248,245,239,.84);font-size:16px;line-height:1.58}}
.signature-strip{{position:absolute;z-index:3;left:.56in;right:.56in;bottom:.86in;display:grid;grid-template-columns:repeat(4,1fr);border:1px solid rgba(248,245,239,.16);background:rgba(6,7,11,.72);box-shadow:0 22px 70px rgba(0,0,0,.24)}}
.signature-cell{{min-height:.98in;padding:17px 15px;border-left:1px solid var(--line)}}
.signature-cell:first-child{{border-left:0}}
.signature-cell b{{display:block;color:#fff;font-size:20px;line-height:1;font-weight:950;letter-spacing:-.02em}}
.signature-cell span{{display:block;margin-top:10px;color:rgba(248,245,239,.74);font-size:8.4px;font-weight:850;letter-spacing:.14em;line-height:1.55;text-transform:uppercase}}
.footer{{position:absolute;z-index:3;left:.56in;right:.56in;bottom:.34in;display:flex;justify-content:space-between;color:rgba(248,245,239,.5);font-size:8px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}}
.work{{background:#f8f6f1;color:#151515}}
.work::before{{background:radial-gradient(circle at 84% 8%,color-mix(in srgb,var(--accent) 10%,transparent),transparent 2.4in),linear-gradient(135deg,#fff,#eee9df);background-size:auto,auto}}
.work::after{{display:none}}
.section-head{{position:relative;z-index:3;display:grid;grid-template-columns:.94fr 1.06fr;gap:.36in;align-items:end;margin-top:.25in;padding-bottom:.22in;border-bottom:1px solid rgba(21,21,21,.13)}}
.eyebrow{{margin:0 0 10px;color:var(--accent);font-size:8px;font-weight:950;letter-spacing:.23em;text-transform:uppercase}}
h2{{font-family:"Arial Narrow","Helvetica Neue",Arial,sans-serif;font-size:40px;line-height:.94;font-weight:950;letter-spacing:-.04em;text-transform:uppercase;color:#151515}}
.intro{{margin:0;color:#4a4946;font-size:12.2px;line-height:1.6}}
.creative-grid{{position:relative;z-index:3;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:.34in}}
.creative-card{{position:relative;min-height:1.82in;border:1px solid rgba(21,21,21,.12);background:linear-gradient(145deg,#fff,rgba(243,239,231,.94));padding:18px;box-shadow:0 14px 34px rgba(8,9,13,.055)}}
.creative-card::before{{content:"";position:absolute;left:0;top:0;width:4px;height:100%;background:linear-gradient(180deg,var(--accent),var(--accent-2))}}
.num{{display:inline-grid;width:.42in;height:.42in;place-items:center;margin-bottom:12px;border:1px solid color-mix(in srgb,var(--accent) 42%,transparent);border-radius:6px;color:var(--accent);font-size:12px;font-weight:950}}
h3{{font-size:15px;line-height:1.12;color:#151515;font-weight:850;letter-spacing:-.01em}}
.creative-card p,.asset-card p{{margin:9px 0 0;color:#3f3e3b;font-size:10.6px;line-height:1.55}}
.content-stack{{position:relative;z-index:3;display:grid;gap:12px;margin-top:.31in}}
.asset-card{{display:grid;grid-template-columns:.48in 1fr;gap:15px;padding:17px 18px;border:1px solid rgba(21,21,21,.12);background:linear-gradient(135deg,#fff,rgba(244,240,232,.94));box-shadow:0 12px 30px rgba(8,9,13,.055)}}
.asset-card .eyebrow{{margin-bottom:7px;color:#68645e;font-size:7.5px;letter-spacing:.18em}}
.asset-card h3{{font-size:16.5px}}
.asset-card .num{{margin:0;background:#11131a;color:#fff;border-color:color-mix(in srgb,var(--accent) 44%,transparent)}}
.feature-page{{background:linear-gradient(135deg,#08090d,var(--deep))}}
.feature-page::before{{background:radial-gradient(circle at 78% 20%,color-mix(in srgb,var(--accent) 20%,transparent),transparent 2.4in),linear-gradient(135deg,rgba(255,255,255,.035),transparent 48%)}}
.feature-page h2,.feature-page h3{{color:#f8f5ef}}
.feature-page .intro,.feature-page .asset-card p,.feature-page .creative-card p{{color:rgba(248,245,239,.82)}}
.feature-page .asset-card,.feature-page .creative-card{{background:rgba(255,255,255,.075);border-color:rgba(248,245,239,.16);box-shadow:none}}
.feature-page .asset-card .eyebrow{{color:color-mix(in srgb,var(--accent) 72%,#fff)}}
.feature-page .brand,.feature-page .footer{{color:rgba(248,245,239,.54)}}
@media print{{body{{background:white}}.book{{width:auto;margin:0}}}}
"""


def render_creative_event_cards(blocks: list[tuple[str, str]], family: str, start_index: int = 1) -> str:
    cards: list[tuple[str, str]] = []
    if family == "interiors":
        current_title = "Design Asset"
    elif family == "speaker":
        current_title = "Speaker Asset"
    elif family == "studio":
        current_title = "Creative Asset"
    else:
        current_title = "Experience Asset"
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_body
        if current_body:
            for piece in split_card_body(" ".join(current_body)):
                cards.append((current_title, piece))
            current_body = []

    for kind, text in blocks:
        if kind == "h":
            flush()
            current_title = title_case(text)
        else:
            current_body.append(text)
    flush()

    if not cards:
        cards = [(current_title, "Customize this asset for the client type, creative offer, timeline, and next booking touchpoint.")]

    if family == "interiors":
        eyebrow = "Design asset"
    elif family == "speaker":
        eyebrow = "Speaker asset"
    elif family == "studio":
        eyebrow = "Studio asset"
    else:
        eyebrow = "Experience asset"
    pieces = []
    for offset, (card_title, body) in enumerate(cards, start=start_index):
        pieces.append(
            f"""
    <article class="asset-card">
      <div class="num">{offset:02d}</div>
      <div>
        <p class="eyebrow">{eyebrow}</p>
        <h3>{html.escape(card_title)}</h3>
        <p>{html.escape(body)}</p>
      </div>
    </article>"""
        )
    return "\n".join(pieces)


def build_creative_event_html(niche: str, title: str, descriptor: str, theme: dict[str, str], blocks: list[tuple[str, str]]) -> str:
    title_html = html.escape(title).replace("AI", "<em>AI</em>")
    chunks = chunk_blocks(blocks, max_chars=2550)
    niche_copy = CREATIVE_EVENT_COPY.get(niche, CREATIVE_EVENT_COPY["Videographers"])
    family = niche_copy["family"]
    cells_html = "\n    ".join(
        f'<div class="signature-cell"><b>{number}</b><span>{html.escape(label)}</span></div>' for number, label in niche_copy["cells"]
    )
    if family == "interiors":
        guide_headline = "Turn taste into a premium client experience."
        guide_cards = [
            ("Lead with the point of view", "Make the style, process, and transformation easy for ideal clients to understand before they inquire."),
            ("Guide the consultation", "Connect inquiry replies, discovery questions, proposal follow-up, and onboarding into one elevated client path."),
            ("Show the transformation", "Turn portfolio stories, project details, testimonials, and referrals into trust-building design assets."),
        ]
    elif family == "speaker":
        guide_headline = "Turn your message into booked stages."
        guide_cards = [
            ("Lead with the promise", "Make the audience outcome, speaker angle, and event value clear before anyone reads the full pitch."),
            ("Package authority", "Connect one-sheets, bios, talk descriptions, and proof into a confident speaker brand system."),
            ("Follow up like a pro", "Use organizer emails, nurture content, and post-event assets to create more stage opportunities."),
        ]
    elif family == "studio":
        guide_headline = "Turn creative attention into booked work."
        guide_cards = [
            ("Lead with the point of view", "Use language that makes the creative style, process, and outcome easy for the right client to recognize."),
            ("Guide the client decision", "Connect inquiry replies, proposals, questionnaires, and follow-ups into one polished buying experience."),
            ("Show proof with intention", "Turn portfolio work, testimonials, and behind-the-scenes content into trust-building conversion assets."),
        ]
    else:
        guide_headline = "Turn beautiful moments into booked experiences."
        guide_cards = [
            ("Clarify the vision", "Help clients understand the feel, timeline, investment, and next step before they become overwhelmed."),
            ("Make the experience feel premium", "Use polished communication, questionnaires, and planning assets to make the service feel high-touch."),
            ("Build referral momentum", "Turn vendor relationships, client delight, and post-event follow-up into repeatable demand."),
        ]
    guide_cards_html = "\n    ".join(
        f'<article class="creative-card"><div class="num">0{index}</div><h3>{html.escape(title_)}</h3><p>{html.escape(body)}</p></article>'
        for index, (title_, body) in enumerate(guide_cards, start=1)
    )
    pages = [
        f"""<section class="page">
  <div class="brand">
    <div></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <p class="cover-kicker">{html.escape(niche_copy["kicker"])}</p>
  <h1>{title_html}</h1>
  <p class="lead">{html.escape(niche_copy["lead"])}</p>
  <div class="signature-strip">
    {cells_html}
  </div>
  <div class="footer"><span>Content Elevated</span><span>01</span></div>
</section>""",
        f"""<section class="page work">
  <div class="brand">
    <div></div>
    <div class="badge">Creative Notes</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">Use the system</p><h2>{guide_headline}</h2></div>
    <p class="intro">{html.escape(niche_copy["intro"])}</p>
  </div>
  <div class="creative-grid">
    {guide_cards_html}
  </div>
  <div class="footer"><span>{html.escape(title)}</span><span>02</span></div>
</section>""",
    ]

    for page_index, chunk in enumerate(chunks, start=3):
        page_class = "page work feature-page" if page_index % 3 == 0 else "page work"
        pages.append(
            f"""<section class="{page_class}">
  <div class="brand">
    <div></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">{html.escape(descriptor)}</p><h2>{html.escape(title)}</h2></div>
    <p class="intro">Use these assets to make the offer clearer, the client journey more polished, and the next booking step easier to take.</p>
  </div>
  <div class="content-stack">{render_creative_event_cards(chunk, family)}</div>
  <div class="footer"><span>{html.escape(title)}</span><span>{page_index:02d}</span></div>
</section>"""
        )

    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{html.escape(title)}</title><style>{creative_event_css(theme, family)}</style></head><body><main class=\"book\">"
        + "\n".join(pages)
        + "</main></body></html>"
    )


def build_professional_service_html(niche: str, title: str, descriptor: str, theme: dict[str, str], blocks: list[tuple[str, str]]) -> str:
    title_html = html.escape(title).replace("AI", "<em>AI</em>")
    chunks = chunk_blocks(blocks, max_chars=2550)
    brand = html.escape(niche)
    pages = [
        f"""<section class="page professional-cover">
  <div class="brand">
    <div></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <p class="cover-kicker">Authority · trust · client growth</p>
  <h1>{title_html}</h1>
  <p class="lead">A refined client-growth system for turning expertise into clearer communication, better follow-up, stronger referral touchpoints, and more trusted advisory relationships.</p>
  <div class="memo-strip">
    <div class="memo-cell"><b>01</b><span>Clarify the client conversation</span></div>
    <div class="memo-cell"><b>02</b><span>Follow up with more authority</span></div>
    <div class="memo-cell"><b>03</b><span>Build trust before the consult</span></div>
  </div>
  <div class="footer"><span>Content Elevated</span><span>01</span></div>
</section>""",
        f"""<section class="page work">
  <div class="brand">
    <div></div>
    <div class="badge">Advisor Notes</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">Use the system</p><h2>Make expertise easier to trust.</h2></div>
    <p class="intro">Start with the asset closest to the next client moment: inquiry response, consultation follow-up, referral nurture, renewal conversation, education content, or retention touchpoint.</p>
  </div>
  <div class="advisory-grid">
    <article class="advisory-card"><div class="num">01</div><h3>Lead with context</h3><p>Adapt each asset around the client’s situation, risk, urgency, and decision stage.</p></article>
    <article class="advisory-card"><div class="num">02</div><h3>Sound clear, not canned</h3><p>Keep the structure, then add the details that prove the client was heard.</p></article>
    <article class="advisory-card"><div class="num">03</div><h3>Review before sending</h3><p>Check every client-facing asset for accuracy, compliance, and professional tone.</p></article>
  </div>
  <div class="footer"><span>{html.escape(title)}</span><span>02</span></div>
</section>""",
    ]

    for page_index, chunk in enumerate(chunks, start=3):
        page_class = "page work private-page" if page_index % 3 == 0 else "page work"
        pages.append(
            f"""<section class="{page_class}">
  <div class="brand">
    <div></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">{html.escape(descriptor)}</p><h2>{html.escape(title)}</h2></div>
    <p class="intro">Use these assets to make client communication clearer, more consistent, and easier to act on.</p>
  </div>
  <div class="content-stack">{render_professional_cards(chunk)}</div>
  <div class="footer"><span>{html.escape(title)}</span><span>{page_index:02d}</span></div>
</section>"""
        )

    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{html.escape(title)}</title><style>{professional_service_css(theme)}</style></head><body><main class=\"book\">"
        + "\n".join(pages)
        + "</main></body></html>"
    )


def bespoke_css(theme: dict[str, str], family: str) -> str:
    accent = theme["accent"]
    accent2 = theme["accent2"]
    dark = theme["dark"]
    paper = theme["paper"]
    return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --ink:#151716;
  --muted:#5f665f;
  --paper:{paper};
  --paper-2:#efe8dc;
  --line:rgba(21,23,22,.13);
  --accent:{accent};
  --accent-2:{accent2};
  --deep:{dark};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#ddd7cf;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;overflow:hidden;page-break-after:always;padding:.58in;background:linear-gradient(135deg,var(--paper),#fff 54%,var(--paper-2))}}
.page::before{{content:"";position:absolute;inset:.32in;border:1px solid var(--line);pointer-events:none}}
.page::after{{content:"";position:absolute;right:-.9in;top:.58in;width:3.5in;height:8.7in;background:linear-gradient(180deg,color-mix(in srgb,var(--accent) 14%,transparent),transparent 68%);transform:skewX(-8deg);opacity:.72;pointer-events:none}}
.brand{{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-start;color:rgba(21,23,22,.62);font-size:9px;font-weight:900;letter-spacing:.24em;text-transform:uppercase}}
.badge{{border:1px solid color-mix(in srgb,var(--accent) 26%,transparent);background:rgba(255,255,255,.66);padding:10px 14px;color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}}
.cover-kicker{{position:relative;z-index:3;margin-top:.82in;display:flex;align-items:center;gap:12px;color:var(--accent);font-size:10px;font-weight:950;letter-spacing:.27em;text-transform:uppercase}}
.cover-kicker::before{{content:"";width:.5in;height:1px;background:var(--accent)}}
h1,h2,h3{{position:relative;z-index:3;margin:0}}
h1{{max-width:6.18in;margin-top:.2in;font-family:Georgia,"Times New Roman",serif;font-size:58px;line-height:.96;font-weight:400;letter-spacing:-.05em;color:var(--ink)}}
h1 em,h2 em{{font-style:italic;color:var(--accent)}}
.lead{{position:relative;z-index:3;max-width:5.2in;margin-top:.28in;color:#434842;font-size:15px;line-height:1.64}}
.signature-strip{{position:absolute;z-index:3;left:.58in;right:.58in;bottom:.88in;display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:rgba(255,255,255,.48)}}
.signature-cell{{min-height:.92in;padding:16px 15px;border-left:1px solid var(--line)}}
.signature-cell:first-child{{border-left:0}}
.signature-cell b{{display:block;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:23px;font-weight:400;line-height:1}}
.signature-cell span{{display:block;margin-top:9px;color:#697069;font-size:8.3px;font-weight:850;letter-spacing:.14em;line-height:1.5;text-transform:uppercase}}
.footer{{position:absolute;z-index:3;left:.58in;right:.58in;bottom:.42in;display:flex;justify-content:space-between;color:rgba(21,23,22,.52);font-size:8px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}}
.work{{background:linear-gradient(135deg,#fff,var(--paper) 62%,var(--paper-2));color:var(--ink)}}
.work::before{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 84% 8%,color-mix(in srgb,var(--accent-2) 22%,transparent),transparent 2.45in);pointer-events:none}}
.work::after{{display:none}}
.section-head{{position:relative;z-index:3;display:grid;grid-template-columns:.92fr 1.08fr;gap:.38in;align-items:end;margin-top:.25in;padding-bottom:.23in;border-bottom:1px solid var(--line)}}
.eyebrow{{margin:0 0 10px;color:var(--accent);font-size:8px;font-weight:950;letter-spacing:.23em;text-transform:uppercase}}
h2{{font-family:Georgia,"Times New Roman",serif;font-size:39px;line-height:.98;font-weight:400;letter-spacing:-.045em;color:var(--ink)}}
.intro{{margin:0;color:#4b514b;font-size:12px;line-height:1.62}}
.bespoke-grid{{position:relative;z-index:3;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:.34in}}
.bespoke-card{{position:relative;min-height:1.84in;border:1px solid var(--line);background:rgba(255,255,255,.76);padding:18px;box-shadow:0 12px 28px rgba(21,23,22,.045)}}
.bespoke-card::before{{content:"";position:absolute;left:18px;right:18px;top:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--accent-2));opacity:.75}}
.num{{display:inline-grid;width:.42in;height:.42in;place-items:center;margin-bottom:12px;border:1px solid color-mix(in srgb,var(--accent) 32%,transparent);background:#fff;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:13px;font-weight:400}}
h3{{font-family:Inter,"Helvetica Neue",Arial,sans-serif;color:var(--ink);font-size:15px;line-height:1.14;font-weight:850;letter-spacing:-.01em}}
.bespoke-card p,.asset-card p{{margin:9px 0 0;color:#4b514b;font-size:10.4px;line-height:1.56}}
.content-stack{{position:relative;z-index:3;display:grid;gap:12px;margin-top:.31in}}
.asset-card{{display:grid;grid-template-columns:.48in 1fr;gap:15px;padding:17px 18px;border:1px solid var(--line);background:rgba(255,255,255,.8);box-shadow:0 10px 24px rgba(21,23,22,.04)}}
.asset-card .eyebrow{{margin-bottom:7px;color:#73786f;font-size:7.4px;letter-spacing:.17em}}
.asset-card h3{{font-size:16px}}
.asset-card .num{{margin:0;background:var(--deep);color:#fff;border-color:color-mix(in srgb,var(--accent) 36%,transparent)}}
.feature-page{{background:linear-gradient(135deg,var(--deep),color-mix(in srgb,var(--deep) 86%,#fff));color:#fff}}
.feature-page::before{{background:radial-gradient(circle at 78% 15%,color-mix(in srgb,var(--accent) 24%,transparent),transparent 2.35in),linear-gradient(135deg,rgba(255,255,255,.04),transparent 48%)}}
.feature-page h2,.feature-page h3{{color:#fff}}
.feature-page .intro,.feature-page .asset-card p,.feature-page .bespoke-card p{{color:rgba(255,255,255,.78)}}
.feature-page .asset-card,.feature-page .bespoke-card{{background:rgba(255,255,255,.075);border-color:rgba(255,255,255,.15);box-shadow:none}}
.feature-page .asset-card .eyebrow{{color:color-mix(in srgb,var(--accent-2) 74%,#fff)}}
.feature-page .brand,.feature-page .footer{{color:rgba(255,255,255,.56)}}

.family-barber{{--ink:#f5eee4;--paper:#0b0806;--paper-2:#17100c;--line:rgba(245,238,228,.16)}}
.family-barber .page{{background:linear-gradient(135deg,#070504,#15100c 58%,#0b0806)}}
.family-barber .page::before{{border-color:rgba(245,238,228,.12)}}
.family-barber .lead,.family-barber .intro,.family-barber .bespoke-card p,.family-barber .asset-card p{{color:rgba(245,238,228,.76)}}
.family-barber .bespoke-card,.family-barber .asset-card,.family-barber .signature-strip{{background:rgba(255,255,255,.055);border-color:rgba(245,238,228,.14)}}
.family-barber .work{{background:linear-gradient(135deg,#0b0806,#19110c)}}

.family-petcare{{--ink:#2b241a;--paper:#fff8ef;--paper-2:#eadbc6;--line:rgba(154,122,85,.18)}}
.family-petcare .page{{background:radial-gradient(circle at 82% 10%,rgba(216,195,164,.34),transparent 2.4in),linear-gradient(135deg,#fffdf8,#fff8ef 64%,#f0e4d1)}}
.family-petcare .page::before{{inset:.3in;border-color:rgba(154,122,85,.14);border-radius:26px}}
.family-petcare .page::after{{right:.72in;top:1.08in;width:2.15in;height:2.15in;border-radius:50%;border:1px solid rgba(154,122,85,.13);background:radial-gradient(circle,rgba(255,255,255,.6),rgba(216,195,164,.18) 62%,transparent 63%);transform:none;opacity:.72}}
.family-petcare h1,.family-petcare h2{{font-family:Georgia,"Times New Roman",serif;letter-spacing:-.04em}}
.family-petcare .lead,.family-petcare .intro,.family-petcare .bespoke-card p,.family-petcare .asset-card p{{color:#514637}}
.family-petcare .bespoke-card,.family-petcare .asset-card,.family-petcare .signature-strip{{background:rgba(255,255,255,.82);border-color:rgba(154,122,85,.16);box-shadow:0 10px 24px rgba(89,69,43,.035)}}
.family-petcare .feature-page{{background:radial-gradient(circle at 82% 10%,rgba(216,195,164,.28),transparent 2.4in),linear-gradient(135deg,#fffdf8,#fff8ef 64%,#f0e4d1);color:#2b241a}}
.family-petcare .feature-page::before{{inset:.3in;border:1px solid rgba(154,122,85,.14);border-radius:26px;background:transparent}}
.family-petcare .feature-page h2,.family-petcare .feature-page h3{{color:#2b241a}}
.family-petcare .feature-page .intro,.family-petcare .feature-page .asset-card p,.family-petcare .feature-page .bespoke-card p{{color:#514637}}
.family-petcare .feature-page .asset-card,.family-petcare .feature-page .bespoke-card{{background:rgba(255,255,255,.84);border-color:rgba(154,122,85,.16);box-shadow:0 10px 24px rgba(89,69,43,.035)}}
.family-petcare .feature-page .asset-card .eyebrow{{color:#9a7a55}}
.family-petcare .feature-page .brand,.family-petcare .feature-page .footer{{color:rgba(43,36,26,.54)}}

.family-etsy{{--ink:#132023;--paper:#fbfcfb;--paper-2:#e9f0ec;--line:rgba(79,143,148,.16)}}
.family-etsy .page::after{{transform:rotate(-6deg);background:linear-gradient(180deg,rgba(255,143,97,.16),rgba(79,143,148,.1),transparent 70%)}}
.family-etsy .bespoke-card::before{{height:4px}}

.family-coach{{--ink:#1b1d24;--paper:#fbf8f2;--paper-2:#ece5d9;--line:rgba(75,86,118,.16)}}
.family-coach .page{{background:radial-gradient(circle at 80% 10%,rgba(189,170,135,.24),transparent 2.5in),linear-gradient(135deg,#fff,#fbf8f2 62%,#ece5d9)}}
.family-coach .page::after{{right:.62in;top:1.08in;width:2.1in;height:2.1in;border:1px solid rgba(75,86,118,.12);background:radial-gradient(circle,rgba(255,255,255,.58),rgba(189,170,135,.14) 64%,transparent 65%);transform:none;border-radius:50%}}
.family-coach h1,.family-coach h2{{font-family:"Didot","Bodoni 72",Georgia,serif;letter-spacing:-.04em}}
.family-coach .lead,.family-coach .intro,.family-coach .bespoke-card p,.family-coach .asset-card p{{color:#46454c}}
.family-coach .bespoke-card,.family-coach .asset-card,.family-coach .signature-strip{{background:rgba(255,255,255,.82);border-color:rgba(75,86,118,.14);box-shadow:0 10px 24px rgba(35,36,44,.035)}}
.family-coach .feature-page{{background:radial-gradient(circle at 80% 10%,rgba(189,170,135,.22),transparent 2.5in),linear-gradient(135deg,#fff,#fbf8f2 62%,#ece5d9);color:#1b1d24}}
.family-coach .feature-page::before{{inset:.32in;border:1px solid rgba(75,86,118,.14);background:transparent}}
.family-coach .feature-page h2,.family-coach .feature-page h3{{color:#1b1d24}}
.family-coach .feature-page .intro,.family-coach .feature-page .asset-card p,.family-coach .feature-page .bespoke-card p{{color:#46454c}}
.family-coach .feature-page .asset-card,.family-coach .feature-page .bespoke-card{{background:rgba(255,255,255,.84);border-color:rgba(75,86,118,.14);box-shadow:0 10px 24px rgba(35,36,44,.035)}}
.family-coach .feature-page .asset-card .eyebrow{{color:#4b5676}}
.family-coach .feature-page .brand,.family-coach .feature-page .footer{{color:rgba(27,29,36,.54)}}

.family-childcare{{--ink:#27352f;--paper:#fffdf8;--paper-2:#eef7ef;--line:rgba(112,154,128,.18)}}
.family-childcare .page{{background:radial-gradient(circle at 82% 9%,rgba(255,210,185,.42),transparent 2.25in),radial-gradient(circle at 8% 86%,rgba(180,220,190,.28),transparent 2.15in),linear-gradient(135deg,#fffdf8,#fff9f1 54%,#eef7ef)}}
.family-childcare .page::before{{inset:.3in;border-color:rgba(112,154,128,.16);border-radius:28px}}
.family-childcare .page::after{{right:.58in;top:.95in;width:2.1in;height:2.1in;border:1px solid rgba(112,154,128,.14);background:radial-gradient(circle,rgba(255,255,255,.72),rgba(255,210,185,.22) 56%,rgba(180,220,190,.13) 57%,transparent 68%);transform:none;border-radius:38% 62% 45% 55%;opacity:.78}}
.family-childcare h1,.family-childcare h2{{font-family:Georgia,"Times New Roman",serif;letter-spacing:-.04em}}
.family-childcare .cover-kicker,.family-childcare .eyebrow{{color:#6f9f7b}}
.family-childcare .badge{{color:#6f9f7b;border-color:rgba(112,154,128,.22);background:rgba(255,255,255,.72)}}
.family-childcare .num{{border-radius:999px;border-color:rgba(112,154,128,.24);color:#6f9f7b;background:#fffefb}}
.family-childcare .lead,.family-childcare .intro,.family-childcare .bespoke-card p,.family-childcare .asset-card p{{color:#526159}}
.family-childcare .signature-cell b{{color:#6f9f7b}}
.family-childcare .signature-cell span{{color:#718077}}
.family-childcare .bespoke-card,.family-childcare .asset-card,.family-childcare .signature-strip{{background:rgba(255,255,255,.88);border-color:rgba(112,154,128,.15);box-shadow:0 12px 28px rgba(74,105,86,.04)}}
.family-childcare .bespoke-card::before{{height:2px;background:linear-gradient(90deg,#6f9f7b,#f0b8a1);opacity:.52}}
.family-childcare .asset-card .num{{background:#eaf5ec;color:#527b61}}
.family-childcare .feature-page{{background:radial-gradient(circle at 82% 9%,rgba(255,210,185,.38),transparent 2.25in),radial-gradient(circle at 8% 86%,rgba(180,220,190,.28),transparent 2.15in),linear-gradient(135deg,#fffdf8,#fff9f1 54%,#eef7ef);color:#27352f}}
.family-childcare .feature-page::before{{inset:.3in;border:1px solid rgba(112,154,128,.16);border-radius:28px;background:transparent}}
.family-childcare .feature-page h2,.family-childcare .feature-page h3{{color:#27352f}}
.family-childcare .feature-page .intro,.family-childcare .feature-page .asset-card p,.family-childcare .feature-page .bespoke-card p{{color:#526159}}
.family-childcare .feature-page .asset-card,.family-childcare .feature-page .bespoke-card{{background:rgba(255,255,255,.9);border-color:rgba(112,154,128,.15);box-shadow:0 12px 28px rgba(74,105,86,.04)}}
.family-childcare .feature-page .asset-card .eyebrow{{color:#6f9f7b}}
.family-childcare .feature-page .brand,.family-childcare .feature-page .footer{{color:rgba(39,53,47,.54)}}

.family-chef{{--ink:#241711;--paper:#fff8ef;--paper-2:#efe0ca;--line:rgba(148,116,84,.18)}}
.family-chef .page::after{{background:radial-gradient(ellipse at center,rgba(210,179,130,.28),transparent 63%);transform:rotate(5deg)}}
.family-chef h1,.family-chef h2{{font-family:Georgia,"Times New Roman",serif}}

.family-stylist{{--ink:#211920;--paper:#faf6f2;--paper-2:#eaded5;--line:rgba(139,116,132,.17)}}
.family-stylist .page{{background:radial-gradient(circle at 80% 10%,rgba(200,183,163,.24),transparent 2.4in),linear-gradient(135deg,#fff,#faf6f2 62%,#eaded5)}}
.family-stylist .page::after{{right:.74in;top:1.1in;width:1.9in;height:1.9in;border:1px solid rgba(139,116,132,.14);background:radial-gradient(circle,rgba(255,255,255,.62),rgba(200,183,163,.16) 62%,transparent 63%);transform:none;border-radius:50%}}
.family-stylist h1,.family-stylist h2{{font-family:Georgia,"Times New Roman",serif;letter-spacing:-.045em}}
.family-stylist .lead,.family-stylist .intro,.family-stylist .bespoke-card p,.family-stylist .asset-card p{{color:#4f454d}}
.family-stylist .bespoke-card,.family-stylist .asset-card,.family-stylist .signature-strip{{background:rgba(255,255,255,.84);border-color:rgba(139,116,132,.15);box-shadow:0 10px 24px rgba(58,42,54,.035)}}
.family-stylist .bespoke-card::before{{height:1px;opacity:.48}}
.family-stylist .num{{border-radius:999px}}
.family-stylist .feature-page{{background:radial-gradient(circle at 80% 10%,rgba(200,183,163,.22),transparent 2.4in),linear-gradient(135deg,#fff,#faf6f2 62%,#eaded5);color:#211920}}
.family-stylist .feature-page::before{{inset:.32in;border:1px solid rgba(139,116,132,.15);background:transparent}}
.family-stylist .feature-page h2,.family-stylist .feature-page h3{{color:#211920}}
.family-stylist .feature-page .intro,.family-stylist .feature-page .asset-card p,.family-stylist .feature-page .bespoke-card p{{color:#4f454d}}
.family-stylist .feature-page .asset-card,.family-stylist .feature-page .bespoke-card{{background:rgba(255,255,255,.86);border-color:rgba(139,116,132,.15);box-shadow:0 10px 24px rgba(58,42,54,.035)}}
.family-stylist .feature-page .asset-card .eyebrow{{color:#8b7484}}
.family-stylist .feature-page .brand,.family-stylist .feature-page .footer{{color:rgba(33,25,32,.54)}}

.family-trainer{{--ink:#effaf4;--paper:#0d1514;--paper-2:#16211f;--line:rgba(200,255,95,.16)}}
.family-trainer .page{{background:linear-gradient(135deg,#0a1110,#121c1a 58%,#0d1514)}}
.family-trainer .page::after{{background:linear-gradient(180deg,rgba(200,255,95,.12),rgba(45,143,118,.18),transparent 72%)}}
.family-trainer .lead,.family-trainer .intro,.family-trainer .bespoke-card p,.family-trainer .asset-card p{{color:rgba(239,250,244,.78)}}
.family-trainer .bespoke-card,.family-trainer .asset-card,.family-trainer .signature-strip{{background:rgba(255,255,255,.055);border-color:rgba(239,250,244,.13)}}
.family-trainer .work{{background:linear-gradient(135deg,#0d1514,#16211f)}}
@media print{{body{{background:white}}.book{{width:auto;margin:0}}}}
"""

def render_bespoke_cards(blocks: list[tuple[str, str]], family: str, start_index: int = 1) -> str:
    cards: list[tuple[str, str]] = []
    current_title = "Growth Asset"

    for kind, text in blocks:
        if kind == "h":
            current_title = title_case(text)
        else:
            for piece in split_card_body(text):
                cards.append((current_title, piece))
    if not cards:
        cards = [("Growth Asset", "Customize this asset for the client type, offer, timing, and next business touchpoint.")]

    label = {
        "barber": "Chair asset",
        "petcare": "Trust asset",
        "etsy": "Shop asset",
        "coach": "Authority asset",
        "childcare": "Family asset",
        "chef": "Hospitality asset",
        "stylist": "Style asset",
        "trainer": "Performance asset",
    }.get(family, "Growth asset")

    pieces = []
    for offset, (card_title, body) in enumerate(cards, start=start_index):
        pieces.append(
            f"""
    <article class="asset-card">
      <div class="num">{offset:02d}</div>
      <div>
        <p class="eyebrow">{label}</p>
        <h3>{html.escape(card_title)}</h3>
        <p>{html.escape(body)}</p>
      </div>
    </article>"""
        )
    return "\n".join(pieces)


def build_bespoke_html(niche: str, title: str, descriptor: str, theme: dict[str, str], blocks: list[tuple[str, str]]) -> str:
    display_title = title if len(title.split()) > 2 else f"{title} {niche.replace('&', 'and')}"
    title_html = html.escape(display_title).replace("AI", "<em>AI</em>")
    chunks = chunk_blocks(blocks, max_chars=1350)
    copy = BESPOKE_COPY[niche]
    family = copy["family"]
    cells_html = "\n    ".join(
        f'<div class="signature-cell"><b>{number}</b><span>{html.escape(label)}</span></div>' for number, label in copy["cells"]
    )
    guide_cards = [
        ("Start with the buyer moment", "Use the asset that matches the next decision your client, customer, or lead needs to make."),
        ("Make it sound specific", "Swap bracketed language, services, location, timeline, pricing context, and proof so the system feels built for the business."),
        ("Create one weekly rhythm", "Batch content, follow-ups, prompts, and client messages together so execution feels simple instead of scattered."),
    ]
    guide_cards_html = "\n    ".join(
        f'<article class="bespoke-card"><div class="num">0{index}</div><h3>{html.escape(title_)}</h3><p>{html.escape(body)}</p></article>'
        for index, (title_, body) in enumerate(guide_cards, start=1)
    )
    pages = [
        f"""<section class="page">
  <div class="brand">
    <div></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <p class="cover-kicker">{html.escape(copy["kicker"])}</p>
  <h1>{title_html}</h1>
  <p class="lead">{html.escape(copy["lead"])}</p>
  <div class="signature-strip">
    {cells_html}
  </div>
  <div class="footer"><span>Content Elevated</span><span>01</span></div>
</section>""",
        f"""<section class="page work">
  <div class="brand">
    <div></div>
    <div class="badge">Use the System</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">Implementation</p><h2>Make the system feel made for the niche.</h2></div>
    <p class="intro">{html.escape(copy["intro"])}</p>
  </div>
  <div class="bespoke-grid">
    {guide_cards_html}
  </div>
  <div class="footer"><span>{html.escape(display_title)}</span><span>02</span></div>
</section>""",
    ]
    for page_index, chunk in enumerate(chunks, start=3):
        page_class = "page work feature-page" if page_index % 3 == 0 else "page work"
        pages.append(
            f"""<section class="{page_class}">
  <div class="brand">
    <div></div>
    <div class="badge">{html.escape(descriptor)}</div>
  </div>
  <div class="section-head">
    <div><p class="eyebrow">{html.escape(descriptor)}</p><h2>{html.escape(display_title)}</h2></div>
    <p class="intro">Use these assets to sharpen the offer, improve the client journey, and make the next action easier to take.</p>
  </div>
  <div class="content-stack">{render_bespoke_cards(chunk, family)}</div>
  <div class="footer"><span>{html.escape(display_title)}</span><span>{page_index:02d}</span></div>
</section>"""
        )

    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{html.escape(display_title)}</title><style>{bespoke_css(theme, family)}</style></head><body><main class=\"book family-{family}\">"
        + "\n".join(pages)
        + "</main></body></html>"
    )


def source_niche(path: Path) -> str:
    rel = path.relative_to(SOURCE_ROOT)
    return rel.parts[0]


def display_title(path: Path, niche: str) -> str:
    stem = re.sub(r"^\d+_", "", path.stem)
    stem = stem.replace("90Day", "90 Day").replace("LM_", "Free ")
    stem = stem.replace("_", " ")
    for suffix in [niche, niche.replace("&", "and"), niche.rstrip("s")]:
        if stem.lower().endswith(" " + suffix.lower()):
            stem = stem[: -len(suffix)].strip()
    title = title_case(" ".join(stem.split()))
    if title.lower() in {"ai playbook", "brand kit", "email templates", "communication templates", "client templates", "patient templates"}:
        title = f"{title} {title_case(niche.replace('&', 'and'))}"
    return title


def classify(path: Path) -> str:
    name = path.name.lower()
    if name.startswith("lm_"):
        return "Lead Magnet"
    if any(item in name for item in ["90day", "90_day", "90-day", "social_calendar", "content_calendar"]):
        return "90-Day Calendar"
    if "ai_playbook" in name or "prompt" in name:
        return "AI Playbook"
    if "brand_kit" in name:
        return "Brand Kit"
    if "email" in name or "communication" in name or "template" in name:
        return "Templates"
    return "Growth System"


def is_calendar(path: Path) -> bool:
    return classify(path) == "90-Day Calendar"


def split_calendar(blocks: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    if len(blocks) < 6:
        return [blocks]
    third = max(1, len(blocks) // 3)
    return [blocks[:third], blocks[third : third * 2], blocks[third * 2 :]]


def build_html(niche: str, title: str, descriptor: str, theme: dict[str, str], blocks: list[tuple[str, str]]) -> str:
    if is_professional_service_niche(niche):
        return build_professional_service_html(niche, title, descriptor, theme, blocks)

    if is_health_wellness_niche(niche):
        return build_health_wellness_html(niche, title, descriptor, theme, blocks)

    if is_creative_event_niche(niche):
        return build_creative_event_html(niche, title, descriptor, theme, blocks)

    if is_home_service_niche(niche):
        return build_home_service_html(niche, title, descriptor, theme, blocks)

    if is_beauty_niche(niche):
        return build_beauty_html(niche, title, descriptor, theme, blocks)

    if is_bespoke_niche(niche):
        return build_bespoke_html(niche, title, descriptor, theme, blocks)

    title_html = html.escape(title).replace("AI", "<em>AI</em>")
    chunks = chunk_blocks(blocks)
    pages = [
        f"""<section class="page cover">
  <div class="brand">
    <div class="brand-stack">
      <div class="brand-line">CONTENT ELEVATED</div>
      <div class="doc-label">Done-for-you {html.escape(descriptor.lower())} for {html.escape(niche.lower())}</div>
    </div>
  </div>
  <h1>{title_html}</h1>
  <p class="lead">A premium, niche-specific growth system built to help the business move faster with clearer content, stronger client touchpoints, and ready-to-use execution assets.</p>
  <div class="metrics">
    <div class="metric"><b>01</b><span>Ready-to-use<br/>growth system</span></div>
    <div class="metric"><b>02</b><span>Designed for<br/>{html.escape(theme["tag"])}</span></div>
    <div class="metric"><b>03</b><span>Customize<br/>and launch</span></div>
  </div>
  <div class="footer"><span>{html.escape(niche)} product file</span><span>01</span></div>
</section>""",
        f"""<section class="page work direction-page">
  <div class="brand"><div>Content Elevated</div><div></div></div>
  <div class="section-head">
    <div><p class="eyebrow">Implementation Notes</p><h2>Turn this file into action.</h2></div>
    <p class="intro">Use this section to move from strategy into execution with clear steps, customized language, and a simple weekly workflow.</p>
  </div>
  <div class="prompt-grid">
    <article class="prompt-card"><div class="num">01</div><div><p class="eyebrow">Review</p><h3>Skim the system</h3><p>Read the file once for strategy, workflow, and context before customizing any client-facing language.</p></div></article>
    <article class="prompt-card"><div class="num">02</div><div><p class="eyebrow">Customize</p><h3>Make it specific</h3><p>Replace brackets, niche details, service names, offers, and client language with the business details.</p></div></article>
    <article class="prompt-card"><div class="num">03</div><div><p class="eyebrow">Use</p><h3>Put it in motion</h3><p>Move finished prompts, templates, calendars, and scripts into the weekly operating workflow.</p></div></article>
  </div>
  <div class="footer"><span>{html.escape(title)}</span><span>02</span></div>
</section>""",
    ]
    for index, chunk in enumerate(chunks, start=3):
        pages.append(
            f"""<section class="page work direction-page">
  <div class="brand"><div>Content Elevated</div><div></div></div>
  <div class="section-head">
    <div><p class="eyebrow">{html.escape(descriptor)}</p><h2>{html.escape(title)}</h2></div>
    <p class="intro">Working pages designed to keep the strategy clear, usable, and easy to customize for the business.</p>
  </div>
  <div class="content-stack">{render_content_cards(chunk)}</div>
  <div class="footer"><span>{html.escape(title)}</span><span>{index:02d}</span></div>
</section>"""
        )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{html.escape(title)}</title><style>{css(theme)}</style></head><body><main class=\"book layout-{html.escape(theme['layout'])}\">"
        + "\n".join(pages)
        + "</main></body></html>"
    )


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.relative_to(SOURCE_ROOT).parts)


def write_pdf_html(path: Path) -> list[Path]:
    niche = source_niche(path)
    if niche.startswith("_"):
        return []
    theme = theme_for(niche)
    title = theme["headline"] if path.name.startswith("LM_") else display_title(path, niche)
    descriptor = classify(path)
    lines = clean_lines(pdf_text(path), niche)
    blocks = paragraphize(lines)
    if not blocks:
        blocks = [("p", "This source file did not expose extractable text. Keep the original nearby for manual review.")]

    rel = path.relative_to(SOURCE_ROOT)
    nested_parts = rel.parts[1:-1]
    out_dir = OUTPUT_ROOT / slugify(niche)
    if nested_parts:
        out_dir = out_dir.joinpath(*(slugify(part) for part in nested_parts))
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    if is_calendar(path):
        for index, part in enumerate(split_calendar(blocks), start=1):
            month_title = f"{title} · Month {index}"
            out = out_dir / f"{slugify(path.stem)}-month-{index}.html"
            out.write_text(build_html(niche, month_title, descriptor, theme, part), encoding="utf-8")
            written.append(out)
    else:
        out = out_dir / f"{slugify(path.stem)}.html"
        out.write_text(build_html(niche, title, descriptor, theme, blocks), encoding="utf-8")
        written.append(out)
    return written


def copy_spreadsheet(path: Path) -> Path | None:
    if should_skip(path):
        return None
    niche = source_niche(path)
    out_dir = OUTPUT_ROOT / slugify(niche) / "spreadsheets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / path.name
    shutil.copy2(path, out)
    return out


def make_index(outputs: list[Path], spreadsheets: list[Path]) -> None:
    groups: dict[str, list[Path]] = {}
    for path in outputs:
        groups.setdefault(path.parent.name, []).append(path)
    spreadsheet_groups: dict[str, list[Path]] = {}
    for path in spreadsheets:
        spreadsheet_groups.setdefault(path.parent.parent.name, []).append(path)

    sections = []
    for slug in sorted(set(groups) | set(spreadsheet_groups)):
        links = "\n".join(
            f'<li><a href="{path.relative_to(OUTPUT_ROOT).as_posix()}">{html.escape(path.name)}</a></li>'
            for path in sorted(groups.get(slug, []))
        )
        sheet_links = "\n".join(
            f'<li><a href="{path.relative_to(OUTPUT_ROOT).as_posix()}">{html.escape(path.name)}</a></li>'
            for path in sorted(spreadsheet_groups.get(slug, []))
        )
        sections.append(f"<section><h2>{html.escape(title_case(slug.replace('-', ' ')))}</h2><ul>{links}{sheet_links}</ul></section>")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "index.html").write_text(
        """<!doctype html><html><head><meta charset="utf-8"/><title>Rebranded Products</title>
<style>body{margin:0;background:#08090b;color:#f4f6f8;font-family:Inter,Arial,sans-serif;padding:48px}main{max-width:1180px;margin:auto}h1{font-size:48px;letter-spacing:-.05em}section{border:1px solid rgba(255,255,255,.12);border-radius:22px;padding:24px;margin:18px 0;background:rgba(255,255,255,.035)}h2{margin:0 0 12px}a{color:#9fdfff;text-decoration:none}li{margin:7px 0;color:#8190a2}</style></head><body><main><h1>Content Elevated Rebranded Products</h1><p>Updated product files plus spreadsheet files preserved in their matching folders.</p>"""
        + "\n".join(sections)
        + "</main></body></html>",
        encoding="utf-8",
    )


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    spreadsheets: list[Path] = []
    for path in sorted(SOURCE_ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue
        if path.suffix.lower() == ".pdf":
            outputs.extend(write_pdf_html(path))
        elif path.suffix.lower() in SPREADSHEET_EXTENSIONS:
            copied = copy_spreadsheet(path)
            if copied:
                spreadsheets.append(copied)
    make_index(outputs, spreadsheets)
    print(f"Created {len(outputs)} product files.")
    print(f"Copied {len(spreadsheets)} spreadsheets.")
    print(OUTPUT_ROOT / "index.html")


if __name__ == "__main__":
    main()
