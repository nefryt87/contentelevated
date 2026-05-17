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
  <p class="lead">A premium, niche-specific product file rebuilt from the real source content. Same direction as the approved sample index, expanded for the complete bundle.</p>
  <div class="metrics">
    <div class="metric"><b>01</b><span>Real bundle<br/>source content</span></div>
    <div class="metric"><b>02</b><span>Designed for<br/>{html.escape(theme["tag"])}</span></div>
    <div class="metric"><b>03</b><span>Print-ready<br/>review file</span></div>
  </div>
  <div class="footer"><span>{html.escape(niche)} product file</span><span>01</span></div>
</section>""",
        f"""<section class="page work direction-page">
  <div class="brand"><div>Content Elevated</div><div></div></div>
  <div class="section-head">
    <div><p class="eyebrow">Implementation Notes</p><h2>Turn this file into action.</h2></div>
    <p class="intro">This version keeps the original product content intact while matching the premium sample-document direction for this niche.</p>
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
    <p class="intro">Working pages rebuilt in the same visual system as the approved sample direction.</p>
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
<style>body{margin:0;background:#08090b;color:#f4f6f8;font-family:Inter,Arial,sans-serif;padding:48px}main{max-width:1180px;margin:auto}h1{font-size:48px;letter-spacing:-.05em}section{border:1px solid rgba(255,255,255,.12);border-radius:22px;padding:24px;margin:18px 0;background:rgba(255,255,255,.035)}h2{margin:0 0 12px}a{color:#9fdfff;text-decoration:none}li{margin:7px 0;color:#8190a2}</style></head><body><main><h1>Content Elevated Rebranded Products</h1><p>Print-ready HTML rebuilds plus spreadsheet files preserved for review.</p>"""
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
    print(f"Created {len(outputs)} print-ready HTML files.")
    print(f"Copied {len(spreadsheets)} spreadsheets.")
    print(OUTPUT_ROOT / "index.html")


if __name__ == "__main__":
    main()
