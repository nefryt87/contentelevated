from __future__ import annotations

import html
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path("/Users/tomasz/Documents/Content Elevated/Content Elevated Products")
OUT = Path(
    "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/print-ready-pdfs/design-concepts"
)


CONCEPTS = {
    "hair-stylists": {
        "niche": "Hair Stylists",
        "pdf": "5_Free_Rebooking_Text_Templates.pdf",
        "title": "Rebooking Text Atelier",
        "subtitle": "Warm salon editorial, soft paper, blush undertones, appointment-card rhythm.",
        "class": "hair",
    },
    "aestheticians": {
        "niche": "Aestheticians",
        "pdf": "01_AI_Playbook_Aestheticians.pdf",
        "title": "Skin Protocol Studio",
        "subtitle": "Clinical spa luxury: pearl surfaces, treatment-room calm, precise protocol cards.",
        "class": "aesthetic",
    },
    "hvac-contractors": {
        "niche": "HVAC Contractors",
        "pdf": "01_AI_Playbook_HVAC_Contractors.pdf",
        "title": "HVAC Dispatch Manual",
        "subtitle": "Blueprint grids, field notes, service-ticket modules, cool air and heat signals.",
        "class": "hvac",
    },
    "accountants-cpas": {
        "niche": "Accountants & CPAs",
        "pdf": "01_AI_Playbook_Accountants_CPAs.pdf",
        "title": "Advisory Ledger System",
        "subtitle": "Measured finance editorial: ledger lines, quiet confidence, client trust blocks.",
        "class": "cpa",
    },
    "barbers": {
        "niche": "Barbers",
        "pdf": "01_AI_Playbook_Barbers.pdf",
        "title": "Chair Loyalty Playbook",
        "subtitle": "Sharp shop culture: black comb lines, brass accents, tactile appointment slips.",
        "class": "barber",
    },
    "personal-trainers": {
        "niche": "Personal Trainers",
        "pdf": "01_AI_Playbook_Personal_Trainers.pdf",
        "title": "Client Performance System",
        "subtitle": "Kinetic coaching energy: dark training UI, progress metrics, neon discipline.",
        "class": "trainer",
    },
    "wedding-photographers": {
        "niche": "Wedding Photographers",
        "pdf": "01_AI_Playbook_Wedding_Photographers.pdf",
        "title": "Wedding Inquiry Editorial",
        "subtitle": "Romantic cinematic client experience: film margins, ivory paper, quiet emotion.",
        "class": "wedding",
    },
    "etsy-sellers": {
        "niche": "Etsy Sellers",
        "pdf": "01_AI_Playbook_Etsy_Sellers.pdf",
        "title": "Shop Launch Board",
        "subtitle": "Modern maker-commerce: product tiles, SKU labels, clean conversion modules.",
        "class": "etsy",
    },
}


BASE_CSS = r"""
@page { size: Letter; margin: 0; }
* { box-sizing: border-box; }
body { margin:0; background:#d7d7d4; color:var(--ink); font-family: Inter, "Helvetica Neue", Arial, sans-serif; }
.book { width:8.5in; margin:0 auto; }
.page { position:relative; width:8.5in; min-height:11in; page-break-after:always; overflow:hidden; padding:.62in; background:var(--page-bg); }
.brand { position:relative; z-index:3; display:flex; justify-content:space-between; align-items:flex-start; font-size:9px; letter-spacing:.2em; text-transform:uppercase; font-weight:800; color:var(--muted); }
.brand .ce { color:var(--ink); letter-spacing:.18em; }
.tag { border:1px solid var(--line); border-radius:999px; padding:9px 13px; background:var(--tag-bg); }
h1,h2,h3,p { position:relative; z-index:3; }
h1 { margin:0; color:var(--ink); }
h2 { margin:0; color:var(--ink); }
h3 { margin:0; color:var(--accent); }
p { margin:0 0 9px; color:var(--muted); font-size:10.5px; line-height:1.45; }
.footer { position:absolute; left:.62in; right:.62in; bottom:.28in; z-index:3; display:flex; justify-content:space-between; color:var(--muted); opacity:.72; font-size:8px; font-weight:800; letter-spacing:.13em; text-transform:uppercase; }
.small { font-size:8px; letter-spacing:.18em; text-transform:uppercase; font-weight:850; color:var(--accent); }
.sample h3 { margin:16px 0 8px; font-size:9px; letter-spacing:.14em; text-transform:uppercase; }
.sample .line { border-left:2px solid var(--accent); padding:8px 0 8px 12px; background:var(--soft-accent); }
.swatches { display:flex; gap:9px; margin-top:18px; }
.swatches i { width:38px; height:38px; border-radius:50%; border:1px solid var(--line); }

.hair { --ink:#201716; --muted:#786663; --accent:#b98378; --accent2:#e2b9aa; --line:rgba(32,23,22,.14); --tag-bg:rgba(255,255,255,.46); --soft-accent:linear-gradient(90deg,rgba(185,131,120,.12),transparent); --page-bg:radial-gradient(circle at 18% 16%,rgba(226,185,170,.38),transparent 2.2in),linear-gradient(135deg,#fff8f3,#f6e5df); }
.hair.cover:before { content:""; position:absolute; inset:.54in .72in auto auto; width:2.2in; height:7.6in; border-radius:999px; background:linear-gradient(180deg,rgba(185,131,120,.28),transparent); filter:blur(1px); }
.hair h1 { margin-top:1.25in; max-width:5.3in; font-family:Georgia,serif; font-size:55px; line-height:.96; font-weight:400; letter-spacing:-.045em; }
.hair .hero-note { position:absolute; right:.62in; bottom:1.12in; width:2.25in; border:1px solid var(--line); border-radius:28px; padding:22px; background:rgba(255,255,255,.48); box-shadow:0 30px 70px rgba(107,76,70,.12); }
.hair .editorial-strip { position:absolute; left:.62in; bottom:1.05in; width:4.5in; display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }
.hair .editorial-strip div { border:1px solid var(--line); border-radius:18px; min-height:1.15in; padding:14px; background:rgba(255,255,255,.42); }
.hair .direction { margin-top:1.1in; display:grid; grid-template-columns:1fr 1fr; gap:.35in; }
.hair .sample { margin-top:.65in; max-width:6.5in; border-radius:34px; padding:32px; background:rgba(255,255,255,.54); border:1px solid var(--line); }

.aesthetic { --ink:#151817; --muted:#687169; --accent:#6f927e; --accent2:#d6c8b4; --line:rgba(21,24,23,.12); --tag-bg:rgba(255,255,255,.52); --soft-accent:linear-gradient(90deg,rgba(111,146,126,.11),transparent); --page-bg:radial-gradient(circle at 80% 14%,rgba(214,200,180,.45),transparent 2.35in),radial-gradient(circle at 15% 90%,rgba(111,146,126,.16),transparent 2.4in),linear-gradient(135deg,#fbfaf5,#edf2ec); }
.aesthetic.cover:before { content:""; position:absolute; inset:.98in .62in auto auto; width:3.45in; height:5.55in; border-radius:42px; background:linear-gradient(135deg,rgba(255,255,255,.65),rgba(111,146,126,.12)); border:1px solid var(--line); box-shadow:0 25px 70px rgba(50,70,60,.1); }
.aesthetic.cover:after { content:"PROTOCOL 01\A CONSULTATION\A TREATMENT MAP\A REBOOKING"; white-space:pre; position:absolute; right:1in; top:2.25in; width:2.3in; color:var(--muted); font-size:11px; line-height:2.3; letter-spacing:.16em; text-transform:uppercase; z-index:2; }
.aesthetic h1 { margin-top:1.35in; max-width:4.4in; font-family:Georgia,serif; font-size:50px; line-height:1; font-weight:400; letter-spacing:-.04em; }
.aesthetic .direction { margin-top:1in; display:grid; grid-template-columns:.75fr 1.25fr; gap:.35in; }
.aesthetic .sample { margin-top:.7in; display:grid; grid-template-columns:.9fr 1.1fr; gap:.3in; padding:28px; border:1px solid var(--line); border-radius:30px; background:rgba(255,255,255,.62); }

.hvac { --ink:#07111d; --muted:#536474; --accent:#37a8e6; --accent2:#f1853e; --line:rgba(7,17,29,.14); --tag-bg:rgba(255,255,255,.42); --soft-accent:linear-gradient(90deg,rgba(55,168,230,.11),transparent); --page-bg:linear-gradient(rgba(7,17,29,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(7,17,29,.045) 1px,transparent 1px),radial-gradient(circle at 80% 18%,rgba(55,168,230,.22),transparent 2.5in),linear-gradient(135deg,#f4fbff,#e4edf5); background-size:auto, .32in .32in, auto, auto; }
.hvac.cover:before { content:""; position:absolute; right:.62in; top:1.35in; width:3.15in; height:6.25in; background:#0d1a28; border-radius:18px; box-shadow:0 35px 80px rgba(7,17,29,.18); clip-path:polygon(0 0,100% 8%,100% 100%,0 92%); }
.hvac.cover:after { content:"SERVICE\A DIAGNOSTIC\A FOLLOW-UP\A AGREEMENTS"; white-space:pre; position:absolute; right:1.05in; top:2.1in; z-index:2; color:#dff5ff; font-size:20px; line-height:2.2; font-family:'Arial Narrow',Arial,sans-serif; font-weight:900; letter-spacing:.08em; }
.hvac h1 { margin-top:1.15in; max-width:4.5in; font-family:'Arial Narrow','Helvetica Neue',Arial,sans-serif; font-size:60px; line-height:.86; font-weight:950; letter-spacing:-.055em; text-transform:uppercase; }
.hvac .direction { margin-top:1in; display:grid; grid-template-columns:repeat(3,1fr); gap:13px; }
.hvac .direction > div { border:1px solid var(--line); border-radius:10px; background:rgba(255,255,255,.58); padding:18px; min-height:2.1in; }
.hvac .sample { margin-top:.65in; border:1px solid var(--line); border-radius:16px; padding:24px; background:rgba(255,255,255,.68); }

.cpa { --ink:#121417; --muted:#62686d; --accent:#536f78; --accent2:#8aa5a2; --line:rgba(18,20,23,.13); --tag-bg:rgba(255,255,255,.45); --soft-accent:linear-gradient(90deg,rgba(83,111,120,.1),transparent); --page-bg:linear-gradient(90deg,rgba(18,20,23,.045) 1px,transparent 1px),linear-gradient(#fbfaf5,#eee9df); background-size:.5in 100%, auto; }
.cpa.cover:before { content:""; position:absolute; left:.62in; right:.62in; bottom:1.08in; height:2.3in; border-top:1px solid var(--line); border-bottom:1px solid var(--line); background:repeating-linear-gradient(0deg,transparent 0,transparent .36in,rgba(18,20,23,.07) .365in); }
.cpa h1 { margin-top:1.2in; max-width:5.7in; font-family:Georgia,serif; font-size:54px; line-height:.98; font-weight:400; letter-spacing:-.04em; }
.cpa .ledger { position:absolute; left:.78in; right:.78in; bottom:1.32in; display:grid; grid-template-columns:1.2fr .6fr .6fr; gap:0; z-index:2; border:1px solid var(--line); background:rgba(255,255,255,.58); }
.cpa .ledger div { padding:14px; border-right:1px solid var(--line); font-size:9px; letter-spacing:.13em; text-transform:uppercase; color:var(--muted); }
.cpa .direction { margin-top:1in; display:grid; grid-template-columns:1fr 1fr; gap:.45in; }
.cpa .sample { margin-top:.65in; padding:0; border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
.cpa .sample p, .cpa .sample h3 { padding-left:.1in; }

.barber { --ink:#15110f; --muted:#7a6a5d; --accent:#a87442; --accent2:#272d2f; --line:rgba(21,17,15,.16); --tag-bg:rgba(255,255,255,.35); --soft-accent:linear-gradient(90deg,rgba(168,116,66,.12),transparent); --page-bg:radial-gradient(circle at 80% 15%,rgba(39,45,47,.2),transparent 2.6in),linear-gradient(135deg,#f3eee6,#d8c6ad); }
.barber.cover:before { content:""; position:absolute; right:-.4in; top:1.2in; width:4.2in; height:7.2in; background:repeating-linear-gradient(90deg,#171311 0,#171311 10px,#2b211c 11px,#2b211c 18px); transform:rotate(-8deg); border-radius:28px; box-shadow:0 35px 80px rgba(21,17,15,.22); }
.barber h1 { margin-top:1.25in; max-width:4.65in; font-family:'Arial Narrow','Helvetica Neue',Arial,sans-serif; font-size:62px; line-height:.84; font-weight:950; letter-spacing:-.055em; text-transform:uppercase; }
.barber .ticket { position:absolute; left:.62in; bottom:1.05in; width:5.2in; padding:20px; border:1px dashed var(--accent); background:rgba(255,255,255,.48); transform:rotate(-1deg); }
.barber .direction { margin-top:1.05in; columns:2; column-gap:.35in; }
.barber .sample { margin-top:.65in; display:grid; grid-template-columns:.35fr 1fr; gap:.28in; border-radius:0; border-top:4px solid var(--ink); padding-top:24px; }

.trainer { --ink:#101315; --muted:#69706e; --accent:#2d8f76; --accent2:#c8ff5f; --line:rgba(16,19,21,.13); --tag-bg:rgba(255,255,255,.42); --soft-accent:linear-gradient(90deg,rgba(45,143,118,.12),transparent); --page-bg:radial-gradient(circle at 80% 14%,rgba(200,255,95,.2),transparent 2.2in),linear-gradient(135deg,#f5f8f6,#dfe9e4); }
.trainer.cover:before { content:""; position:absolute; right:.55in; top:1.28in; width:3.4in; height:6.5in; border-radius:24px; background:#111818; box-shadow:0 34px 80px rgba(16,19,21,.2); }
.trainer.cover:after { content:"38%\\A SHOW RATE\\A 14 DAYS\\A CLIENT FLOW"; white-space:pre; position:absolute; right:.95in; top:2in; z-index:2; font-family:'Arial Narrow',Arial,sans-serif; font-size:34px; line-height:1.2; font-weight:950; color:#f8fff2; }
.trainer h1 { margin-top:1.08in; max-width:4.4in; font-family:'Arial Narrow','Helvetica Neue',Arial,sans-serif; font-size:64px; line-height:.82; font-weight:950; letter-spacing:-.06em; text-transform:uppercase; }
.trainer .metrics { position:absolute; left:.62in; right:.62in; bottom:1.08in; display:grid; grid-template-columns:repeat(4,1fr); border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
.trainer .metrics div { padding:18px 14px; border-right:1px solid var(--line); }
.trainer .direction { margin-top:1in; display:grid; grid-template-columns:1.2fr .8fr; gap:.35in; }
.trainer .sample { margin-top:.65in; background:#111818; color:#f8fff2; padding:28px; border-radius:24px; }
.trainer .sample p { color:rgba(248,255,242,.72); }

.wedding { --ink:#1d1715; --muted:#756760; --accent:#a67a6d; --accent2:#d3ad8b; --line:rgba(29,23,21,.13); --tag-bg:rgba(255,255,255,.45); --soft-accent:linear-gradient(90deg,rgba(166,122,109,.11),transparent); --page-bg:radial-gradient(circle at 78% 16%,rgba(211,173,139,.28),transparent 2.4in),linear-gradient(135deg,#fffaf6,#eaded4); }
.wedding.cover:before { content:""; position:absolute; right:.68in; top:1.15in; width:2.85in; height:6.4in; border:12px solid rgba(255,255,255,.58); background:linear-gradient(135deg,rgba(166,122,109,.32),rgba(255,255,255,.18)); box-shadow:0 32px 78px rgba(90,65,58,.14); transform:rotate(2deg); }
.wedding.cover:after { content:""; position:absolute; right:1.1in; top:1.75in; width:2.2in; height:5.2in; border:1px solid rgba(29,23,21,.16); transform:rotate(-2deg); }
.wedding h1 { margin-top:1.25in; max-width:4.7in; font-family:Georgia,serif; font-size:54px; line-height:.98; font-weight:400; letter-spacing:-.045em; }
.wedding .direction { margin-top:1.1in; display:grid; grid-template-columns:1fr 1fr; gap:.35in; }
.wedding .sample { margin-top:.7in; padding:30px 36px; border-left:1px solid var(--line); border-right:1px solid var(--line); }

.etsy { --ink:#111516; --muted:#5d6566; --accent:#4f8f94; --accent2:#ff8f61; --line:rgba(17,21,22,.13); --tag-bg:rgba(255,255,255,.5); --soft-accent:linear-gradient(90deg,rgba(79,143,148,.1),transparent); --page-bg:radial-gradient(circle at 78% 15%,rgba(255,143,97,.18),transparent 2.3in),linear-gradient(135deg,#fbfcfb,#e4ebe9); }
.etsy h1 { margin-top:1.05in; max-width:5.4in; font-family:Inter,'Helvetica Neue',Arial,sans-serif; font-size:56px; line-height:.93; font-weight:850; letter-spacing:-.06em; }
.etsy.cover:before { content:""; position:absolute; right:.62in; top:1.25in; width:3.2in; height:6.3in; display:block; background:
linear-gradient(90deg,var(--line) 1px,transparent 1px),linear-gradient(var(--line) 1px,transparent 1px),rgba(255,255,255,.5); background-size:1.05in 1.05in; border:1px solid var(--line); border-radius:26px; }
.etsy.cover:after { content:"SKU-01\\A LISTING\\A LAUNCH\\A REVIEWS\\A RETENTION"; white-space:pre; position:absolute; right:1.02in; top:1.82in; z-index:2; font-size:12px; line-height:2.6; letter-spacing:.16em; font-weight:850; color:var(--ink); }
.etsy .direction { margin-top:.95in; display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
.etsy .direction > div { border:1px solid var(--line); border-radius:18px; padding:16px; background:rgba(255,255,255,.55); min-height:2in; }
.etsy .sample { margin-top:.65in; display:grid; grid-template-columns:repeat(2,1fr); gap:18px; }
.etsy .sample > * { border:1px solid var(--line); border-radius:18px; padding:16px; background:rgba(255,255,255,.55); }
"""


def extract(pdf: Path) -> list[str]:
    reader = PdfReader(str(pdf))
    text = "\n".join(page.extract_text() or "" for page in reader.pages[:3])
    lines = []
    for line in text.splitlines():
        cleaned = " ".join(line.strip().split())
        if cleaned:
            lines.append(cleaned)
    return lines


def sample_items(lines: list[str]) -> list[str]:
    items = []
    buf: list[str] = []
    for line in lines:
        if line.upper() == "CONTENT ELEVATED":
            continue
        is_heading = len(line) < 76 and (line.isupper() or re.match(r"^(Chapter|Prompt|Template|Section)", line, re.I))
        if is_heading:
            if buf:
                items.append(" ".join(buf))
                buf = []
            items.append(line)
        else:
            buf.append(line)
            if len(" ".join(buf)) > 210:
                items.append(" ".join(buf))
                buf = []
        if len(items) >= 12:
            break
    if buf and len(items) < 12:
        items.append(" ".join(buf))
    return items


def sample_html(items: list[str]) -> str:
    bits = []
    for item in items:
        escaped = html.escape(item)
        if len(item) < 78 and (item.isupper() or item.lower().startswith(("chapter", "prompt", "template"))):
            bits.append(f"<h3>{escaped}</h3>")
        else:
            cls = ' class="line"' if item.lower().startswith(("write ", "copy ", "subject", "dear ")) else ""
            bits.append(f"<p{cls}>{escaped}</p>")
    return "".join(bits)


def swatches(cls: str) -> str:
    palettes = {
        "hair": ["#fff7f3", "#f4dfd8", "#201716", "#b98378", "#e2b9aa"],
        "aesthetic": ["#fbfaf5", "#edf2ec", "#151817", "#6f927e", "#d6c8b4"],
        "hvac": ["#f4fbff", "#e4edf5", "#07111d", "#37a8e6", "#f1853e"],
        "cpa": ["#fbfaf5", "#eee9df", "#121417", "#536f78", "#8aa5a2"],
        "barber": ["#f3eee6", "#d8c6ad", "#15110f", "#a87442", "#272d2f"],
        "trainer": ["#f5f8f6", "#dfe9e4", "#101315", "#2d8f76", "#c8ff5f"],
        "wedding": ["#fffaf6", "#eaded4", "#1d1715", "#a67a6d", "#d3ad8b"],
        "etsy": ["#fbfcfb", "#e4ebe9", "#111516", "#4f8f94", "#ff8f61"],
    }
    return "".join(f'<i style="background:{color}"></i>' for color in palettes[cls])


def direction_page(concept: dict[str, str], cls: str) -> str:
    niche = html.escape(concept["niche"])
    notes = {
        "hair": ["Appointment cards", "Soft editorial spacing", "Warm client retention cues"],
        "aesthetic": ["Protocol cards", "Pearl clinical light", "Treatment-room calm"],
        "hvac": ["Blueprint grid", "Service-ticket hierarchy", "Cool/heat signal color"],
        "cpa": ["Ledger structure", "Quiet trust language", "Advisory confidence"],
        "barber": ["Sharp slips", "Shop texture", "Masculine editorial contrast"],
        "trainer": ["Metrics strip", "Dark performance panel", "Kinetic coaching tone"],
        "wedding": ["Film frame margins", "Romantic restraint", "Inquiry-to-booking flow"],
        "etsy": ["SKU card grid", "Product launch modules", "Clean maker commerce"],
    }[cls]
    cards = "".join(f"<div><p class='small'>{i:02d}</p><p>{html.escape(note)}</p></div>" for i, note in enumerate(notes, 1))
    return f"""<section class="page {cls}"><div class="brand"><div class="ce">CONTENT ELEVATED</div><div class="tag">{niche}</div></div><p class="small" style="margin-top:.95in">Design Language</p><h2>Approve the mood before the full bundle.</h2><div class="direction">{cards}</div><div class="swatches">{swatches(cls)}</div><div class="footer"><span>{niche}</span><span>Concept 02</span></div></section>"""


def render(slug: str, concept: dict[str, str]) -> str:
    cls = concept["class"]
    niche = html.escape(concept["niche"])
    title = html.escape(concept["title"])
    pdf = ROOT / concept["niche"] / concept["pdf"]
    items = sample_items(extract(pdf))
    note = f"<div class='hero-note'><p class='small'>Positioning</p><p>{html.escape(concept['subtitle'])}</p></div>"
    extra = {
        "hair": note + "<div class='editorial-strip'><div><p class='small'>Text</p><p>Warm</p></div><div><p class='small'>Timing</p><p>Booked</p></div><div><p class='small'>Tone</p><p>Personal</p></div></div>",
        "cpa": "<div class='ledger'><div>Consultation conversion</div><div>Retention</div><div>Referrals</div></div>",
        "trainer": "<div class='metrics'><div><p class='small'>Leads</p><p>+38%</p></div><div><p class='small'>Check-ins</p><p>Weekly</p></div><div><p class='small'>Plans</p><p>90 days</p></div><div><p class='small'>Close</p><p>Follow-up</p></div></div>",
        "barber": "<div class='ticket'><p class='small'>Shop note</p><p>Designed to feel like a premium appointment slip meets growth manual.</p></div>",
    }.get(cls, "")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>{niche} Concept</title><style>{BASE_CSS}</style></head><body><main class="book">
<section class="page cover {cls}"><div class="brand"><div class="ce">CONTENT ELEVATED</div><div class="tag">{niche}</div></div><h1>{title}</h1><p style="max-width:4.75in;margin-top:.22in;font-size:14px;line-height:1.52">{html.escape(concept["subtitle"])}</p>{extra}<div class="footer"><span>{niche}</span><span>Concept 01</span></div></section>
{direction_page(concept, cls)}
<section class="page {cls}"><div class="brand"><div class="ce">CONTENT ELEVATED</div><div class="tag">Interior Proof</div></div><div class="sample">{sample_html(items)}</div><div class="footer"><span>{niche}</span><span>Concept 03</span></div></section>
</main></body></html>"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, concept in CONCEPTS.items():
        out = OUT / f"{slug}-concept.html"
        out.write_text(render(slug, concept), encoding="utf-8")
        print(out)


if __name__ == "__main__":
    main()
