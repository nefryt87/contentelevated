from __future__ import annotations

import html
import re
from pathlib import Path

from pypdf import PdfReader


SOURCE_ROOT = Path("/Users/tomasz/Documents/Content Elevated/Content Elevated Products")
OUT_ROOT = Path(
    "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/print-ready-pdfs/sample-documents"
)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower().replace("&", "and")).strip("-")


def title_case(value: str) -> str:
    return value.title().replace("Ai", "AI").replace("Cpa", "CPA").replace("Hvac", "HVAC").replace("Seo", "SEO")


STYLE_BY_NICHE: dict[str, dict[str, str]] = {
    "Accountants & CPAs": {
        "headline": "5 AI Prompts for a Sharper Practice",
        "mood": "Ledger-clean advisory authority",
        "accent": "#5f7f86",
        "accent2": "#a8bab5",
        "paper": "#fbfaf4",
        "dark": "#161b1f",
        "layout": "ledger",
        "tag": "CPA",
    },
    "Aestheticians": {
        "headline": "5 AI Prompts for a Fully Booked Skin Studio",
        "mood": "Pearl clinical luxury",
        "accent": "#7d9a88",
        "accent2": "#dac9b5",
        "paper": "#fbfaf5",
        "dark": "#17211c",
        "layout": "protocol",
        "tag": "Skin",
    },
    "Attorneys": {
        "headline": "5 AI Prompts for a More Trusted Firm",
        "mood": "Modern legal confidence",
        "accent": "#6c7481",
        "accent2": "#c2b08a",
        "paper": "#f8f6f1",
        "dark": "#17191d",
        "layout": "ledger",
        "tag": "Legal",
    },
    "Barbers": {
        "headline": "5 Free AI Prompts to Fill Your Chair",
        "mood": "Dark shop culture",
        "accent": "#c8963d",
        "accent2": "#2a2d2d",
        "paper": "#0a0807",
        "dark": "#080706",
        "layout": "dark-shop",
        "tag": "Barber",
    },
    "Bridal Hair & Makeup Artists": {
        "headline": "5 AI Prompts for Bridal Booking Flow",
        "mood": "Romantic studio polish",
        "accent": "#b9878d",
        "accent2": "#dfc1b5",
        "paper": "#fff8f5",
        "dark": "#24191b",
        "layout": "editorial",
        "tag": "Bridal",
    },
    "Car Wash Businesses": {
        "headline": "5 AI Prompts for Membership Growth",
        "mood": "Glossy local service energy",
        "accent": "#3e9ac4",
        "accent2": "#8ed3f2",
        "paper": "#f2f9fc",
        "dark": "#0b1820",
        "layout": "field",
        "tag": "Wash",
    },
    "Chiropractors": {
        "headline": "5 AI Prompts for Patient Retention",
        "mood": "Wellness clinic trust",
        "accent": "#748d7a",
        "accent2": "#b9c9bc",
        "paper": "#f8faf5",
        "dark": "#182019",
        "layout": "protocol",
        "tag": "Care",
    },
    "Dentists": {
        "headline": "5 AI Prompts for a Better Patient Flow",
        "mood": "Clean clinical confidence",
        "accent": "#6e9eaa",
        "accent2": "#d7e8e8",
        "paper": "#f8fcfb",
        "dark": "#142023",
        "layout": "protocol",
        "tag": "Dental",
    },
    "Dog Walkers & Pet Sitters": {
        "headline": "5 AI Prompts for More Repeat Clients",
        "mood": "Warm neighborhood trust",
        "accent": "#9a7a55",
        "accent2": "#d8c3a4",
        "paper": "#fff8ef",
        "dark": "#211a13",
        "layout": "cards",
        "tag": "Local",
    },
    "Electricians": {
        "headline": "5 AI Prompts for More Service Calls",
        "mood": "Technical service precision",
        "accent": "#4d9dc9",
        "accent2": "#f1b84f",
        "paper": "#f2f8fb",
        "dark": "#101820",
        "layout": "field",
        "tag": "Power",
    },
    "Etsy Sellers": {
        "headline": "5 AI Prompts for a Stronger Shop",
        "mood": "Maker-commerce launch board",
        "accent": "#4f8f94",
        "accent2": "#ff8f61",
        "paper": "#fbfcfb",
        "dark": "#11191b",
        "layout": "commerce",
        "tag": "Shop",
    },
    "Event Planners": {
        "headline": "5 AI Prompts for Better Event Bookings",
        "mood": "Polished planning studio",
        "accent": "#9170a0",
        "accent2": "#d6b98f",
        "paper": "#fbf7f4",
        "dark": "#201823",
        "layout": "editorial",
        "tag": "Events",
    },
    "Financial Advisors": {
        "headline": "5 AI Prompts for Client Confidence",
        "mood": "Quiet wealth advisory",
        "accent": "#61798b",
        "accent2": "#aebdb8",
        "paper": "#f8f8f2",
        "dark": "#171d22",
        "layout": "ledger",
        "tag": "Wealth",
    },
    "Florists": {
        "headline": "5 AI Prompts for More Floral Orders",
        "mood": "Botanical boutique editorial",
        "accent": "#8b765d",
        "accent2": "#c9aeb6",
        "paper": "#fff8f3",
        "dark": "#211916",
        "layout": "editorial",
        "tag": "Floral",
    },
    "HVAC Contractors": {
        "headline": "5 AI Prompts for More HVAC Calls",
        "mood": "Blueprint field system",
        "accent": "#37a8e6",
        "accent2": "#f1853e",
        "paper": "#f4fbff",
        "dark": "#0d1a28",
        "layout": "field",
        "tag": "HVAC",
    },
    "Hair Stylists": {
        "headline": "5 AI Prompts for Rebooking More Clients",
        "mood": "Soft salon revenue system",
        "accent": "#b98378",
        "accent2": "#e2b9aa",
        "paper": "#fff7f3",
        "dark": "#241a1a",
        "layout": "editorial",
        "tag": "Salon",
    },
    "Insurance Agents": {
        "headline": "5 AI Prompts for More Policy Conversations",
        "mood": "Practical trust and protection",
        "accent": "#667f95",
        "accent2": "#b6c2cc",
        "paper": "#f7f9fb",
        "dark": "#151c24",
        "layout": "ledger",
        "tag": "Policy",
    },
    "Interior Designers": {
        "headline": "5 AI Prompts for Premium Design Leads",
        "mood": "Architectural editorial",
        "accent": "#8d7a69",
        "accent2": "#cab8a3",
        "paper": "#faf5ef",
        "dark": "#1c1713",
        "layout": "editorial",
        "tag": "Design",
    },
    "Lash Technicians": {
        "headline": "5 AI Prompts for More Lash Clients",
        "mood": "Beauty appointment polish",
        "accent": "#a77c85",
        "accent2": "#dcc0c4",
        "paper": "#fff7f8",
        "dark": "#23191d",
        "layout": "editorial",
        "tag": "Lash",
    },
    "Life & Business Coaches": {
        "headline": "5 AI Prompts for Better Discovery Calls",
        "mood": "Clear expertise-led growth",
        "accent": "#7e819b",
        "accent2": "#d0b98d",
        "paper": "#f8f6f1",
        "dark": "#1b1d27",
        "layout": "cards",
        "tag": "Coach",
    },
    "Makeup Artists": {
        "headline": "5 AI Prompts for More Makeup Bookings",
        "mood": "Modern glam studio",
        "accent": "#ba7b83",
        "accent2": "#e2b7ac",
        "paper": "#fff7f5",
        "dark": "#24191b",
        "layout": "editorial",
        "tag": "MUA",
    },
    "Massage Therapists": {
        "headline": "5 AI Prompts for Repeat Massage Clients",
        "mood": "Calm retention wellness",
        "accent": "#798d75",
        "accent2": "#c1cbb6",
        "paper": "#f8faf2",
        "dark": "#1b2118",
        "layout": "protocol",
        "tag": "Wellness",
    },
    "Med Spas": {
        "headline": "5 AI Prompts for Med Spa Growth",
        "mood": "Clinical luxury conversion",
        "accent": "#8a927f",
        "accent2": "#d8c7ad",
        "paper": "#fbfaf5",
        "dark": "#181d18",
        "layout": "protocol",
        "tag": "Med Spa",
    },
    "Mortgage Brokers": {
        "headline": "5 AI Prompts for More Pre-Approvals",
        "mood": "Modern lending clarity",
        "accent": "#637b8c",
        "accent2": "#c4b99f",
        "paper": "#f8f7f1",
        "dark": "#171d22",
        "layout": "ledger",
        "tag": "Lending",
    },
    "Nail Technicians": {
        "headline": "5 AI Prompts for More Nail Clients",
        "mood": "Polished beauty studio",
        "accent": "#a97c84",
        "accent2": "#dfbbb7",
        "paper": "#fff7f5",
        "dark": "#22191b",
        "layout": "editorial",
        "tag": "Nails",
    },
    "Nannies & Childcare Professionals": {
        "headline": "5 AI Prompts for More Family Trust",
        "mood": "Warm professional childcare",
        "accent": "#8c7b58",
        "accent2": "#d8caaa",
        "paper": "#fff9ef",
        "dark": "#211b13",
        "layout": "cards",
        "tag": "Care",
    },
    "Nutritionists": {
        "headline": "5 AI Prompts for Better Client Plans",
        "mood": "Fresh wellness clarity",
        "accent": "#6f9274",
        "accent2": "#c8d7b9",
        "paper": "#fbfcf3",
        "dark": "#182218",
        "layout": "protocol",
        "tag": "Nutrition",
    },
    "Party Planners": {
        "headline": "5 AI Prompts for Party Bookings",
        "mood": "Playful premium planning",
        "accent": "#9670a5",
        "accent2": "#e0b05e",
        "paper": "#fbf5fb",
        "dark": "#201724",
        "layout": "cards",
        "tag": "Party",
    },
    "Personal Chefs": {
        "headline": "5 AI Prompts for Private Chef Clients",
        "mood": "Culinary hospitality editorial",
        "accent": "#947454",
        "accent2": "#d2b382",
        "paper": "#fff8ef",
        "dark": "#211712",
        "layout": "editorial",
        "tag": "Chef",
    },
    "Personal Stylists": {
        "headline": "5 AI Prompts for Styling Clients",
        "mood": "Fashion editorial confidence",
        "accent": "#8b7484",
        "accent2": "#c8b7a3",
        "paper": "#faf6f2",
        "dark": "#1e171b",
        "layout": "editorial",
        "tag": "Style",
    },
    "Personal Trainers": {
        "headline": "5 AI Prompts for More Training Clients",
        "mood": "Kinetic performance tech",
        "accent": "#2d8f76",
        "accent2": "#c8ff5f",
        "paper": "#f5f8f6",
        "dark": "#111818",
        "layout": "performance",
        "tag": "Train",
    },
    "Physical Therapists": {
        "headline": "5 AI Prompts for Patient Follow-Up",
        "mood": "Rehab clarity and trust",
        "accent": "#6e8f89",
        "accent2": "#b9cbc4",
        "paper": "#f8fbf8",
        "dark": "#17211f",
        "layout": "protocol",
        "tag": "PT",
    },
    "Plumbers": {
        "headline": "5 AI Prompts for More Plumbing Jobs",
        "mood": "Reliable local service",
        "accent": "#3f8fb3",
        "accent2": "#d0a15c",
        "paper": "#f3f8fa",
        "dark": "#101b22",
        "layout": "field",
        "tag": "Plumb",
    },
    "Public Speakers": {
        "headline": "5 AI Prompts for More Speaking Bookings",
        "mood": "Stage authority",
        "accent": "#7d7298",
        "accent2": "#d0a75d",
        "paper": "#f7f5f2",
        "dark": "#1b1824",
        "layout": "cards",
        "tag": "Stage",
    },
    "Tattoo Artists": {
        "headline": "5 AI Prompts for Tattoo Bookings",
        "mood": "Dark studio portfolio",
        "accent": "#9a6c65",
        "accent2": "#c8963d",
        "paper": "#0c0a0a",
        "dark": "#080707",
        "layout": "dark-shop",
        "tag": "Tattoo",
    },
    "Videographers": {
        "headline": "5 AI Prompts for More Video Clients",
        "mood": "Cinematic creator studio",
        "accent": "#5f86a8",
        "accent2": "#d19a62",
        "paper": "#f4f7f8",
        "dark": "#101419",
        "layout": "cards",
        "tag": "Video",
    },
    "Wedding Photographers": {
        "headline": "5 AI Prompts for Wedding Inquiries",
        "mood": "Romantic film editorial",
        "accent": "#a67a6d",
        "accent2": "#d3ad8b",
        "paper": "#fffaf6",
        "dark": "#211817",
        "layout": "editorial",
        "tag": "Photo",
    },
}


def find_sample_pdf(niche_dir: Path) -> Path | None:
    lead = sorted(niche_dir.glob("LM_*.pdf"))
    if lead:
        return lead[0]
    pdfs = sorted(niche_dir.glob("*.pdf"))
    if not pdfs:
        return None
    return sorted(pdfs, key=lambda p: (len(PdfReader(str(p)).pages), p.name))[0]


def read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages[:3])


def extract_prompts(text: str) -> list[tuple[str, str]]:
    lines = [" ".join(line.strip().split()) for line in text.splitlines() if line.strip()]
    prompts: list[tuple[str, str]] = []
    current_title = ""
    current_body: list[str] = []
    for line in lines:
        match = re.match(r"^(PROMPT|TEMPLATE)\s*(\d+)[:\s-]+(.+)$", line, re.I)
        if match:
            if current_title and current_body:
                prompts.append((current_title, " ".join(current_body)))
            current_title = title_case(match.group(3))
            current_body = []
        elif current_title:
            if line.lower().startswith("want the full system"):
                break
            current_body.append(line)
    if current_title and current_body:
        prompts.append((current_title, " ".join(current_body)))
    if prompts:
        return prompts[:5]

    fallback = []
    buffer: list[str] = []
    for line in lines:
        if line.isupper() and len(line) < 80:
            if buffer:
                fallback.append(("Action Prompt", " ".join(buffer)))
                buffer = []
        elif len(line) > 45:
            buffer.append(line)
        if len(fallback) >= 5:
            break
    if buffer and len(fallback) < 5:
        fallback.append(("Action Prompt", " ".join(buffer)))
    return fallback[:5]


def css(style: dict[str, str]) -> str:
    paper = style["paper"]
    accent = style["accent"]
    accent2 = style["accent2"]
    dark = style["dark"]
    is_dark = style["layout"] == "dark-shop"
    ink = "#f8f3e9" if is_dark else "#121415"
    muted = "rgba(248,243,233,.72)" if is_dark else "rgba(18,20,21,.62)"
    bg = dark if is_dark else paper
    display = "Georgia, 'Times New Roman', serif"
    if style["layout"] in {"field", "performance", "dark-shop"}:
        display = "'Arial Narrow', 'Helvetica Neue', Arial, sans-serif"
    elif style["layout"] == "commerce":
        display = "Inter, 'Helvetica Neue', Arial, sans-serif"
    layout = style["layout"]
    return f"""
@page {{ size: Letter; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:#d2d2cf; color:{ink}; font-family:Inter,'Helvetica Neue',Arial,sans-serif; }}
.book {{ width:8.5in; margin:0 auto; }}
.page {{ position:relative; width:8.5in; min-height:11in; overflow:hidden; page-break-after:always; padding:.58in; background:{bg}; }}
.page:before {{ content:""; position:absolute; inset:0; background:
  radial-gradient(circle at 82% 14%, color-mix(in srgb,{accent} 24%,transparent), transparent 2.35in),
  radial-gradient(circle at 12% 90%, color-mix(in srgb,{accent2} 20%,transparent), transparent 2.55in),
  linear-gradient(135deg, color-mix(in srgb,{bg} 94%,white), color-mix(in srgb,{bg} 86%,{accent})); pointer-events:none; }}
.page:after {{ content:""; position:absolute; inset:0; background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.045) 1px,transparent 1px); background-size:.42in .42in; opacity:{'.3' if is_dark else '.22'}; mask-image:radial-gradient(circle at 50% 40%,black,transparent 80%); pointer-events:none; }}
.brand {{ position:relative; z-index:3; display:flex; justify-content:space-between; align-items:flex-start; font-size:9px; font-weight:900; letter-spacing:.22em; text-transform:uppercase; color:{muted}; }}
.brand-stack {{ display:grid; gap:8px; }}
.brand-line {{ color:{ink}; letter-spacing:.26em; }}
.doc-label {{ color:{accent}; font-size:9px; letter-spacing:.22em; text-transform:uppercase; font-weight:900; }}
.tag {{ padding:9px 13px; border:1px solid color-mix(in srgb,{accent} 32%,transparent); border-radius:999px; color:{accent}; background:{'rgba(255,255,255,.035)' if is_dark else 'rgba(255,255,255,.38)'}; }}
h1 {{ position:relative; z-index:3; margin:.88in 0 0; max-width:5.6in; font-family:{display}; font-size:{'74px' if style['layout'] in {'field','performance','dark-shop'} else '54px'}; line-height:{'.84' if style['layout'] in {'field','performance','dark-shop'} else '.96'}; font-weight:{'950' if style['layout'] in {'field','performance','dark-shop','commerce'} else '400'}; letter-spacing:-.055em; text-transform:{'uppercase' if style['layout'] in {'field','performance','dark-shop'} else 'none'}; }}
.gold {{ color:{accent}; }}
.lead {{ position:relative; z-index:3; max-width:4.75in; margin-top:.28in; color:{muted}; font-size:15px; line-height:1.48; }}
.cover-linework {{ position:absolute; z-index:2; right:.58in; top:1.48in; width:3.05in; height:5.95in; border-top:1px solid color-mix(in srgb,{accent} 38%,transparent); border-bottom:1px solid color-mix(in srgb,{accent} 22%,transparent); background:
  linear-gradient(90deg, transparent, color-mix(in srgb,{accent} 11%,transparent), transparent),
  repeating-linear-gradient(90deg, rgba(255,255,255,.052) 0 1px, transparent 1px 24px);
  opacity:.7; }}
.cover-linework:after {{ content:""; position:absolute; inset:.35in; border:1px solid color-mix(in srgb,{accent} 16%,transparent); border-left:0; border-right:0; }}
.motif {{ display:none; }}
.metrics {{ position:absolute; z-index:3; left:.58in; right:2.2in; bottom:1.1in; display:grid; grid-template-columns:repeat(3,1fr); border-top:1px solid color-mix(in srgb,{accent} 52%,transparent); border-bottom:1px solid color-mix(in srgb,{accent} 32%,transparent); }}
.metric {{ min-height:1.1in; padding:16px 13px; border-right:1px solid color-mix(in srgb,{accent} 32%,transparent); }}
.metric b {{ display:block; color:{accent}; font-size:22px; margin-bottom:10px; font-family:{display}; }}
.metric span {{ display:block; color:{muted}; font-size:9px; line-height:1.55; font-weight:850; letter-spacing:.14em; text-transform:uppercase; }}
.work {{ background:{dark}; color:#f8f3e9; }}
.work:before {{ background:radial-gradient(circle at 14% 10%, color-mix(in srgb,{accent} 18%,transparent), transparent 2in), linear-gradient(135deg, {dark}, color-mix(in srgb,{dark} 78%,black)); }}
.section-head {{ position:relative; z-index:3; margin-top:.45in; display:grid; grid-template-columns:1.05fr .95fr; gap:.35in; align-items:end; }}
.eyebrow {{ margin:0 0 10px; color:{accent}; font-size:8px; font-weight:950; letter-spacing:.22em; text-transform:uppercase; }}
h2 {{ margin:0; font-family:{display}; font-size:40px; line-height:.94; font-weight:{'950' if style['layout'] in {'field','performance','dark-shop','commerce'} else '400'}; letter-spacing:-.04em; text-transform:{'uppercase' if style['layout'] in {'field','performance','dark-shop'} else 'none'}; }}
.intro {{ color:rgba(248,243,233,.7); font-size:11px; line-height:1.55; }}
.prompt-grid {{ position:relative; z-index:3; margin-top:.4in; display:grid; gap:14px; }}
.prompt-card {{ display:grid; grid-template-columns:.5in 1fr; gap:15px; padding:17px; border:1px solid color-mix(in srgb,{accent} 26%,transparent); background:linear-gradient(135deg,rgba(255,255,255,.06),rgba(255,255,255,.018)); border-radius:{'12px' if style['layout'] in {'field','commerce'} else '18px'}; box-shadow:0 18px 50px rgba(0,0,0,.18); }}
.num {{ width:.5in; height:.5in; display:grid; place-items:center; border-radius:50%; border:1px solid color-mix(in srgb,{accent} 56%,transparent); color:{accent}; font-family:Georgia,serif; font-size:14px; }}
h3 {{ margin:0 0 8px; color:#fff8ef; font-size:17px; line-height:1.1; }}
.prompt-card p {{ margin:0; color:rgba(248,243,233,.72); font-size:9.8px; line-height:1.46; }}
.footer {{ position:absolute; z-index:3; left:.58in; right:.58in; bottom:.31in; display:flex; justify-content:space-between; color:{muted}; font-size:8px; font-weight:850; letter-spacing:.16em; text-transform:uppercase; }}
.cta {{ position:relative; z-index:3; margin-top:.35in; padding:24px; border:1px solid color-mix(in srgb,{accent} 28%,transparent); border-radius:24px; background:linear-gradient(135deg,color-mix(in srgb,{accent} 12%,transparent),rgba(255,255,255,.025)); }}
.cta h2 {{ font-size:34px; }}

/* Distinct niche systems */
.layout-ledger .cover-linework {{ display:none; }}
.layout-ledger .cover {{ background:{paper}; }}
.layout-ledger .cover:after {{ background-size:.28in .28in; opacity:.32; }}
.layout-ledger .work {{ background:#f7f6ef; color:{dark}; }}
.layout-ledger .work:before {{ background:linear-gradient(135deg,#fbfaf4,#ece8dc); }}
.layout-ledger .intro,.layout-ledger .prompt-card p {{ color:rgba(20,24,26,.66); }}
.layout-ledger h3 {{ color:{dark}; }}
.layout-ledger .prompt-card {{ border-radius:0; box-shadow:none; background:rgba(255,255,255,.48); border-left:5px solid {accent}; }}

.layout-protocol .cover-linework {{ display:none; }}
.layout-protocol .cover {{ background:{paper}; }}
.layout-protocol .work {{ background:#fbfbf5; color:{dark}; }}
.layout-protocol .work:before {{ background:radial-gradient(circle at 82% 12%,color-mix(in srgb,{accent} 13%,transparent),transparent 2in),linear-gradient(135deg,#fff,#eef3ea); }}
.layout-protocol .intro,.layout-protocol .prompt-card p {{ color:rgba(20,25,22,.66); }}
.layout-protocol h3 {{ color:{dark}; }}
.layout-protocol .prompt-grid {{ grid-template-columns:1fr 1fr; }}
.layout-protocol .prompt-card:first-child {{ grid-column:span 2; }}
.layout-protocol .prompt-card {{ border-radius:22px; background:rgba(255,255,255,.7); box-shadow:0 20px 60px rgba(45,75,54,.08); }}

.layout-editorial .cover-linework {{ display:none; }}
.layout-editorial .work {{ background:#141111; }}
.layout-editorial .prompt-grid {{ grid-template-columns:1fr 1fr; }}
.layout-editorial .prompt-card:first-child {{ grid-column:span 2; }}
.layout-editorial .prompt-card {{ border-radius:30px; padding:22px; }}

.layout-field .cover-linework {{ display:none; }}
.layout-field .cover {{ background:{dark}; }}
.layout-field .metrics {{ right:.58in; }}
.layout-field .prompt-card {{ border-radius:8px; clip-path:polygon(14px 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%,0 14px); }}

.layout-performance .cover-linework {{ display:none; }}
.layout-performance .cover {{ background:#050707; }}
.layout-performance h1 {{ max-width:6.25in; font-size:82px; }}
.layout-performance .prompt-grid {{ grid-template-columns:1fr; }}
.layout-performance .prompt-card {{ border-radius:7px; background:linear-gradient(100deg,rgba(255,255,255,.06),color-mix(in srgb,{accent} 14%,transparent)); }}
.layout-performance .num {{ border-radius:8px; font-family:Inter,Arial,sans-serif; font-weight:950; }}

.layout-dark-shop .cover-linework {{ display:none; }}
.layout-dark-shop .cover {{ background:#060504; }}
.layout-dark-shop .prompt-card {{ background:linear-gradient(135deg,rgba(255,255,255,.06),rgba(0,0,0,.34)); border-radius:6px; }}

.layout-commerce .cover-linework {{ display:none; }}
.layout-commerce .cover {{ background:#f8fbf9; }}
.layout-commerce h1 {{ font-size:62px; letter-spacing:-.06em; }}
.layout-commerce .work {{ background:#f8fbf9; color:{dark}; }}
.layout-commerce .work:before {{ background:linear-gradient(135deg,#fff,color-mix(in srgb,{accent} 8%,white)); }}
.layout-commerce .intro,.layout-commerce .prompt-card p {{ color:rgba(18,24,24,.66); }}
.layout-commerce h3 {{ color:{dark}; }}
.layout-commerce .prompt-card {{ background:#fff; border-radius:20px; box-shadow:0 18px 46px rgba(0,0,0,.08); }}

.layout-cards .cover-linework {{ display:none; }}
.layout-cards .prompt-grid {{ grid-template-columns:1fr 1fr; }}
.layout-cards .prompt-card {{ border-radius:24px; }}
@media print {{ body {{ background:white; }} .book {{ margin:0; }} }}
"""


def prompt_card(index: int, title: str, body: str) -> str:
    return f"""
    <article class="prompt-card">
      <div class="num">{index:02d}</div>
      <div>
        <p class="eyebrow">Copy / paste prompt</p>
        <h3>{html.escape(title)}</h3>
        <p>{html.escape(body)}</p>
      </div>
    </article>
    """


def cover_motif(layout: str) -> str:
    return ""


def build_doc(niche: str, pdf: Path, style: dict[str, str]) -> str:
    prompts = extract_prompts(read_pdf(pdf))
    while len(prompts) < 5:
        prompts.append(("Action Prompt", "Customize this prompt with your business details, client type, and offer. Use it to move a real client conversation forward."))
    cover_title = html.escape(style["headline"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(niche)} Sample Document</title>
  <style>{css(style)}</style>
</head>
<body>
<main class="book layout-{html.escape(style["layout"])}">
  <section class="page cover">
    <div class="brand">
      <div class="brand-stack">
        <div class="brand-line">CONTENT ELEVATED</div>
        <div class="doc-label">Done-for-you AI prompts for {html.escape(niche.lower())}</div>
      </div>
    </div>
    {cover_motif(style["layout"])}
    <h1>{cover_title}</h1>
    <p class="lead">A premium, niche-specific sample document built from the real product content. Review this direction before we apply it to the full bundle.</p>
    <div class="metrics">
      <div class="metric"><b>01</b><span>Copy and paste<br/>client prompts</span></div>
      <div class="metric"><b>02</b><span>Designed for<br/>{html.escape(style["tag"])}</span></div>
      <div class="metric"><b>03</b><span>Fast to use<br/>easy to customize</span></div>
    </div>
    <div class="footer"><span>{html.escape(niche)} sample document</span><span>01</span></div>
  </section>
  <section class="page work">
    <div class="brand"><div>Content Elevated</div><div></div></div>
    <div class="section-head">
      <div><p class="eyebrow">Prompt System</p><h2>Start with the client moment.</h2></div>
      <p class="intro">Use these prompts when the customer is asking, deciding, rebooking, reviewing, or needing a reason to say yes.</p>
    </div>
    <div class="prompt-grid">
      {prompt_card(1, prompts[0][0], prompts[0][1])}
      {prompt_card(2, prompts[1][0], prompts[1][1])}
      {prompt_card(3, prompts[2][0], prompts[2][1])}
    </div>
    <div class="footer"><span>{html.escape(niche)}</span><span>02</span></div>
  </section>
  <section class="page work">
    <div class="brand"><div>Content Elevated</div><div></div></div>
    <div class="section-head">
      <div><p class="eyebrow">Follow-up / Content / Trust</p><h2>Turn attention into action.</h2></div>
      <p class="intro">This final page shows how the visual system handles longer prompt text, CTA structure, and bundle positioning.</p>
    </div>
    <div class="prompt-grid">
      {prompt_card(4, prompts[3][0], prompts[3][1])}
      {prompt_card(5, prompts[4][0], prompts[4][1])}
    </div>
    <div class="cta">
      <p class="eyebrow">Full bundle direction</p>
      <h2>{html.escape(niche)} Growth Bundle</h2>
      <p class="intro">Once this sample is approved, the same niche-specific art direction can be applied across the AI Playbook, 30-day calendar files, templates, brand kit, and client system documents.</p>
    </div>
    <div class="footer"><span>Approval sample</span><span>03</span></div>
  </section>
</main>
</body>
</html>
"""


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for niche_dir in sorted(SOURCE_ROOT.iterdir()):
        if not niche_dir.is_dir() or niche_dir.name.startswith("_") or niche_dir.name == "broker_toolkit":
            continue
        style = STYLE_BY_NICHE.get(niche_dir.name)
        if not style:
            continue
        pdf = find_sample_pdf(niche_dir)
        if not pdf:
            continue
        out_dir = OUT_ROOT / slugify(niche_dir.name)
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{slugify(niche_dir.name)}-sample.html"
        out.write_text(build_doc(niche_dir.name, pdf, style), encoding="utf-8")
        created.append(out)

    style_by_slug = {slugify(niche): style for niche, style in STYLE_BY_NICHE.items()}
    index_links = "\n".join(
        f"""<a class="sample-card {html.escape(style_by_slug[path.parent.name]["layout"])}" href="{path.relative_to(OUT_ROOT).as_posix()}">
  <span>{html.escape(style_by_slug[path.parent.name]["layout"].replace("-", " "))}</span>
  <strong>{html.escape(path.parent.name.replace("-", " ").title())}</strong>
  <em>{html.escape(style_by_slug[path.parent.name]["mood"])}</em>
</a>"""
        for path in created
    )
    (OUT_ROOT / "index.html").write_text(
        f"""<!doctype html><html><head><meta charset="utf-8"><title>Sample Documents</title>
<style>
*{{box-sizing:border-box}}body{{font-family:Inter,Arial,sans-serif;background:radial-gradient(circle at 20% 0,#222,#090909 55%);color:#eee;margin:0;padding:56px}}
.wrap{{max-width:1180px;margin:0 auto}}.eyebrow{{color:#9fb2ff;text-transform:uppercase;letter-spacing:.22em;font-size:11px;font-weight:850}}
h1{{font-size:54px;line-height:.95;margin:14px 0 12px;letter-spacing:-.06em}}p{{color:#aaa;max-width:680px;line-height:1.6}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:36px}}
.sample-card{{min-height:172px;padding:22px;border:1px solid rgba(255,255,255,.11);border-radius:24px;background:linear-gradient(145deg,rgba(255,255,255,.07),rgba(255,255,255,.02));color:#f5f5f5;text-decoration:none;display:flex;flex-direction:column;justify-content:space-between;transition:transform .25s ease,border-color .25s ease,background .25s ease}}
.sample-card:hover{{transform:translateY(-4px);border-color:rgba(159,178,255,.38);background:linear-gradient(145deg,rgba(159,178,255,.11),rgba(255,255,255,.025))}}
span{{color:#9fb2ff;text-transform:uppercase;letter-spacing:.18em;font-size:10px;font-weight:900}}strong{{font-size:24px;line-height:1.02;letter-spacing:-.04em}}em{{font-style:normal;color:#aaa;font-size:13px;line-height:1.45}}
.editorial span{{color:#e2b7c3}}.protocol span{{color:#b8d6c5}}.ledger span{{color:#a8c0c8}}.field span{{color:#70cfff}}.performance span{{color:#c8ff5f}}.dark-shop span{{color:#d0a14c}}.commerce span{{color:#ff9d73}}.cards span{{color:#d7bd83}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}body{{padding:30px}}h1{{font-size:38px}}}}
</style></head>
<body><main class="wrap"><div class="eyebrow">Content Elevated review set</div><h1>Niche-specific sample documents</h1><p>Each sample now uses a distinct art direction: ledger, clinical protocol, editorial studio, field-service blueprint, performance tech, commerce, dark shop, or relationship-card system.</p><section class="grid">{index_links}</section></main></body></html>""",
        encoding="utf-8",
    )
    print(f"Created {len(created)} sample documents.")
    print(OUT_ROOT / "index.html")
    for path in created:
        print(path)


if __name__ == "__main__":
    main()
