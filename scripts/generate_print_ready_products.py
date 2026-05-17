from __future__ import annotations

import html
import os
import re
from pathlib import Path

from pypdf import PdfReader


SOURCE_ROOT = Path("/Users/tomasz/Documents/Content Elevated/Content Elevated Products")
OUTPUT_ROOT = Path(
    "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/print-ready-pdfs"
)


SECTION_RE = re.compile(
    r"^(SECTION|TEMPLATE|PROMPT|CHAPTER|WEEK|MONTH|DAY|BONUS|WHY|HOW TO|INTRODUCTION|"
    r"CONCLUSION|SUBJECT|EMAIL|SCRIPT|CHECKLIST|PALETTE|TYPOGRAPHY|CANVA|REFERRAL|"
    r"ADVISORY|TAX|CLIENT|NEW CLIENT|YEAR-END|IRS|PHONE|SOCIAL|CONTENT|BRAND|INTAKE|"
    r"BOOKING|SYSTEM|PARTNERSHIP|OFFER|FOLLOW-UP|RETENTION|REACTIVATION)\b",
    re.I,
)


THEMES = {
    "beauty": {
        "bg": "#f8f1ef",
        "paper": "#fffaf6",
        "ink": "#191313",
        "muted": "#736464",
        "accent": "#b77a7d",
        "accent2": "#d8b6a9",
        "dark": "#21191a",
        "label": "Client experience system",
    },
    "professional": {
        "bg": "#f2f0e8",
        "paper": "#fbfaf5",
        "ink": "#121417",
        "muted": "#61666d",
        "accent": "#536f78",
        "accent2": "#8aa5a2",
        "dark": "#1d252c",
        "label": "Trust operating system",
    },
    "trades": {
        "bg": "#eef3f7",
        "paper": "#fbfdff",
        "ink": "#07111d",
        "muted": "#526171",
        "accent": "#348bb9",
        "accent2": "#f08245",
        "dark": "#0e1b28",
        "label": "Field growth system",
    },
    "creative": {
        "bg": "#f4eee8",
        "paper": "#fffaf3",
        "ink": "#171211",
        "muted": "#6f625d",
        "accent": "#8f6a7a",
        "accent2": "#c5a66f",
        "dark": "#191414",
        "label": "Creative demand system",
    },
    "wellness": {
        "bg": "#f0f4ed",
        "paper": "#fbfcf7",
        "ink": "#141a17",
        "muted": "#5f6c61",
        "accent": "#6e8a77",
        "accent2": "#b7c7bb",
        "dark": "#17211b",
        "label": "Care growth system",
    },
    "commerce": {
        "bg": "#eff3f4",
        "paper": "#fbfcfc",
        "ink": "#111416",
        "muted": "#5d6468",
        "accent": "#3f8f98",
        "accent2": "#9cb7ff",
        "dark": "#11171c",
        "label": "Shop growth system",
    },
    "hospitality": {
        "bg": "#f4efe6",
        "paper": "#fffaf1",
        "ink": "#171410",
        "muted": "#6b6256",
        "accent": "#9a7654",
        "accent2": "#c6a987",
        "dark": "#211a14",
        "label": "Guest experience system",
    },
}


def slugify(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def theme_for(niche: str) -> dict[str, str]:
    n = niche.lower()
    if any(word in n for word in ["aesthetic", "barber", "bridal", "hair", "lash", "makeup", "med spa", "nail", "stylist", "tattoo"]):
        return THEMES["beauty"]
    if any(word in n for word in ["attorney", "accountant", "cpa", "financial", "insurance", "mortgage"]):
        return THEMES["professional"]
    if any(word in n for word in ["hvac", "electrician", "plumber", "car wash"]):
        return THEMES["trades"]
    if any(word in n for word in ["chiropractor", "dentist", "massage", "nutrition", "physical", "wellness"]):
        return THEMES["wellness"]
    if any(word in n for word in ["etsy", "e-commerce"]):
        return THEMES["commerce"]
    if any(word in n for word in ["chef", "nannies", "dog", "pet"]):
        return THEMES["hospitality"]
    return THEMES["creative"]


def css(theme: dict[str, str]) -> str:
    return f"""
@page {{ size: Letter; margin: 0; }}
:root {{
  --bg:{theme["bg"]}; --paper:{theme["paper"]}; --ink:{theme["ink"]}; --muted:{theme["muted"]};
  --accent:{theme["accent"]}; --accent2:{theme["accent2"]}; --dark:{theme["dark"]};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:#d8d8d5;color:var(--ink);font-family:Inter,Arial,sans-serif}}
.book{{width:8.5in;margin:0 auto}}
.page{{position:relative;width:8.5in;min-height:11in;page-break-after:always;padding:.62in;background:
  radial-gradient(circle at 84% 10%, color-mix(in srgb,var(--accent) 20%,transparent), transparent 2.45in),
  radial-gradient(circle at 10% 90%, color-mix(in srgb,var(--accent2) 22%,transparent), transparent 2.65in),
  linear-gradient(135deg,var(--paper),var(--bg) 67%,#e5e3dc);overflow:hidden}}
.page:before{{content:"";position:absolute;inset:0;background-image:
  linear-gradient(rgba(20,20,20,.042) 1px,transparent 1px),
  linear-gradient(90deg,rgba(20,20,20,.032) 1px,transparent 1px);background-size:.42in .42in;
  mask-image:linear-gradient(180deg,rgba(0,0,0,.58),rgba(0,0,0,.08));pointer-events:none}}
.page:after{{content:"";position:absolute;right:-.82in;top:.72in;width:2.8in;height:8.6in;border:1px solid color-mix(in srgb,var(--accent) 22%,transparent);border-radius:999px;transform:rotate(-12deg);pointer-events:none}}
.brand{{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:flex-start}}
.mark{{display:flex;gap:12px;align-items:center}}.seal{{width:42px;height:42px;border:1px solid color-mix(in srgb,var(--accent) 38%,var(--ink));border-radius:50%;display:grid;place-items:center;font-family:Georgia,serif;font-size:14px;background:rgba(255,255,255,.34)}}.word{{font-size:10px;font-weight:850;letter-spacing:.22em;text-transform:uppercase}}.word span{{display:block;margin-top:7px;color:var(--muted);font-size:8px;letter-spacing:.17em}}.pill{{border:1px solid rgba(20,20,20,.13);border-radius:999px;padding:10px 14px;background:rgba(255,255,255,.36);font-size:8px;font-weight:850;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}}
.kicker{{position:relative;z-index:2;margin:.76in 0 18px;display:flex;gap:12px;align-items:center;color:var(--accent);font-size:9px;font-weight:850;letter-spacing:.24em;text-transform:uppercase}}.kicker:before{{content:"";width:44px;height:1px;background:linear-gradient(90deg,var(--accent),var(--accent2))}}
h1{{position:relative;z-index:2;margin:0;max-width:6.28in;font-family:Georgia,'Times New Roman',serif;font-size:52px;line-height:.96;font-weight:400;letter-spacing:-.04em}}h1 em{{font-style:italic;color:var(--accent)}}h2{{position:relative;z-index:2;margin:0 0 15px;font-family:Georgia,'Times New Roman',serif;font-size:31px;line-height:1.02;font-weight:400;letter-spacing:-.035em}}h3{{margin:18px 0 8px;font-size:11px;line-height:1.2;font-weight:850;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}}p{{margin:0 0 8px;color:var(--muted);font-size:10.5px;line-height:1.42}}.lead{{position:relative;z-index:2;max-width:5.55in;margin:.24in 0 0;font-size:14px;line-height:1.52}}
.cover-grid{{position:absolute;left:.62in;right:.62in;bottom:.8in;z-index:2;display:grid;grid-template-columns:1.2fr .8fr;gap:18px}}.panel{{border:1px solid rgba(20,20,20,.12);border-radius:22px;background:rgba(255,255,255,.56);box-shadow:0 24px 62px rgba(30,30,30,.08);padding:24px}}.dark{{background:linear-gradient(135deg,var(--dark),color-mix(in srgb,var(--dark) 82%,var(--accent)));color:#f8f4eb}}.dark p{{color:rgba(248,244,235,.76)}}.smallcaps{{font-size:8.5px;font-weight:850;letter-spacing:.18em;text-transform:uppercase;color:var(--accent2)}}
.stat-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:9px}}.stat{{border:1px solid rgba(255,255,255,.14);border-radius:15px;padding:13px;background:rgba(255,255,255,.045)}}.stat strong{{display:block;font-family:Georgia,serif;font-size:25px;font-weight:400;color:#f3efe7}}.stat span{{display:block;margin-top:6px;font-size:8px;font-weight:850;letter-spacing:.14em;line-height:1.35;text-transform:uppercase;color:rgba(246,243,235,.62)}}
.content{{position:relative;z-index:2;margin-top:.44in;border:1px solid rgba(20,20,20,.12);border-radius:24px;background:rgba(255,255,255,.62);padding:27px;box-shadow:0 18px 52px rgba(20,24,27,.07)}}.section-label{{margin:20px 0 10px;border-top:1px solid rgba(20,20,20,.12);padding-top:14px;color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.16em;text-transform:uppercase}}.template-line{{border-left:2px solid var(--accent);padding:7px 0 7px 12px;background:linear-gradient(90deg,color-mix(in srgb,var(--accent) 10%,transparent),transparent 74%)}}
.toc{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:.34in}}.toc-item{{border:1px solid rgba(20,20,20,.11);border-radius:18px;padding:17px;background:rgba(255,255,255,.44)}}.toc-item b{{display:block;margin-bottom:7px;font-family:Georgia,serif;font-size:20px;font-weight:400;color:var(--dark)}}.toc-item span{{color:var(--muted);font-size:9.5px;line-height:1.4}}.footer{{position:absolute;left:.62in;right:.62in;bottom:.3in;z-index:2;display:flex;justify-content:space-between;color:rgba(75,82,88,.7);font-size:8px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}}.page-number{{font-family:Georgia,serif;color:var(--accent)}}
@media print{{body{{background:white}}.book{{margin:0}}}}
"""


def pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def clean_lines(text: str) -> list[str]:
    return [" ".join(line.strip().split()) for line in text.splitlines() if line.strip()]


def paragraphize(lines: list[str]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    buf: list[str] = []
    for line in lines:
        is_head = len(line) < 100 and (
            line.isupper() or SECTION_RE.match(line) or re.match(r"^(Template|Prompt|Chapter)\s+\d+", line)
        )
        if is_head:
            if buf:
                out.append(("p", " ".join(buf)))
                buf = []
            out.append(("h", line))
        elif line.startswith(("✓", "•", "- ")):
            if buf:
                out.append(("p", " ".join(buf)))
                buf = []
            out.append(("bullet", line))
        else:
            if len(" ".join(buf + [line])) > 260:
                out.append(("p", " ".join(buf)))
                buf = [line]
            else:
                buf.append(line)
    if buf:
        out.append(("p", " ".join(buf)))
    return out


def chunks(blocks: list[tuple[str, str]], max_chars: int = 3000) -> list[list[tuple[str, str]]]:
    pages: list[list[tuple[str, str]]] = []
    cur: list[tuple[str, str]] = []
    count = 0
    for kind, text in blocks:
        cost = len(text) + 60
        if cur and count + cost > max_chars:
            pages.append(cur)
            cur = []
            count = 0
        cur.append((kind, text))
        count += cost
    if cur:
        pages.append(cur)
    return pages


def render_blocks(blocks: list[tuple[str, str]]) -> str:
    bits: list[str] = []
    for kind, text in blocks:
        escaped = html.escape(text)
        if kind == "h":
            bits.append(f'<h3>{escaped}</h3>' if len(text) < 48 else f'<div class="section-label">{escaped}</div>')
        elif kind == "bullet":
            bits.append(f'<p class="template-line">{escaped}</p>')
        else:
            cls = ' class="template-line"' if text.startswith(("SUBJECT", "Dear ", "Write a ", "[Note:", "Copy and paste")) else ""
            bits.append(f"<p{cls}>{escaped}</p>")
    return "\n".join(bits)


def display_title(path: Path, niche: str) -> str:
    stem = re.sub(r"^\d+_", "", path.stem)
    stem = stem.replace("90Day", "90 Day").replace("LM_", "Free ")
    stem = stem.replace("_", " ")
    niche_words = [w for w in re.split(r"[^A-Za-z0-9]+", niche) if w]
    suffixes = {
        " ".join(niche_words),
        " ".join(w.rstrip("s") for w in niche_words),
        niche.replace("&", "and"),
    }
    for suffix in sorted(suffixes, key=len, reverse=True):
        if suffix and stem.lower().endswith(" " + suffix.lower()):
            stem = stem[: -len(suffix)].strip()
            break
    stem = re.sub(r"\b(HMUA|CPA|CPAs)\b", lambda m: m.group(1).upper(), stem, flags=re.I)
    return " ".join(stem.split()).title().replace("Ai", "AI").replace("Cpa", "CPA")


def is_calendar(path: Path) -> bool:
    name = path.name.lower()
    return "90day" in name or "90_day" in name or "90-day" in name or "social_calendar" in name or "content_calendar" in name


def split_calendar_blocks(blocks: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    third = max(1, len(blocks) // 3)
    return [blocks[:third], blocks[third : third * 2], blocks[third * 2 :]]


def build_html(niche: str, title: str, descriptor: str, theme: dict[str, str], body_blocks: list[tuple[str, str]]) -> str:
    page_chunks = chunks(body_blocks, 2900)
    title_html = html.escape(title).replace("AI", "<em>AI</em>")
    pages = [
        f'''<section class="page cover"><div class="brand"><div class="mark"><div class="seal">CE</div><div class="word">{html.escape(niche)}<span>Complete Growth Bundle</span></div></div><div class="pill">{html.escape(theme["label"])}</div></div><p class="kicker">{html.escape(descriptor)}</p><h1>{title_html}</h1><p class="lead">A premium, ready-to-use business growth asset redesigned for clarity, conversion, and day-to-day action.</p><div class="cover-grid"><div class="panel dark"><p class="smallcaps">Built for the way this business actually works</p><p>Use this file to move faster: plan better content, send stronger client communication, create more trust, and turn the included prompts into real business action.</p></div><div class="panel dark"><div class="stat-grid"><div class="stat"><strong>AI</strong><span>assisted system</span></div><div class="stat"><strong>30</strong><span>day action rhythm</span></div><div class="stat"><strong>CE</strong><span>premium file</span></div><div class="stat"><strong>PDF</strong><span>print ready</span></div></div></div></div><div class="footer"><span>{html.escape(niche)} Growth Bundle</span><span class="page-number">01</span></div></section>''',
        f'''<section class="page"><div class="brand"><div class="mark"><div class="seal">CE</div><div class="word">{html.escape(niche)}<span>Complete Growth Bundle</span></div></div><div class="pill">Start here</div></div><p class="kicker">How to use this</p><h2>Turn the system into motion.</h2><p class="lead">Pick the section closest to the next revenue moment, customize the brackets, and save the finished version into your client workflow. This design is built to be printed, exported, or used as an internal operating document.</p><div class="toc"><div class="toc-item"><b>01</b><span>Read the strategy once so the system makes sense.</span></div><div class="toc-item"><b>02</b><span>Customize the language for your market, offer, and client type.</span></div><div class="toc-item"><b>03</b><span>Batch the prompts, templates, and scripts into your weekly workflow.</span></div><div class="toc-item"><b>04</b><span>Keep the pages you use most close to your daily operations.</span></div></div><div class="footer"><span>{html.escape(niche)} Growth Bundle</span><span class="page-number">02</span></div></section>''',
    ]
    for index, block_chunk in enumerate(page_chunks, start=3):
        pages.append(
            f'''<section class="page"><div class="brand"><div class="mark"><div class="seal">CE</div><div class="word">{html.escape(niche)}<span>{html.escape(title)}</span></div></div><div class="pill">Working pages</div></div><div class="content">{render_blocks(block_chunk)}</div><div class="footer"><span>{html.escape(title)}</span><span class="page-number">{index:02d}</span></div></section>'''
        )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{html.escape(title)}</title><style>{css(theme)}</style></head><body><main class=\"book\">"
        + "\n".join(pages)
        + "</main></body></html>"
    )


def write_doc(path: Path, niche: str, out_dir: Path, theme: dict[str, str], overwrite: bool = False) -> list[Path]:
    text = pdf_text(path)
    lines = [line for line in clean_lines(text) if line.upper() not in {niche.upper(), "CONTENT ELEVATED"}]
    blocks = paragraphize(lines)
    title = display_title(path, niche)
    descriptor = "Lead magnet edition" if path.name.startswith("LM_") else ("30-day content system" if is_calendar(path) else "Premium business system")
    written: list[Path] = []
    if is_calendar(path):
        for idx, part in enumerate(split_calendar_blocks(blocks), start=1):
            month_title = f"{title} · Month {idx}"
            out = out_dir / f"{slugify(path.stem)}-month-{idx}.html"
            if out.exists() and not overwrite:
                continue
            out.write_text(build_html(niche, month_title, descriptor, theme, part), encoding="utf-8")
            written.append(out)
    else:
        out = out_dir / f"{slugify(path.stem)}.html"
        if overwrite or not out.exists():
            out.write_text(build_html(niche, title, descriptor, theme, blocks), encoding="utf-8")
            written.append(out)
    return written


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    all_written: list[Path] = []
    overwrite = os.environ.get("CE_OVERWRITE") == "1"
    requested = {
        item.strip()
        for item in os.environ.get("CE_NICHES", "").split("|")
        if item.strip()
    }
    skipped = {
        item.strip()
        for item in os.environ.get("CE_SKIP_NICHES", "").split("|")
        if item.strip()
    }
    for niche_dir in sorted(SOURCE_ROOT.iterdir()):
        if not niche_dir.is_dir() or niche_dir.name.startswith("_") or niche_dir.name == "broker_toolkit":
            continue
        if requested and niche_dir.name not in requested:
            continue
        if niche_dir.name in skipped:
            continue
        pdfs = sorted(niche_dir.glob("*.pdf"))
        if not pdfs:
            continue
        niche = niche_dir.name
        out_dir = OUTPUT_ROOT / slugify(niche)
        out_dir.mkdir(parents=True, exist_ok=True)
        theme = theme_for(niche)
        for pdf in pdfs:
            all_written.extend(write_doc(pdf, niche, out_dir, theme, overwrite=overwrite))
    print(f"Created {len(all_written)} new print-ready HTML files.")
    for path in all_written[:250]:
        print(path)


if __name__ == "__main__":
    main()
