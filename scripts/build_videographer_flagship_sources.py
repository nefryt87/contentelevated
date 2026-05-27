#!/usr/bin/env python3
"""Build clean Videographers flagship HTML sources.

The existing visual direction was strong, but several source files contained
extraction fragments and split prompts. This creates stable buyer-facing HTML
sources with cleaner copy, stronger package value, and safer fixed-page output.
"""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "rebranded-products-sample-direction" / "videographers"
INV = ROOT / "content-elevated-product-os" / "data" / "bundle-inventory.json"
PM = ROOT / "content-elevated-product-os" / "data" / "product-master.json"


CSS = """
@page { size: Letter; margin: 0; }
:root{
  --ink:#f8fbff;
  --paper:#06070b;
  --panel:#0e1119;
  --panel2:#151923;
  --soft:#b8c0cc;
  --muted:#7e8796;
  --line:rgba(248,251,255,.14);
  --blue:#4aa8ff;
  --cyan:#35e4d7;
  --violet:#7c6cff;
  --warm:#f0c389;
  --bone:#f6f4ee;
  --charcoal:#15171d;
}
*{box-sizing:border-box}
body{margin:0;background:#111;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}
.book{width:8.5in;margin:0 auto}
.page{position:relative;width:8.5in;height:11in;overflow:hidden;page-break-after:always;padding:.56in;background:
  radial-gradient(circle at 78% 16%,rgba(74,168,255,.22),transparent 2.3in),
  radial-gradient(circle at 18% 88%,rgba(53,228,215,.10),transparent 2.45in),
  linear-gradient(135deg,#05060a,#0b0e16 56%,#070910)}
.page::before{content:"";position:absolute;inset:.28in;border:1px solid rgba(248,251,255,.10);border-radius:26px;pointer-events:none}
.page::after{content:"";position:absolute;right:-1.1in;top:.55in;width:4.1in;height:8.8in;border:1px solid rgba(248,251,255,.06);background:linear-gradient(180deg,rgba(255,255,255,.035),transparent 65%);transform:skewX(-8deg);opacity:.42;pointer-events:none}
.light{background:radial-gradient(circle at 86% 10%,rgba(74,168,255,.12),transparent 2.5in),linear-gradient(135deg,#fff,#f1f3f7 62%,#e8edf5);color:#171b22}
.light::before{border-color:rgba(23,27,34,.12)}
.light::after{display:none}
.feature{background:radial-gradient(circle at 78% 12%,rgba(53,228,215,.16),transparent 2.3in),linear-gradient(135deg,#070910,#121724 62%,#0a0d14)}
.brand{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-start;gap:20px}
.wordmark{font-size:10.5px;font-weight:900;letter-spacing:.23em;text-transform:uppercase;color:rgba(248,251,255,.78)}
.wordmark small{display:block;margin-top:7px;color:rgba(74,168,255,.9);font-size:8px;font-weight:850;letter-spacing:.18em}
.light .wordmark{color:#151922}.light .wordmark small{color:#356fa8}
.badge{border:1px solid rgba(248,251,255,.15);border-radius:999px;background:rgba(255,255,255,.055);padding:9px 13px;color:#dcecff;font-size:8px;font-weight:900;letter-spacing:.17em;text-transform:uppercase}
.light .badge{border-color:rgba(21,25,34,.15);background:rgba(255,255,255,.72);color:#356fa8}
.kicker{position:relative;z-index:3;display:flex;align-items:center;gap:12px;color:var(--cyan);font-size:9px;font-weight:950;letter-spacing:.24em;text-transform:uppercase}
.kicker::before{content:"";width:42px;height:1px;background:linear-gradient(90deg,var(--blue),var(--cyan))}
h1,h2,h3{position:relative;z-index:3;margin:0}
h1{max-width:6.6in;margin-top:.75in;font-family:"Arial Narrow","Helvetica Neue",Arial,sans-serif;font-size:72px;line-height:.86;font-weight:950;letter-spacing:-.055em;text-transform:uppercase}
h1 em{font-style:normal;color:#fff;text-shadow:0 0 30px rgba(74,168,255,.36)}
h2{font-family:"Arial Narrow","Helvetica Neue",Arial,sans-serif;font-size:41px;line-height:.94;font-weight:950;letter-spacing:-.04em;text-transform:uppercase}
h2 em{font-style:normal;color:var(--blue)}
h3{font-size:17px;line-height:1.13;font-weight:850;letter-spacing:-.01em}
p{position:relative;z-index:3;margin:0;color:var(--soft);font-size:11.5px;line-height:1.55}
.light p{color:#47505b}
.lead{max-width:5.4in;margin-top:.28in;color:rgba(248,251,255,.84);font-size:15.5px;line-height:1.55}
.light .lead{color:#3a444f}
.cover-strip{position:absolute;z-index:3;left:.56in;right:.56in;bottom:.86in;display:grid;grid-template-columns:repeat(4,1fr);border:1px solid rgba(248,251,255,.15);background:rgba(6,7,11,.72);box-shadow:0 22px 70px rgba(0,0,0,.24)}
.cover-cell{min-height:.96in;padding:16px 15px;border-left:1px solid var(--line)}
.cover-cell:first-child{border-left:0}
.cover-cell b{display:block;color:#fff;font-size:21px;line-height:1;font-weight:950;letter-spacing:-.02em}
.cover-cell span{display:block;margin-top:10px;color:rgba(248,251,255,.72);font-size:8px;font-weight:850;letter-spacing:.14em;line-height:1.5;text-transform:uppercase}
.footer{position:absolute;z-index:3;left:.56in;right:.56in;bottom:.34in;display:flex;justify-content:space-between;color:rgba(248,251,255,.48);font-size:8px;font-weight:850;letter-spacing:.14em;text-transform:uppercase}
.light .footer{color:rgba(21,25,34,.5)}
.section-head{position:relative;z-index:3;display:grid;grid-template-columns:.95fr 1.05fr;gap:.34in;align-items:end;margin-top:.26in;padding-bottom:.22in;border-bottom:1px solid rgba(248,251,255,.13)}
.light .section-head{border-bottom-color:rgba(21,25,34,.12)}
.eyebrow{margin:0 0 9px;color:var(--blue);font-size:8px;font-weight:950;letter-spacing:.21em;text-transform:uppercase}
.intro{margin:0;color:rgba(248,251,255,.72);font-size:11.6px;line-height:1.56}
.light .intro{color:#555f6b}
.grid-2{position:relative;z-index:3;display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:.30in}
.grid-3{position:relative;z-index:3;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:.30in}
.card,.panel{position:relative;z-index:3;border:1px solid rgba(248,251,255,.14);background:linear-gradient(145deg,rgba(255,255,255,.075),rgba(255,255,255,.035));border-radius:18px;padding:16px;box-shadow:0 16px 42px rgba(0,0,0,.16)}
.light .card,.light .panel{border-color:rgba(21,25,34,.12);background:linear-gradient(145deg,#fff,rgba(242,244,249,.94));box-shadow:0 14px 36px rgba(10,18,28,.06)}
.card::before{content:"";position:absolute;left:0;top:15px;bottom:15px;width:3px;border-radius:999px;background:linear-gradient(180deg,var(--blue),var(--cyan))}
.num{display:inline-grid;width:.42in;height:.42in;place-items:center;margin-bottom:11px;border:1px solid rgba(74,168,255,.42);border-radius:10px;color:#dcecff;font-size:11px;font-weight:950;background:rgba(74,168,255,.08)}
.light .num{background:#111827;color:#fff;border-color:rgba(74,168,255,.55)}
.card p,.panel p{margin-top:9px;font-size:10.3px;line-height:1.5}
.stack{position:relative;z-index:3;display:grid;gap:11px;margin-top:.30in}
.asset{display:grid;grid-template-columns:.50in 1fr;gap:14px;padding:15px 17px;border:1px solid rgba(248,251,255,.14);border-radius:18px;background:rgba(255,255,255,.065)}
.light .asset{border-color:rgba(21,25,34,.12);background:rgba(255,255,255,.78)}
.asset .num{margin:0}
.asset p{font-size:10.7px;line-height:1.5}
.script{margin-top:9px;border-radius:14px;background:rgba(255,255,255,.08);border:1px solid rgba(248,251,255,.12);padding:12px;color:rgba(248,251,255,.82);font-size:10.3px;line-height:1.48}
.light .script{background:#fff;border-color:rgba(21,25,34,.10);color:#323943}
.script ul{margin:0;padding-left:18px}.script li{margin:0 0 6px}
.table{position:relative;z-index:3;margin-top:.25in;border:1px solid rgba(21,25,34,.12);border-radius:18px;overflow:hidden;background:rgba(255,255,255,.82)}
.row{display:grid;grid-template-columns:1.05fr 1.35fr 1.4fr;border-top:1px solid rgba(21,25,34,.11)}
.row:first-child{border-top:0}.row>*{padding:9px 11px;border-left:1px solid rgba(21,25,34,.11);font-size:9.7px;line-height:1.35;color:#525b66}.row>*:first-child{border-left:0;color:#171b22;font-weight:800}
.row.head>*{background:#111827;color:white;font-size:7.6px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}
.swatches{display:flex;gap:10px;margin-top:11px}.swatch{width:.4in;height:.4in;border-radius:999px;border:1px solid rgba(0,0,0,.14)}
.quote{position:relative;z-index:3;margin-top:.38in;padding:.34in;border:1px solid rgba(248,251,255,.15);border-radius:22px;background:rgba(255,255,255,.07)}
.quote p{font-size:17px;line-height:1.42;color:#fff}
@media print{body{background:white}.book{width:auto;margin:0}}
"""


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def brand(doc: str, badge: str = "") -> str:
    return (
        '<div class="brand">'
        '<div class="wordmark">Content Elevated<small>Videographer Growth Bundle</small></div>'
        f'<div class="badge">{esc(badge or doc)}</div>'
        "</div>"
    )


def page(inner: str, number: int, doc: str, cls: str = "") -> str:
    return f'<section class="page {cls}">{inner}<div class="footer"><span>{esc(doc)}</span><span>{number:02d}</span></div></section>'


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def cover(title: str, subtitle: str, doc: str, cells: list[tuple[str, str]]) -> str:
    cell_html = "".join(f'<div class="cover-cell"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in cells)
    return page(
        brand(doc, doc)
        + '<p class="kicker" style="margin-top:.78in">Cinematic systems · premium clients</p>'
        + f"<h1>{title}</h1>"
        + f'<p class="lead">{esc(subtitle)}</p>'
        + f'<div class="cover-strip">{cell_html}</div>',
        1,
        doc,
    )


def intro_page(doc: str, number: int, headline: str, intro: str) -> str:
    return page(
        brand(doc, "How To Use")
        + f'<div class="section-head"><div><p class="eyebrow">How to use it</p><h2>{headline}</h2></div><p class="intro">{esc(intro)}</p></div>'
        + '<div class="grid-3">'
        + '<article class="card"><div class="num">01</div><h3>Pick the market</h3><p>Decide whether the asset is for weddings, corporate work, commercial brands, or hybrid studios before customizing the copy.</p></article>'
        + '<article class="card"><div class="num">02</div><h3>Customize the proof</h3><p>Add your style, portfolio examples, production process, delivery timeline, package names, and client outcomes.</p></article>'
        + '<article class="card"><div class="num">03</div><h3>Ship the system</h3><p>Install the inquiry reply, follow-up sequence, questionnaire, content calendar, and vendor touchpoints before redesigning anything.</p></article>'
        + "</div>",
        number,
        doc,
        "light",
    )


def section_page(doc: str, number: int, kicker: str, headline: str, intro: str, cards: list[tuple[str, str, str]], cls: str = "light") -> str:
    body = brand(doc, kicker) + f'<div class="section-head"><div><p class="eyebrow">{esc(kicker)}</p><h2>{headline}</h2></div><p class="intro">{esc(intro)}</p></div><div class="stack">'
    for idx, (title, label, text) in enumerate(cards, 1):
        body += (
            '<article class="asset">'
            f'<div class="num">{idx:02d}</div><div><h3>{esc(title)}</h3><p class="eyebrow" style="margin-top:8px;margin-bottom:0">{esc(label)}</p>'
            f'<div class="script">{text}</div></div></article>'
        )
    body += "</div>"
    return page(body, number, doc, cls)


def grid_page(doc: str, number: int, kicker: str, headline: str, intro: str, cards: list[tuple[str, str]], cls: str = "") -> str:
    body = brand(doc, kicker) + f'<div class="section-head"><div><p class="eyebrow">{esc(kicker)}</p><h2>{headline}</h2></div><p class="intro">{esc(intro)}</p></div><div class="grid-3">'
    for idx, (title, text) in enumerate(cards, 1):
        body += f'<article class="card"><div class="num">{idx:02d}</div><h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
    body += "</div>"
    return page(body, number, doc, cls)


def write_html(name: str, title: str, pages: list[str]) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{esc(title)}</title><style>{CSS}</style></head>"
        f'<body><main class="book">{"".join(pages)}</main></body></html>'
    )
    (OUT / name).write_text(doc, encoding="utf-8")
    return len(pages)


def update_inventory(files: list[dict]) -> None:
    data = json.loads(INV.read_text(encoding="utf-8"))
    for product in data:
        if product.get("slug") == "videographers":
            product["customer_pdf_count"] = len(files)
            product["total_customer_pages"] = sum(f["pages"] for f in files)
            product["prompt_count"] = 52
            product["template_count_estimate"] = 137
            product["spreadsheet_count"] = 0
            product["spreadsheet_files"] = []
            product["files"] = files
            break
    INV.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    pm = json.loads(PM.read_text(encoding="utf-8"))
    for product in pm:
        if product.get("slug") == "videographers":
            product["html_file_count"] = len(files)
            product["website_status"] = "copy drafted"
            product["payhip_status"] = "copy drafted"
            product["editorial_status"] = "flagship source rebuilt; needs PDF export + human visual proof"
            product["marketing_priority"] = "flagship"
            product["notes"] = "Videographers promoted to flagship; source rebuilt with clean cinematic design, stronger content, and export-safe page structure. Needs price/cover confirmation and PDF proof."
            break
    PM.write_text(json.dumps(pm, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    files: list[dict] = []

    doc = "Start Here - Videographer Growth System"
    pages = [
        cover("Start Here: <em>Videographer</em> Growth System", "A practical implementation guide for turning the bundle into better inquiries, stronger creative briefs, smoother delivery, and more referral-ready client experiences.", doc, [("01", "Inquiry system"), ("90", "Day content plan"), ("24+", "Client templates"), ("B2B", "Wedding + commercial")]),
        intro_page(doc, 2, "Turn the bundle into a studio operating system.", "The fastest win is not making everything pretty. It is installing the moments that book projects: inquiry response, follow-up, questionnaire, package presentation, delivery message, review ask, and vendor touch."),
        section_page(doc, 3, "Install first", "The first 48 hours.", "Customize these assets before touching the rest of the bundle.", [
            ("Inquiry response", "Bookings", ul(["Create one wedding version and one corporate version.", "Add your package names, starting price, and call link.", "Save as a phone note, email template, and CRM snippet."])),
            ("Follow-up sequence", "Lost lead recovery", ul(["Use Day 3, Day 8, and Day 14 follow-ups.", "Add one relevant portfolio link to each.", "Keep the third message graceful, never desperate."])),
            ("Project questionnaire", "Client experience", ul(["Send after booking or before proposal depending on your process.", "Use answers to shape timeline, shot list, and edit priorities.", "Keep it short enough that clients finish it."])),
        ]),
        section_page(doc, 4, "7-Day Launch", "Put the system into market.", "A focused week for getting the assets live and visible.", [
            ("Day 1-2", "Foundation", ul(["Update the brand kit with your studio voice.", "Choose the primary market: wedding, commercial, corporate, or hybrid.", "Add booking links to all templates."])),
            ("Day 3-4", "Content", ul(["Write 12 captions from the calendar.", "Create 3 portfolio posts using real story context.", "Draft one YouTube or LinkedIn authority piece."])),
            ("Day 5-7", "Revenue", ul(["Send one vendor relationship email.", "Follow up with 5 warm inquiries or past clients.", "Ask for 2 reviews from recently delivered projects."])),
        ], "feature"),
        grid_page(doc, 5, "Quality gate", "Before you upload or send anything.", "Use this checklist to keep the product polished and professional.", [
            ("No generic claims", "Replace broad phrases like 'high quality video' with specific style, process, or deliverable language."),
            ("No fake metrics", "Do not invent ROI, bookings, or campaign results. Use placeholders or actual client-approved proof."),
            ("Clear next step", "Every sales asset should invite the client into one action: call, reply, book, review, or refer."),
        ], "light"),
    ]
    files.append({"file": "start-here-videographer-growth-system.html", "title": doc, "pages": write_html("start-here-videographer-growth-system.html", doc, pages), "prompts": 0, "templates": 18, "internal": False, "internal_reasons": []})

    doc = "Videographer AI Playbook"
    pages = [
        cover("<em>AI</em> Playbook Videographers", "A cinematic growth playbook for converting inquiries, presenting packages, building vendor relationships, and turning delivered films into future bookings.", doc, [("7", "Growth chapters"), ("18", "Core prompts"), ("2", "Markets"), ("1", "Studio system")]),
        intro_page(doc, 2, "Write like a strategist, not a template.", "Use AI to get to a stronger first draft. Then add your eye, your taste, your portfolio examples, and the details that make the client feel seen."),
        section_page(doc, 3, "Inquiry conversion", "Same-day responses that feel specific.", "Wedding and commercial buyers often compare multiple studios. Speed matters, but specificity wins.", [
            ("Wedding inquiry response", "Prompt", "Write a warm inquiry response for [Names], who asked about wedding videography for [date] at [venue]. Mention [specific details]. My style is [style]. Invite them to a call, briefly explain the next step, and keep it under 200 words."),
            ("Corporate inquiry response", "Prompt", "Write a confident response for [Name] at [Company] asking about [project type]. Show that I understand the business goal, ask 2 smart scope questions, and invite a discovery call. Under 200 words."),
            ("3-touch follow-up", "Prompt", "Write Day 3, Day 8, and Day 14 follow-ups for a [wedding/corporate] inquiry. Each should add value, mention one relevant portfolio example, and end with a soft next step."),
        ]),
        section_page(doc, 4, "Package strategy", "Present value before price.", "The client should understand the experience and deliverables before they compare numbers.", [
            ("Package recommendation", "Prompt", "Write a package presentation email for [client/project]. Packages: [paste packages]. Recommend the best-fit option based on [client priorities]. Confident, clear, and not pushy."),
            ("Objection response", "Prompt", "Write a reply to a client saying the package is above budget. Reinforce the value, offer a clear lower-scope option if available, and keep the relationship warm."),
            ("Premium positioning", "Prompt", "Rewrite my package description so it sounds more premium and specific. Include process, creative direction, delivery, and client experience. Avoid hype."),
        ], "feature"),
        section_page(doc, 5, "Pre-production", "Make the project feel directed.", "Great production starts before the camera comes out.", [
            ("Creative brief generator", "Prompt", "Turn these client notes into a clear creative brief: [paste notes]. Include objective, audience, tone, deliverables, must-capture moments, logistics, and open questions."),
            ("Shot priority map", "Prompt", "Create a shot priority list for [wedding/corporate project] based on [details]. Separate must-have, nice-to-have, audio moments, and risk notes."),
            ("Timeline review", "Prompt", "Review this production timeline and flag gaps, unrealistic transitions, missing setup time, audio needs, and moments that need client confirmation: [paste timeline]."),
        ]),
        section_page(doc, 6, "Vendor partnerships", "Build the referral engine.", "Photographers, planners, venues, agencies, and event producers can become repeat referral partners.", [
            ("Photographer intro", "Prompt", "Write a warm introduction to [Photographer Name]. Mention my style, how coordinated photo/video teams improve the client experience, and suggest coffee, mutual referrals, or a styled shoot."),
            ("Planner value touch", "Prompt", "Write a monthly value email to a wedding planner sharing one useful video planning insight they can pass to couples. Under 150 words, useful and not salesy."),
            ("Agency partnership", "Prompt", "Write an introduction to a marketing agency that may need video support for clients. Position me as reliable, strategic, and easy to collaborate with."),
        ], "feature"),
        section_page(doc, 7, "Content engine", "Turn finished work into demand.", "A film is not only a deliverable. It is proof, story, process, authority, and a reason to inquire.", [
            ("Portfolio story post", "Prompt", "Write an Instagram caption for a recent [wedding/commercial] film. Include the story, creative challenge, one production detail, and a booking CTA. Under 150 words."),
            ("YouTube authority idea", "Prompt", "Create a YouTube outline for [topic] that positions my studio as the expert while still being helpful to potential clients."),
            ("LinkedIn commercial post", "Prompt", "Write a LinkedIn post explaining one way strategic video helps [industry] improve trust, training, recruitment, sales, or brand clarity."),
        ]),
        section_page(doc, 8, "Delivery experience", "Make the handoff memorable.", "Delivery is where referrals are earned.", [
            ("Wedding film delivery", "Prompt", "Write a wedding film delivery email for [Names]. Include 2 personal observations, explain how to download/share, and gently plant the review ask."),
            ("Corporate asset delivery", "Prompt", "Write a professional delivery email for [Company]. Include deliverables, file structure, usage tips, revision window, and next-step suggestions."),
            ("Review request", "Prompt", "Write a review request 5-7 days after delivery. Make it warm, specific, and easy to complete. Include links for [Google/platform]."),
        ], "feature"),
        grid_page(doc, 9, "30-Day rollout", "The studio growth sprint.", "Use the playbook in a tight implementation cycle.", [
            ("Week 1", "Install inquiry response, follow-up sequence, and package presentation emails."),
            ("Week 2", "Build vendor outreach list and send 10 personalized relationship messages."),
            ("Week 3", "Batch 9 portfolio/content posts from existing projects."),
            ("Week 4", "Send review requests, referral thank-yous, and a commercial retainer pitch."),
            ("Monthly habit", "Review inquiries, booked calls, booked projects, and follow-up gaps."),
            ("Best practice", "Save every strong AI output as a studio template so the system compounds."),
        ], "light"),
    ]
    files.append({"file": "01-ai-playbook-videographers.html", "title": doc, "pages": write_html("01-ai-playbook-videographers.html", doc, pages), "prompts": 18, "templates": 26, "internal": False, "internal_reasons": []})

    calendar_months = [
        ("month-1", "Brand Story & Craft", ["Your filming philosophy", "Behind the scenes", "Portfolio story", "Corporate video purpose", "What clients get wrong", "Audio matters", "Editing process", "Vendor shoutout", "Inquiry CTA", "YouTube process video", "LinkedIn case study", "Client testimonial"]),
        ("month-2", "Authority & Education", ["How to choose a videographer", "Timeline mistakes", "Corporate video brief", "Venue lighting tip", "Why audio matters", "Package differences", "Planner collaboration", "Brand video use cases", "Film delivery experience", "FAQ carousel", "Budget education", "Book a consult"]),
        ("month-3", "Conversion & Momentum", ["Recent film launch", "Seasonal booking CTA", "Vendor relationship post", "Commercial retainer idea", "Client reaction", "Styled shoot recap", "Review post", "Limited date availability", "Corporate event checklist", "Portfolio breakdown", "Referral ask", "Final booking push"]),
    ]
    for idx, (suffix, theme, ideas) in enumerate(calendar_months, 1):
        doc = f"90-Day Content Calendar - Videographers - Month {idx}"
        pages = [
            cover(f"90-Day Content Calendar <em>Month {idx}</em>", f"Four weeks of Instagram, YouTube, and LinkedIn content built around {theme.lower()} for wedding, corporate, and commercial videography studios.", doc, [("12", "Content prompts"), ("3", "Channels"), ("4", "Weeks"), ("1", "Booking rhythm")]),
            intro_page(doc, 2, f"Month {idx}: {theme}.", "Use each idea as a post, reel, carousel, YouTube outline, or LinkedIn authority post. Pair every third post with a clear inquiry or consultation CTA."),
            grid_page(doc, 3, "Weeks 1-2", "First half of the month.", "Batch captions in one sitting, then adapt by platform.", [(f"Day {i+1}", idea) for i, idea in enumerate(ideas[:6])], "light"),
            grid_page(doc, 4, "Weeks 3-4", "Second half of the month.", "Use portfolio proof and education before the direct booking push.", [(f"Day {i+7}", idea) for i, idea in enumerate(ideas[6:])], "feature"),
            section_page(doc, 5, "AI Caption Batch", "Generate the month in one prompt.", "Copy, customize, and paste into your AI tool.", [
                ("Caption batch prompt", "Prompt", f"Write 12 social captions for a videographer for the theme '{theme}'. Mix wedding, commercial, behind-the-scenes, education, proof, and booking CTAs. Keep each under 150 words and make each feel specific, not generic."),
                ("Repurpose prompt", "Prompt", "Turn the 12 captions into: 4 reels, 2 carousels, 2 YouTube descriptions, 2 LinkedIn posts, and 2 email snippets."),
                ("Portfolio proof prompt", "Prompt", "Turn this project summary into a story-driven post: [paste project]. Include client goal, creative challenge, production detail, and result or emotional payoff."),
            ], "light"),
        ]
        fname = f"02-90day-content-calendar-videographers-{suffix}.html"
        files.append({"file": fname, "title": doc, "pages": write_html(fname, doc, pages), "prompts": 3, "templates": 15, "internal": False, "internal_reasons": []})

    doc = "Videographer Client Communication Templates"
    template_groups = [
        ("Inquiry & Booking", [("Wedding inquiry response", "Re: Your wedding videography inquiry - [Names]"), ("Corporate inquiry response", "Re: Your video project inquiry - [Company]"), ("Day 3 follow-up", "Checking in on your [project type] inquiry"), ("Post-consult booking follow-up", "Following our call - [Name]")]),
        ("Packages & Production", [("Package pricing email", "Your videography packages"), ("Pre-production questionnaire send-off", "A few details before we film"), ("Timeline check-in", "Quick timeline review"), ("Shot list confirmation", "Confirming must-capture moments")]),
        ("Delivery & Reviews", [("Wedding film delivery", "Your wedding film is ready"), ("Corporate asset delivery", "Final video files + next steps"), ("Revision window note", "Revision notes and timeline"), ("Review request", "A quick favor after your film")]),
        ("Partnerships & Growth", [("Photographer introduction", "Would love to connect"), ("Planner monthly value touch", "A video planning tip for your couples"), ("Agency introduction", "Video production support for your clients"), ("Corporate retainer pitch", "A monthly video content idea for [Company]")]),
    ]
    pages = [cover("Client Communication <em>Templates</em>", "Polished scripts for inquiries, booking, pre-production, delivery, reviews, vendor partnerships, and commercial development.", doc, [("24+", "Templates"), ("4", "Client stages"), ("2", "Markets"), ("1", "Premium experience")]), intro_page(doc, 2, "Make every message feel directed.", "Customize each template with the client details, project context, creative style, timeline, and next step.")]
    page_no = 3
    for group, items in template_groups:
        cards = []
        for title, subject in items:
            cards.append((title, "Template", f"<strong>Subject:</strong> {esc(subject)}<br><br>Hi [Name],<br><br>[Personalized opening tied to their project.] Here is the next step: [clear action]. I recommend [best-fit option or timeline] because [specific reason].<br><br>[Friendly close],<br>[Your Name] | [Studio Name]"))
        pages.append(section_page(doc, page_no, group, group, "Use these as finished client communication starters, then add your project-specific detail.", cards, "light" if page_no % 2 else "feature"))
        page_no += 1
    pages.append(section_page(doc, page_no, "Follow-up rules", "The communication standard.", "A simple operating rule for the studio.", [
        ("Respond fast", "Rule", "Reply to every inquiry within the same business day when possible. Speed signals professionalism."),
        ("Add one specific detail", "Rule", "Every message should prove you read their inquiry, watched their reference, or understood their business objective."),
        ("Make one ask", "Rule", "Do not overload the client. Ask for one decision, one call, one questionnaire, or one confirmation."),
    ], "light"))
    files.append({"file": "03-email-templates-videographers.html", "title": doc, "pages": write_html("03-email-templates-videographers.html", doc, pages), "prompts": 0, "templates": 29, "internal": False, "internal_reasons": []})

    doc = "Videographer Brand Kit"
    pages = [
        cover("Videographer <em>Brand Kit</em>", "A cinematic identity guide with palettes, typography, Canva direction, and launch assets for wedding and commercial videography studios.", doc, [("2", "Palettes"), ("7", "Canva assets"), ("1", "Studio voice"), ("7", "Day launch")]),
        intro_page(doc, 2, "Your brand books before the reel finishes.", "Clients judge taste, professionalism, and trust before they understand cameras or codecs. The brand kit makes the studio feel premium at first glance."),
        page(brand(doc, "Palette") + '<div class="section-head"><div><p class="eyebrow">Palette A</p><h2>Cinematic dark.</h2></div><p class="intro">For moody wedding films, editorial storytelling, and premium commercial work.</p></div><div class="grid-2"><div class="panel"><h3>Deep Navy</h3><div class="swatches"><div class="swatch" style="background:#111827"></div><div class="swatch" style="background:#23324d"></div><div class="swatch" style="background:#4aa8ff"></div><div class="swatch" style="background:#f6f4ee"></div></div><p>#111827 · #23324D · #4AA8FF · #F6F4EE</p></div><div class="panel"><h3>Usage</h3><p>Use dark backgrounds for portfolio stills, bright blue for CTAs and play markers, and warm off-white for editorial text blocks.</p></div></div>', 3, doc, "light"),
        page(brand(doc, "Palette") + '<div class="section-head"><div><p class="eyebrow">Palette B</p><h2>Modern commercial.</h2></div><p class="intro">For brand films, corporate retainers, agency collaborations, and crisp business-facing work.</p></div><div class="grid-2"><div class="panel"><h3>Studio Blue</h3><div class="swatches"><div class="swatch" style="background:#0b1020"></div><div class="swatch" style="background:#35e4d7"></div><div class="swatch" style="background:#7c6cff"></div><div class="swatch" style="background:#dfe7f2"></div></div><p>#0B1020 · #35E4D7 · #7C6CFF · #DFE7F2</p></div><div class="panel"><h3>Usage</h3><p>Use cyan and violet sparingly for technical polish, motion accents, data overlays, and corporate decks.</p></div></div>', 4, doc, "light"),
        grid_page(doc, 5, "Canva assets", "Build a recognizable studio system.", "Create these templates once, then reuse them across every project.", [("Film reveal post", "Hero still, title, venue/client, short story."), ("YouTube thumbnail", "Frame grab, clear title, consistent color strip."), ("LinkedIn case study", "Brief, challenge, approach, outcome."), ("Package comparison", "Three offers with deliverables and best-fit labels."), ("Testimonial card", "Client quote with project still."), ("Availability post", "Season/date CTA with elegant urgency.")], "light"),
        section_page(doc, 6, "7-Day Brand Launch", "Refresh the studio presence.", "Use this after updating colors, type, offers, and portfolio proof.", [("Days 1-2", "Foundation", ul(["Choose palette and font pairings.", "Update bio, headline, and service positioning.", "Select 8 portfolio stills that match the new direction."])), ("Days 3-5", "Assets", ul(["Build reveal, testimonial, package, and case-study templates.", "Create one YouTube thumbnail system.", "Create one LinkedIn banner or media kit slide."])), ("Days 6-7", "Publish", ul(["Post one proof story.", "Send one vendor value touch.", "Update proposal or pricing guide visuals."]))], "feature"),
    ]
    files.append({"file": "04-brand-kit-videographers.html", "title": doc, "pages": write_html("04-brand-kit-videographers.html", doc, pages), "prompts": 0, "templates": 19, "internal": False, "internal_reasons": []})

    doc = "Videographer Questionnaire and Business Development Kit"
    pages = [
        cover("Questionnaire + <em>Business Development</em> Kit", "Wedding questionnaires, corporate briefs, shot planning, styled-shoot outreach, vendor partnership scripts, and retainer development tools.", doc, [("2", "Questionnaires"), ("3", "Briefs"), ("6", "Outreach assets"), ("1", "Cleaner process")]),
        intro_page(doc, 2, "Ask better questions, make better films.", "The right questionnaire protects the production day, improves the edit, and makes the client feel like the studio is already directing the story."),
        section_page(doc, 3, "Wedding Questionnaire", "Capture the emotional priorities.", "Use this before final timeline planning.", [("Core details", "Client intake", ul(["Names, date, venue, planner, photographer, ceremony timing.", "Coverage start/end time.", "Direct day-of contact who is not the couple."])), ("Story priorities", "Creative direction", ul(["Top 3 moments they care about.", "People who must be included.", "Vows, speeches, dances, cultural or family traditions."])), ("Logistics", "Risk control", ul(["Venue restrictions, drone limits, audio restrictions.", "Lighting notes, prep locations, travel times.", "Surprises or sensitive family considerations."]))], "light"),
        section_page(doc, 4, "Corporate Brief", "Clarify the business objective.", "Use this before quoting or pre-production.", [("Objective", "Strategy", ul(["What should the video help accomplish?", "Who is the audience?", "Where will it be used?"])), ("Deliverables", "Scope", ul(["Main edit length.", "Cutdowns or vertical clips.", "Captions, thumbnails, raw footage, usage needs."])), ("Approvals", "Workflow", ul(["Decision maker.", "Revision rounds.", "Brand guidelines, legal review, launch date."]))], "feature"),
        section_page(doc, 5, "Production Planning", "Make the shoot smoother.", "Use these before final confirmation.", [("Shot list guide", "Must-capture", ul(["Hero moments.", "Audio moments.", "Detail shots.", "People and environment.", "Backup B-roll."])), ("Timeline review", "Pre-production", ul(["Arrival/setup.", "Travel between locations.", "Audio setup.", "Golden hour or lighting priorities.", "Buffer time."])), ("Delivery plan", "Post-production", ul(["File naming.", "Delivery platform.", "Review window.", "Final asset formats.", "Archive policy."]))], "light"),
        section_page(doc, 6, "Partnership Tools", "Create referral-ready relationships.", "Use these for photographers, planners, venues, and agencies.", [("Styled shoot pitch", "Wedding market", "Propose a clear concept, partner value, usage plan, deliverables, and timeline. Make the collaboration easy to say yes to."), ("Vendor referral note", "Local network", "Create a warm monthly check-in that shares one useful planning insight and one recent project link."), ("Agency support pitch", "Commercial market", "Position the studio as a reliable production partner for campaigns, launches, recruiting, training, and client content.")], "feature"),
        grid_page(doc, 7, "Implementation", "The clean client process.", "This kit becomes a repeatable operating flow.", [("Inquiry", "Send the right questionnaire only after the client has context."), ("Proposal", "Use questionnaire answers to recommend the package."), ("Pre-production", "Turn answers into timeline, shot priorities, and logistics."), ("Production", "Keep must-capture moments visible."), ("Delivery", "Use client goals to shape the handoff email."), ("Referral", "Ask partners and clients while the experience is fresh.")], "light"),
    ]
    files.append({"file": "05-questionnaire-kit-videographers.html", "title": doc, "pages": write_html("05-questionnaire-kit-videographers.html", doc, pages), "prompts": 0, "templates": 22, "internal": False, "internal_reasons": []})

    doc = "5 Free AI Prompts for Videographers"
    pages = [
        cover("5 Free <em>AI Prompts</em> to Book More Clients", "Copy, paste, customize, and turn inquiry replies, delivery emails, vendor outreach, and social posts into stronger booking assets.", doc, [("5", "Prompts"), ("<5", "Minutes each"), ("2", "Markets"), ("1", "Next booking")]),
        section_page(doc, 2, "Prompts 1-2", "Inquiry conversion.", "Use these when a new lead lands.", [("Wedding inquiry response", "Prompt", "Write a warm inquiry response for [Names], wedding date [date], venue [venue]. They mentioned [details]. My style is [style]. Make them feel seen, briefly explain my approach, mention packages, and invite them to a call."), ("Corporate inquiry response", "Prompt", "Write a professional response for [Name] at [Company] asking about [project]. Show I understand their business objective, ask 2 smart scope questions, and invite a discovery call.")], "light"),
        section_page(doc, 3, "Prompts 3-4", "Delivery and referral.", "Use these after the project is finished.", [("Wedding film delivery", "Prompt", "Write a wedding film delivery email for [Names]. Include 2 personal observations from the day, the film link, download/share notes, and a gentle review seed."), ("Photographer partnership intro", "Prompt", "Write a warm introduction to [Photographer Name]. Mention my studio style, why coordinated photo/video teams help couples, and suggest coffee, mutual referrals, or a styled shoot.")], "feature"),
        section_page(doc, 4, "Prompt 5", "Content batch.", "Turn one sitting into visibility.", [("5-caption batch", "Prompt", "Write 5 Instagram captions for a videographer specializing in [wedding/commercial/both]. Topics: a project story, a craft lesson, a client mistake to avoid, a behind-the-scenes insight, and a booking CTA. Under 150 words each.")], "light"),
    ]
    files.append({"file": "lm-videographers.html", "title": doc, "pages": write_html("lm-videographers.html", doc, pages), "prompts": 5, "templates": 8, "internal": False, "internal_reasons": []})

    update_inventory(files)
    print(f"Built {len(files)} Videographer files in {OUT}")
    print(f"Total pages: {sum(f['pages'] for f in files)}")


if __name__ == "__main__":
    main()
