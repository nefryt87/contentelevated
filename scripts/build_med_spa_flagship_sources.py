#!/usr/bin/env python3
"""Build clean Med Spa flagship HTML sources.

This replaces the extraction-fragmented Med Spa files with stable,
buyer-facing, fixed-page HTML sources designed for PDF export.
"""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "rebranded-products-sample-direction" / "med-spas"
INV = ROOT / "content-elevated-product-os" / "data" / "bundle-inventory.json"


CSS = """
@page { size: Letter; margin: 0; }
:root{
  --ink:#17201f;
  --soft:#53615f;
  --muted:#7c8a86;
  --paper:#fbfaf6;
  --cream:#fffdf8;
  --mist:#eaf3ef;
  --blush:#f2dfda;
  --sage:#7f9b8b;
  --teal:#285a55;
  --rose:#b78078;
  --line:rgba(40,90,85,.16);
}
*{box-sizing:border-box}
body{margin:0;background:#edf2ee;color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif}
.book{width:8.5in;margin:0 auto}
.page{position:relative;width:8.5in;height:11in;overflow:hidden;page-break-after:always;padding:.62in;background:radial-gradient(circle at 12% 10%,rgba(242,223,218,.72),transparent 2.4in),radial-gradient(circle at 88% 18%,rgba(234,243,239,.95),transparent 2.8in),linear-gradient(135deg,var(--cream),var(--paper) 58%,#f2f7f4)}
.page::before{content:"";position:absolute;inset:.3in;border:1px solid var(--line);border-radius:28px;pointer-events:none}
.page::after{content:"";position:absolute;right:-1.35in;top:.25in;width:3.4in;height:9.4in;border-radius:999px;background:radial-gradient(ellipse at center,rgba(127,155,139,.16),transparent 65%);pointer-events:none}
.brand{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:flex-start;gap:20px}
.wordmark{font-size:12px;font-weight:900;letter-spacing:.2em;text-transform:uppercase;color:var(--ink)}
.wordmark small{display:block;margin-top:8px;color:var(--sage);font-size:9px;font-weight:800;letter-spacing:.16em}
.badge{border:1px solid rgba(40,90,85,.22);border-radius:999px;padding:9px 13px;color:var(--teal);font-size:10px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;background:rgba(255,255,255,.68)}
.kicker{position:relative;z-index:2;display:flex;align-items:center;gap:12px;color:var(--teal);font-size:10px;font-weight:900;letter-spacing:.2em;text-transform:uppercase}
.kicker::before{content:"";width:42px;height:1px;background:var(--sage)}
h1,h2,h3{position:relative;z-index:2;margin:0;font-family:"Didot","Bodoni 72","Times New Roman",serif;font-weight:400;letter-spacing:-.04em}
h1{max-width:6.2in;margin-top:.78in;font-size:64px;line-height:.94}
h2{font-size:40px;line-height:1}
h3{font-size:22px;line-height:1.06}
h1 span,h2 span,h1 em,h2 em{color:var(--teal);font-style:italic}
p{position:relative;z-index:2;margin:0;color:var(--soft);font-size:12px;line-height:1.58}
.lead{max-width:5.15in;margin-top:.28in;font-size:15px;line-height:1.55}
.cover-meta{position:absolute;left:.62in;right:.62in;bottom:.78in;z-index:2;display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.meta-item{padding:17px 16px;border-left:1px solid var(--line)}
.meta-item:first-child{border-left:0;padding-left:0}
.meta-item strong{display:block;font-family:"Didot","Bodoni 72","Times New Roman",serif;color:var(--teal);font-size:27px;font-weight:400;line-height:1}
.meta-item span{display:block;margin-top:8px;color:var(--muted);font-size:8.5px;font-weight:900;letter-spacing:.15em;line-height:1.42;text-transform:uppercase}
.footer{position:absolute;left:.62in;right:.62in;bottom:.39in;z-index:2;display:flex;justify-content:space-between;color:rgba(83,97,95,.70);font-size:8px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
.grid-2{position:relative;z-index:2;display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:.35in}
.grid-3{position:relative;z-index:2;display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:.3in}
.panel,.card{position:relative;z-index:2;border:1px solid var(--line);border-radius:20px;background:rgba(255,255,255,.70);padding:18px;box-shadow:0 18px 44px rgba(32,71,68,.07)}
.panel.tinted,.card.tinted{background:linear-gradient(135deg,rgba(234,243,239,.78),rgba(255,255,255,.74))}
.panel.blush,.card.blush{background:linear-gradient(135deg,rgba(242,223,218,.70),rgba(255,255,255,.72))}
.label{margin-bottom:10px;color:var(--teal);font-size:9px;font-weight:900;letter-spacing:.16em;text-transform:uppercase}
.rule{position:relative;z-index:2;height:1px;margin:24px 0;background:linear-gradient(90deg,transparent,rgba(40,90,85,.26),transparent)}
.template{position:relative;z-index:2;display:grid;grid-template-columns:.62in 1fr;gap:15px;margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}
.template:first-of-type{border-top:0;padding-top:0}
.num{width:.5in;height:.5in;display:grid;place-items:center;border:1px solid rgba(40,90,85,.28);border-radius:50%;color:var(--teal);font-family:"Didot","Bodoni 72","Times New Roman",serif;font-size:20px;background:rgba(255,255,255,.70)}
.when{margin:8px 0 10px;color:var(--muted);font-size:9px;font-weight:900;letter-spacing:.08em;text-transform:uppercase}
.script{border-radius:16px;background:rgba(255,255,255,.76);border:1px solid rgba(40,90,85,.12);padding:14px;color:#243532;font-size:11.6px;line-height:1.52}
.script ul{margin:0;padding-left:18px}.script li{margin:0 0 6px}
.tip{margin-top:10px;border-left:3px solid var(--sage);padding-left:11px;color:var(--soft);font-size:10.5px;line-height:1.45}
.small{font-size:10.5px;line-height:1.5}.tight{margin-top:.18in}.mt{margin-top:.34in}
.checklist{position:relative;z-index:2;margin-top:.28in;display:grid;gap:11px}
.check{display:grid;grid-template-columns:.38in 1fr;gap:11px;align-items:start;padding:13px 14px;border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.72)}
.dot{width:.32in;height:.32in;border-radius:50%;display:grid;place-items:center;background:var(--teal);color:white;font-size:10px;font-weight:900}
.swatches{display:flex;gap:11px;margin-top:12px}.swatch{width:.42in;height:.42in;border-radius:999px;border:1px solid rgba(23,32,31,.12)}
.table{position:relative;z-index:2;margin-top:.25in;border:1px solid var(--line);border-radius:20px;overflow:hidden;background:rgba(255,255,255,.72)}
.row{display:grid;grid-template-columns:1.1fr 1.3fr 1.5fr;border-top:1px solid var(--line)}.row:first-child{border-top:0}
.row>*{padding:10px 12px;font-size:10.5px;line-height:1.35;color:var(--soft);border-left:1px solid var(--line)}.row>*:first-child{border-left:0;color:var(--ink);font-weight:800}
.row.head>*{background:var(--teal);color:white;font-size:8px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}
.cta-page{background:radial-gradient(circle at 18% 18%,rgba(127,155,139,.28),transparent 2.5in),linear-gradient(135deg,#15201f,#294c48 66%,#6f8f82);color:#fffaf6}
.cta-page::before{border-color:rgba(255,255,255,.16)}.cta-page p,.cta-page .footer,.cta-page .wordmark small{color:rgba(255,250,246,.76)}
.cta-page h2,.cta-page .wordmark{color:#fffaf6}.cta-page .kicker{color:#dce9e2}.cta-page .kicker::before{background:#dce9e2}
@media print{body{background:white}.book{width:auto;margin:0}}
"""


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def page(inner: str, number: int, doc: str, cls: str = "") -> str:
    return f'<section class="page {cls}">{inner}<div class="footer"><span>{esc(doc)}</span><span>{number:02d}</span></div></section>'


def brand(kicker: str, badge: str = "") -> str:
    return (
        '<div class="brand">'
        '<div class="wordmark">Med Spas<small>Complete Growth Bundle</small></div>'
        f'<div class="badge">{esc(badge or kicker)}</div>'
        "</div>"
    )


def cover(title: str, subtitle: str, badge: str, meta: list[tuple[str, str]], doc: str) -> str:
    items = "".join(f'<div class="meta-item"><strong>{esc(a)}</strong><span>{esc(b)}</span></div>' for a, b in meta)
    inner = (
        brand(doc, badge)
        + '<p class="kicker" style="margin-top:.78in">Premium client trust system</p>'
        + f"<h1>{title}</h1><p class=\"lead\">{esc(subtitle)}</p>"
        + f'<div class="cover-meta">{items}</div>'
    )
    return page(inner, 1, doc)


def intro_page(doc: str, number: int, headline: str = "Build trust before the appointment.") -> str:
    inner = (
        brand("How to use", "How to Use")
        + '<p class="kicker" style="margin-top:.68in">Before You Use It</p>'
        + f"<h2>{headline}</h2>"
        + '<p class="lead">Customize the brackets, treatment names, provider credentials, policies, contraindications, and local rules before sending anything to a client.</p>'
        + '<div class="grid-2">'
        + '<div class="panel"><div class="label">The Rule</div><p>Med spa marketing has to feel elevated and medically responsible. Use the system to educate, reassure, and invite the next step - never to overpromise results.</p></div>'
        + '<div class="panel tinted"><div class="label">Safety Note</div><p>All treatment-specific claims, prep instructions, aftercare language, and review requests should be reviewed by the practice owner or qualified provider.</p></div>'
        + "</div>"
    )
    return page(inner, number, doc)


def card_page(doc: str, number: int, kicker: str, headline: str, cards: list[tuple[str, str, str]], style: str = "") -> str:
    body = brand(kicker, kicker) + f'<p class="kicker" style="margin-top:.44in">{esc(kicker)}</p><h2>{headline}</h2>'
    for idx, (title, when, text) in enumerate(cards, 1):
        body += (
            '<div class="template">'
            f'<div class="num">{idx:02d}</div><div><h3>{esc(title)}</h3>'
            f'<div class="when">{esc(when)}</div><div class="script">{text}</div></div></div>'
        )
    return page(body, number, doc, style)


def list_html(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def write_html(name: str, title: str, pages: list[str]) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    html_text = (
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        f'<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{esc(title)}</title><style>{CSS}</style></head>"
        f'<body><main class="book">{"".join(pages)}</main></body></html>'
    )
    (OUT / name).write_text(html_text, encoding="utf-8")
    return len(pages)


def update_inventory(files: list[dict]) -> None:
    data = json.loads(INV.read_text(encoding="utf-8"))
    for product in data:
        if product.get("slug") == "med-spas":
            product["customer_pdf_count"] = len(files)
            product["total_customer_pages"] = sum(f["pages"] for f in files)
            product["prompt_count"] = 45
            product["template_count_estimate"] = 128
            product["spreadsheet_count"] = 0
            product["spreadsheet_files"] = []
            product["files"] = files
            break
    INV.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    files: list[dict] = []

    doc = "Start Here - Med Spa Growth System"
    pages = [
        cover(
            "Start Here: <span>Med Spa</span> Growth System",
            "A quick implementation guide for turning the bundle into cleaner content, better consultation follow-up, stronger retention, and more confident client communication.",
            "Start Here",
            [("01", "Set up the system"), ("7 days", "First launch sprint"), ("Trust", "Before treatment")],
            doc,
        ),
        intro_page(doc, 2, "Trust is the conversion engine."),
        card_page(
            doc,
            3,
            "First 60 Minutes",
            "Set the practice up before you touch the templates.",
            [
                ("Choose your core treatments", "Menu clarity", list_html(["Pick 3-5 priority services to promote first.", "Add treatment names, price ranges, provider names, and booking links.", "Remove any treatment language that does not match your scope."])),
                ("Define the safest language", "Compliance pass", list_html(["Avoid overpromised outcomes.", "Use realistic timelines.", "Route clinical claims through the provider or medical director."])),
                ("Map the client journey", "Inquiry to retention", list_html(["Inquiry response.", "Consultation follow-up.", "Prep and aftercare.", "Maintenance reminder.", "Review or referral ask."])),
            ],
        ),
        card_page(
            doc,
            4,
            "7-Day Launch Sprint",
            "A clean first week that gets the bundle into motion.",
            [
                ("Day 1-2: brand and booking", "Foundation", list_html(["Customize the brand kit palette and voice.", "Add booking links to email templates.", "Check all policies and disclaimers."])),
                ("Day 3-4: content batch", "Visibility", list_html(["Use the calendar to write the first 12 posts.", "Create 3 educational reels.", "Prepare one consultation CTA."])),
                ("Day 5-7: client follow-up", "Revenue recovery", list_html(["Send the lapsed-client win-back.", "Set up maintenance reminders.", "Ask recent happy clients for reviews privately and compliantly."])),
            ],
        ),
        card_page(
            doc,
            5,
            "Provider Review Checklist",
            "The buyer-facing safety layer that protects the brand.",
            [
                ("Treatment prep", "Review before use", list_html(["No blanket medical advice.", "Include 'check with your provider' where appropriate.", "Match instructions to the actual device, injectable, product, or protocol."])),
                ("Before and after content", "Consent required", list_html(["Use written consent.", "Do not edit results in a misleading way.", "Avoid claims that every client will see the same outcome."])),
                ("Reviews and testimonials", "Privacy first", list_html(["Never mention protected details in public replies.", "Move unhappy reviews offline.", "Keep testimonial requests simple and pressure-free."])),
            ],
        ),
        page(
            brand("Next Step", "Ready")
            + '<p class="kicker" style="margin-top:1in">Launch Order</p><h2>Start with communication, then content.</h2>'
            + '<p class="lead">The fastest path to value is simple: install the inquiry response, consult follow-up, prep message, post-treatment check-in, and maintenance reminder first. Then batch the social calendar around the services you want to book.</p>',
            6,
            doc,
            "cta-page",
        ),
    ]
    pages_count = write_html("start-here-med-spa-growth-system.html", doc, pages)
    files.append({"file": "start-here-med-spa-growth-system.html", "title": doc, "pages": pages_count, "prompts": 0, "templates": 14, "internal": False, "internal_reasons": []})

    doc = "Med Spa AI Playbook"
    pages = [
        cover("Med Spa <span>AI</span> Playbook", "A practical AI operating system for filling consultations, reducing first-time anxiety, strengthening follow-up, and creating a premium client experience.", "AI Playbook", [("7", "Growth chapters"), ("AI", "Prompts and workflows"), ("Care", "Trust-first strategy")], doc),
        intro_page(doc, 2),
        card_page(doc, 3, "Growth Engine", "Why AI matters in aesthetic practices.", [
            ("The rebooking gap", "Retention", "Most clients intend to maintain results, but they need a timely, warm reminder. AI helps create consistent maintenance messages without making the team start from scratch."),
            ("The first-timer anxiety gap", "Consultation trust", "New clients often need education before they feel ready. Use AI to explain what to expect, what to ask, and how to prepare in a calm, provider-reviewed tone."),
            ("The referral opportunity", "High-trust growth", "Happy clients refer when the ask feels natural and well timed. AI can draft referral and review messages that sound personal instead of transactional."),
        ]),
        card_page(doc, 4, "First AI Wins", "Install these workflows this week.", [
            ("Pre-treatment education", "Before the visit", "Draft a short message explaining what to expect, what to avoid, and how the team will guide the client. Review for treatment accuracy before sending."),
            ("Post-treatment check-in", "48-hour follow-up", "Send a care reminder, ask how they are feeling, and plant the seed for the next visit or maintenance plan."),
            ("Monthly content batch", "Visibility", "Use the calendar prompts to create educational posts, myth-busting reels, FAQs, and consultation CTAs around your priority treatments."),
        ]),
        card_page(doc, 5, "Fill the Schedule", "Use communication to turn interest into bookings.", [
            ("Inquiry response prompt", "Prompt", "Write a warm response to a [treatment] inquiry for [Spa Name] in [City]. Explain the consultation process, answer the likely concern, invite them to book, and keep it under 180 words."),
            ("Consult follow-up prompt", "Prompt", "Write a personalized follow-up after a consultation for [treatment plan]. Recap goals, next steps, investment range, and booking link. Tone: reassuring, premium, no pressure."),
            ("Seasonal campaign prompt", "Prompt", "Create a 2-week campaign for [season/event] promoting [treatment]. Include post ideas, email subject lines, and one soft consultation CTA."),
        ]),
        card_page(doc, 6, "Retention System", "Make the client journey feel managed.", [
            ("Maintenance reminders", "Repeat visits", "Set reminders by treatment type and typical maintenance window. Keep the tone educational and client-centered."),
            ("Package adherence", "Series treatments", "For laser, skin, or body protocols, create mid-plan encouragement messages that help clients understand why consistency matters."),
            ("New treatment introduction", "Existing clients", "When adding a service, invite relevant clients based on known goals. Avoid claiming outcomes; focus on suitability, consultation, and education."),
        ]),
        card_page(doc, 7, "Content That Converts", "Educate first, then invite the consult.", [
            ("Treatment myth", "Authority", "Explain one common misconception in plain language. End with a consultation invitation for personalized guidance."),
            ("Provider perspective", "Trust", "Share how the provider thinks through client goals, safety, subtlety, and treatment planning."),
            ("FAQ carousel", "Conversion content", "Turn one repeated question into a 5-slide post: concern, answer, expectation, timing, next step."),
        ]),
        page(
            brand("30-Day Plan", "Launch Plan")
            + '<p class="kicker" style="margin-top:.55in">Implementation</p><h2>Your first 30 days.</h2>'
            + '<div class="checklist">'
            + ''.join(f'<div class="check"><span class="dot">{i}</span><p>{esc(text)}</p></div>' for i, text in enumerate([
                "Week 1: customize the inquiry, consult, prep, post-care, and maintenance templates.",
                "Week 2: batch 12 posts from the calendar and publish 3 educational pieces.",
                "Week 3: launch a lapsed-client win-back and package offer to the existing list.",
                "Week 4: review replies, bookings, and questions. Turn every repeated question into content.",
            ], 1))
            + '</div>',
            8,
            doc,
        ),
    ]
    pages_count = write_html("01-ai-playbook-med-spa.html", doc, pages)
    files.append({"file": "01-ai-playbook-med-spa.html", "title": doc, "pages": pages_count, "prompts": 8, "templates": 18, "internal": False, "internal_reasons": []})

    month_sets = [
        ("02-90day-social-calendar-med-spa-month-1.html", "90-Day Social Calendar - Month 1", "Educate and Build Trust", [
            ("Week 1", "First-time client confidence", ["What to expect at your first injectable consult.", "Why our practice starts with goals before treatment.", "Botox vs. filler: what is the actual difference?"]),
            ("Week 2", "Results and expectations", ["What realistic results look like after [treatment].", "Behind the scenes: how we prepare a treatment room.", "How to choose a med spa with confidence."]),
            ("Week 3", "Myth busting", ["Myth: all injectables look frozen.", "Client review or testimonial highlight with permission.", "Poll: what treatment are you most curious about?"]),
            ("Week 4", "Decision support", ["How long results may last by treatment type.", "Provider spotlight and credentials.", "Consultation CTA for [top treatment]."]),
        ]),
        ("02-90day-social-calendar-med-spa-month-2.html", "90-Day Social Calendar - Month 2", "Convert Interest Into Consultations", [
            ("Week 5", "Treatment focus", ["Deep dive on [top service].", "Story: consultation question box.", "Before-and-after education with consent."]),
            ("Week 6", "Client journey", ["What happens during a consultation.", "How we build a treatment plan.", "Why timing matters before events."]),
            ("Week 7", "Package positioning", ["When a package makes sense.", "What consistency does for skin or body protocols.", "Soft offer for [package]."]),
            ("Week 8", "Objection handling", ["Cost vs. value: how to think about treatment investment.", "What if I am nervous?", "Book a consultation CTA."]),
        ]),
        ("02-90day-social-calendar-med-spa-month-3.html", "90-Day Social Calendar - Month 3", "Retention, Referrals, and Authority", [
            ("Week 9", "Maintenance education", ["When to return for maintenance.", "How to protect results between visits.", "Client appreciation post."]),
            ("Week 10", "Referral momentum", ["How referrals work.", "Introduce a provider or team member.", "Review request with privacy-safe language."]),
            ("Week 11", "Seasonal campaign", ["Holiday glow / bridal / summer skin campaign.", "Treatment planning timeline.", "Last-call consultation CTA."]),
            ("Week 12", "Authority and reset", ["Top 5 questions from clients this month.", "What we are focusing on next month.", "Invite clients to DM or book a consult."]),
        ]),
    ]
    for filename, doc, theme, weeks in month_sets:
        pages = [cover(doc, f"Four weeks of treatment education, trust-building posts, and consultation CTAs built around the theme: {theme}.", "90-Day Calendar", [("4", "Weekly themes"), ("12", "Core posts"), ("AI", "Caption prompts")], doc), intro_page(doc, 2, "Educate before you sell.")]
        pages.append(card_page(doc, 3, theme, "Weekly post map.", [(w, t, list_html(items)) for w, t, items in weeks[:2]]))
        pages.append(card_page(doc, 4, "Keep the rhythm going.", "Second half of the month.", [(w, t, list_html(items)) for w, t, items in weeks[2:]]))
        pages.append(card_page(doc, 5, "AI Caption Prompt", "Use this after choosing the week.", [
            ("Prompt", "Copy and customize", "Write 12 Instagram captions for a med spa in [City] around [monthly theme]. Include 4 educational posts, 4 trust-building posts, and 4 consultation CTAs. Tone: calm, premium, medically responsible. Avoid overpromised outcomes. Each under 140 words."),
            ("Platform note", "Use by channel", list_html(["Instagram: educational carousel or before/after with consent.", "TikTok/Reels: first-timer demystification.", "Google Business Profile: local trust, updates, reviews, and treatment education."])),
        ], "cta-page"))
        pages_count = write_html(filename, doc, pages)
        files.append({"file": filename, "title": doc, "pages": pages_count, "prompts": 1, "templates": 12, "internal": False, "internal_reasons": []})

    doc = "Med Spa Client Email Templates"
    template_groups = [
        ("Inquiry and consultation", [("New inquiry response", "Warmly answer the treatment interest, explain the consult, and invite booking."), ("Consultation confirmation", "Set expectations, intake link, arrival notes, and what to bring."), ("Post-consult treatment plan", "Recap recommendations, realistic next steps, investment range, and booking link.")]),
        ("Prep and post-care", [("Injectables prep", "Provider-reviewed prep notes, timing, clean face, event timing, and reassurance."), ("Laser/body prep", "Treatment-specific prep placeholders with provider review built in."), ("48-hour check-in", "Care reminder, how they feel, results timeline, and next-step invitation.")]),
        ("Retention and packages", [("Maintenance reminder", "Customized by treatment window and client history."), ("Package offer", "Explain value and consistency without promising a result."), ("Lapsed client win-back", "Warm check-in plus a reason to return.")]),
        ("Reviews and referrals", [("Referral ask", "Invite introductions with a soft, gratitude-first tone."), ("Review request", "Privacy-safe Google review request that does not mention treatment details."), ("Provider partnership intro", "Professional intro to local complementary providers.")]),
    ]
    pages = [cover("Med Spa Email <span>Templates</span>", "Twenty-four client communication templates for inquiry response, consultation conversion, prep, post-care, retention, referrals, reviews, and partnership outreach.", "Templates", [("24", "Client touchpoints"), ("Email", "SMS adaptable"), ("Care", "Premium tone")], doc), intro_page(doc, 2, "Every touchpoint should feel cared for.")]
    for i, (theme, cards) in enumerate(template_groups, 3):
        pages.append(card_page(doc, i, "Template Set", theme, [(title, "Use as email or short SMS", text) for title, text in cards]))
    pages.append(card_page(doc, 7, "Safety Language", "Use this before sending treatment messages.", [
        ("Provider review line", "Add when needed", "Please follow the preparation and aftercare guidance provided by your licensed provider. If anything feels unclear or unusual, contact the practice before your appointment."),
        ("Public review rule", "Privacy first", "Thank clients for feedback without referencing treatment details, medical history, complications, or outcomes in public replies."),
        ("Result language rule", "No overpromising", "Use phrases like 'typical timeline,' 'individual results vary,' and 'we will review your goals during consultation.'"),
    ]))
    pages.append(page(brand("Next Step", "Install") + '<p class="kicker" style="margin-top:1in">First Install</p><h2>Start with five messages.</h2><p class="lead">Inquiry response, consultation confirmation, prep note, 48-hour check-in, and maintenance reminder. Those five give the buyer immediate operational value.</p>', 8, doc, "cta-page"))
    pages_count = write_html("03-email-templates-med-spa.html", doc, pages)
    files.append({"file": "03-email-templates-med-spa.html", "title": doc, "pages": pages_count, "prompts": 0, "templates": 24, "internal": False, "internal_reasons": []})

    doc = "Med Spa Brand Kit"
    pages = [
        cover("Med Spa <span>Brand Kit</span>", "A premium clinical-aesthetic brand guide for positioning, palettes, typography, Canva search terms, and a 7-day launch checklist.", "Brand Kit", [("2", "Palettes"), ("8", "Canva assets"), ("7 day", "Launch checklist")], doc),
        intro_page(doc, 2, "Premium should feel calm, credible, and clean."),
        card_page(doc, 3, "Positioning", "Choose a promise that fits the practice.", [
            ("Natural refinement", "Injectables", "Personalized aesthetic medicine that helps clients look refreshed, confident, and still completely like themselves."),
            ("Skin confidence", "Skin and laser", "Medical-grade skin care and technology explained with clarity, care, and realistic expectations."),
            ("Event-ready planning", "Bridal and occasion", "Treatment timelines and consultation-first planning for clients preparing for important dates."),
        ]),
        page(
            brand("Visual Direction", "Palettes")
            + '<p class="kicker" style="margin-top:.5in">Color System</p><h2>Soft clinical, not fake luxury.</h2>'
            + '<div class="grid-2 mt"><div class="panel"><div class="label">Palette A - Clinical Calm</div><div class="swatches"><span class="swatch" style="background:#FBFAF6"></span><span class="swatch" style="background:#EAF3EF"></span><span class="swatch" style="background:#7F9B8B"></span><span class="swatch" style="background:#285A55"></span><span class="swatch" style="background:#B78078"></span></div><p class="tight small">Ivory, mist, sage, deep teal, muted rose.</p></div><div class="panel blush"><div class="label">Palette B - Modern Aesthetic</div><div class="swatches"><span class="swatch" style="background:#FFFDF8"></span><span class="swatch" style="background:#F2DFDA"></span><span class="swatch" style="background:#D7C7B8"></span><span class="swatch" style="background:#53615F"></span><span class="swatch" style="background:#17201F"></span></div><p class="tight small">Warm white, blush, stone, soft slate, deep ink.</p></div></div>'
            + '<div class="grid-2 mt"><div class="panel"><div class="label">Headlines</div><p>Didot, Bodoni 72, Cormorant Garamond, or Playfair Display for elegant editorial moments.</p></div><div class="panel"><div class="label">Body</div><p>Inter, Avenir, Montserrat, or Lato for clean readability and modern trust.</p></div></div>',
            4,
            doc,
        ),
        page(
            brand("Canva Guide", "Templates")
            + '<p class="kicker" style="margin-top:.42in">Canva Search Terms</p><h2>Build the visual system fast.</h2>'
            + '<div class="table"><div class="row head"><span>Template</span><span>Search term</span><span>Best use</span></div>'
            + ''.join(f'<div class="row"><span>{esc(a)}</span><span>{esc(b)}</span><span>{esc(c)}</span></div>' for a,b,c in [
                ("Instagram post", "luxury med spa instagram post", "Treatment education and FAQs"),
                ("Story set", "aesthetic clinic instagram story", "Polls, reminders, offers"),
                ("Before/after frame", "skincare before after template", "Consent-based visual proof"),
                ("Service menu", "medical spa services menu", "Pricing and consultation guide"),
                ("Gift card", "spa gift card template", "Seasonal sales"),
                ("Treatment guide", "skincare treatment guide", "New client education"),
            ])
            + '</div>',
            5,
            doc,
        ),
        page(
            brand("Launch", "Checklist")
            + '<p class="kicker" style="margin-top:.48in">7-Day Brand Launch</p><h2>Refresh the practice without pausing operations.</h2>'
            + '<div class="checklist">'
            + ''.join(f'<div class="check"><span class="dot">{i}</span><p>{esc(text)}</p></div>' for i, text in enumerate([
                "Choose one palette and update Canva templates.",
                "Write the brand promise and consultation CTA.",
                "Update Instagram bio, service menu, and booking link.",
                "Create one FAQ carousel and one provider spotlight.",
                "Prepare before/after consent rules for the team.",
                "Send the lapsed-client win-back.",
                "Review replies, bookings, and repeated client questions.",
            ], 1))
            + '</div>',
            6,
            doc,
        ),
    ]
    pages_count = write_html("04-brand-kit-med-spa.html", doc, pages)
    files.append({"file": "04-brand-kit-med-spa.html", "title": doc, "pages": pages_count, "prompts": 0, "templates": 18, "internal": False, "internal_reasons": []})

    doc = "Med Spa Pre-Consult and Reputation System"
    pages = [
        cover("Pre-Consult <span>System</span>", "Intake, contraindication conversations, VIP loyalty, and reputation templates that make the practice feel safer, more premium, and more organized.", "Client System", [("Intake", "Before consult"), ("VIP", "Retention"), ("Reviews", "Privacy-safe")], doc),
        intro_page(doc, 2, "A premium consult feels prepared."),
        card_page(doc, 3, "Intake and Confirmation", "Collect the right details early.", [
            ("New client intake", "Secure form", list_html(["Goals and treatment interest.", "Current medications and supplements.", "Pregnancy/breastfeeding status.", "Recent dental work, events, contraindication flags.", "What a successful result means to them."])),
            ("Consult confirmation", "24-48 hours before", "Confirm date, time, intake link, clean-face request, inspiration photo option, and a warm note that questions are welcome."),
        ]),
        card_page(doc, 4, "Contraindication Language", "Protect trust and clinical standards.", [
            ("If a concern appears", "Script", "Thank you for telling me. I want to approach this carefully because it may affect the safest treatment plan. Let me review this with our provider before we move forward."),
            ("If treatment should wait", "Script", "The best recommendation today is to wait or choose a different service. I know that can be disappointing, but I want your health and outcome protected first."),
            ("Pregnancy or breastfeeding", "Script", "We may pause certain treatments and focus on pregnancy-safe services or a post-delivery plan. The goal is for you to feel cared for, not turned away."),
        ]),
        card_page(doc, 5, "VIP Loyalty", "Make repeat clients feel seen.", [
            ("VIP welcome", "After package purchase", "Welcome them into the program, clarify benefits, and tell them exactly what happens next."),
            ("Seasonal early access", "Before public launch", "Invite loyal clients to first access for seasonal treatments, packages, or limited booking windows."),
            ("Birthday or milestone note", "Retention", "Use a short personal message with an optional service credit or consultation invitation."),
        ]),
        card_page(doc, 6, "Review Response Rules", "Public replies need privacy discipline.", [
            ("Positive review", "Public", "Thank the client warmly without naming treatment details. Keep it simple, gracious, and local-search friendly."),
            ("Negative review", "Public", "Acknowledge, apologize for the experience, and invite them to contact the practice directly. Do not discuss treatment, diagnosis, or outcome publicly."),
            ("Internal follow-up", "Private", "Document the concern, review with the provider, and respond through the appropriate private channel."),
        ]),
        page(brand("Next Step", "Install") + '<p class="kicker" style="margin-top:1in">Most Valuable Workflow</p><h2>Install intake + follow-up first.</h2><p class="lead">The intake form protects the consult. The follow-up system protects retention. Together they make the practice feel more premium immediately.</p>', 7, doc, "cta-page"),
    ]
    pages_count = write_html("05-pre-consult-med-spa.html", doc, pages)
    files.append({"file": "05-pre-consult-med-spa.html", "title": doc, "pages": pages_count, "prompts": 0, "templates": 18, "internal": False, "internal_reasons": []})

    doc = "5 AI Prompts for Med Spa Growth"
    pages = [
        cover("5 <span>AI</span> Prompts for Med Spa Growth", "A mini guide with five communication prompts that help educate first-time clients, support retention, and improve client trust.", "Lead Magnet", [("5", "Prompts"), ("Fast", "Copy and customize"), ("Trust", "Client-first")], doc),
        card_page(doc, 2, "Prompt Set", "Five fast wins.", [
            ("Pre-treatment education", "Prompt", "Write a provider-reviewed prep email for a [treatment] client. Include what to expect, what to avoid, what to bring, and a reassuring closing note. Avoid overpromised outcomes."),
            ("48-hour check-in", "Prompt", "Write a warm follow-up after [treatment] with one care reminder, a realistic timeline, and a soft invitation to book the next step."),
            ("FAQ carousel", "Prompt", "Turn the question '[client question]' into a 5-slide Instagram carousel for a med spa. Tone: calm, premium, clear, medically responsible."),
        ]),
        card_page(doc, 3, "Retention Prompts", "Turn results into relationships.", [
            ("Maintenance reminder", "Prompt", "Write a maintenance reminder for a client who had [treatment] [timeframe] ago. Keep it warm, not pushy, and invite them to book a consultation or next visit."),
            ("Review request", "Prompt", "Write a privacy-safe Google review request after a positive client experience. Do not mention treatment details. Make it short, grateful, and easy to act on."),
        ]),
        page(brand("Full Bundle", "Next Step") + '<p class="kicker" style="margin-top:1in">Want the full system?</p><h2>Turn the prompts into a complete client journey.</h2><p class="lead">The full Med Spa Growth Bundle includes the AI Playbook, 90-day calendar, email templates, brand kit, pre-consult system, and implementation guide.</p>', 4, doc, "cta-page"),
    ]
    pages_count = write_html("lm-med-spa.html", doc, pages)
    files.append({"file": "lm-med-spa.html", "title": doc, "pages": pages_count, "prompts": 5, "templates": 5, "internal": False, "internal_reasons": []})

    update_inventory(files)
    print(f"Built {len(files)} Med Spa files in {OUT}")
    print(f"Total pages: {sum(f['pages'] for f in files)}")


if __name__ == "__main__":
    main()
