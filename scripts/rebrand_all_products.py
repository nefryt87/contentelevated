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
PROFESSIONAL_SERVICE_NICHES = {
    "Accountants & CPAs",
    "Attorneys",
    "Financial Advisors",
    "Insurance Agents",
    "Mortgage Brokers",
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
    return (
        value.title()
        .replace("Ai", "AI")
        .replace("Cpa", "CPA")
        .replace("Cpas", "CPAs")
        .replace("Hvac", "HVAC")
        .replace("Seo", "SEO")
        .replace("Hmua", "HMUA")
    )


def theme_for(niche: str) -> dict[str, str]:
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


def is_professional_service_niche(niche: str) -> bool:
    return niche in PROFESSIONAL_SERVICE_NICHES or "Broker" in niche or "Advisor" in niche


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
.page::after{{content:"";position:absolute;right:.62in;top:.92in;width:2.55in;height:7.6in;border-left:1px solid rgba(23,27,31,.1);background:linear-gradient(90deg,rgba(95,127,134,.065),transparent 72%);pointer-events:none}}
.brand{{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-start;color:rgba(23,27,31,.7);font-size:9px;font-weight:900;letter-spacing:.24em;text-transform:uppercase}}
.brand small{{display:block;margin-top:7px;color:var(--accent);font-size:8px;letter-spacing:.2em}}
.badge{{border:1px solid rgba(23,27,31,.14);background:rgba(255,255,255,.64);padding:9px 13px;color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}}
.cover-kicker{{position:relative;z-index:3;margin-top:.84in;display:flex;align-items:center;gap:12px;color:var(--accent);font-size:10px;font-weight:900;letter-spacing:.24em;text-transform:uppercase}}
.cover-kicker::before{{content:"";width:.48in;height:1px;background:var(--accent)}}
h1,h2,h3{{position:relative;z-index:3;margin:0;font-family:Georgia,"Times New Roman",serif;font-weight:400;letter-spacing:-.045em}}
h1{{max-width:5.65in;margin-top:.22in;font-size:58px;line-height:.96}}
h1 em,h2 em{{font-style:italic;color:var(--accent)}}
.lead{{position:relative;z-index:3;max-width:4.9in;margin-top:.32in;color:#384149;font-size:15.5px;line-height:1.62}}
.memo-strip{{position:absolute;z-index:3;left:.62in;right:.62in;bottom:.82in;display:grid;grid-template-columns:1fr 1fr 1fr;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.memo-cell{{min-height:.96in;padding:17px 18px;border-left:1px solid var(--line)}}
.memo-cell:first-child{{border-left:0;padding-left:0}}
.memo-cell b{{display:block;color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:24px;font-weight:400;line-height:1}}
.memo-cell span{{display:block;margin-top:9px;color:#5f6870;font-size:8.5px;font-weight:850;letter-spacing:.14em;line-height:1.55;text-transform:uppercase}}
.footer{{position:absolute;z-index:3;left:.62in;right:.62in;bottom:.34in;display:flex;justify-content:space-between;color:rgba(23,27,31,.55);font-size:8px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}}
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
            cards.append((current_title, " ".join(current_body)))
            current_body = []

    for kind, text in blocks:
        if kind == "h":
            flush()
            current_title = title_case(text)
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
        <p>{html.escape(body[:980])}</p>
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
            cards.append((current_title, body[:1250], body[1250:1500]))
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
            cards.append((current_title, " ".join(current_body)))
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
        <p>{html.escape(body[:1050])}</p>
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
    current_title = "Advisory System"
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_body
        if current_body:
            cards.append((current_title, " ".join(current_body)))
            current_body = []

    for kind, text in blocks:
        if kind == "h":
            flush()
            current_title = title_case(text)
        else:
            current_body.append(text)
    flush()

    if not cards:
        cards = [("Advisory System", "Customize this section for the client type, engagement, compliance context, and next professional touchpoint.")]

    pieces = []
    for offset, (card_title, body) in enumerate(cards, start=start_index):
        pieces.append(
            f"""
    <article class="dossier-card">
      <div class="num">{offset:02d}</div>
      <div>
        <p class="eyebrow">Client system</p>
        <h3>{html.escape(card_title)}</h3>
        <p>{html.escape(body[:1080])}</p>
      </div>
    </article>"""
        )
    return "\n".join(pieces)


def build_professional_service_html(niche: str, title: str, descriptor: str, theme: dict[str, str], blocks: list[tuple[str, str]]) -> str:
    title_html = html.escape(title).replace("AI", "<em>AI</em>")
    chunks = chunk_blocks(blocks, max_chars=2550)
    brand = html.escape(niche)
    pages = [
        f"""<section class="page">
  <div class="brand">
    <div>CONTENT ELEVATED<small>{brand} Advisory System</small></div>
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
  <div class="footer"><span>{brand} advisory system</span><span>01</span></div>
</section>""",
        f"""<section class="page work">
  <div class="brand">
    <div>CONTENT ELEVATED<small>{brand}</small></div>
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
    <div>CONTENT ELEVATED<small>{brand}</small></div>
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
    return title_case(" ".join(stem.split()))


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

    if is_home_service_niche(niche):
        return build_home_service_html(niche, title, descriptor, theme, blocks)

    if is_beauty_niche(niche):
        return build_beauty_html(niche, title, descriptor, theme, blocks)

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
