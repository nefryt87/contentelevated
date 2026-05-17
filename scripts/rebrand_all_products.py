from __future__ import annotations

import html
import os
import re
import shutil
from pathlib import Path

from pypdf import PdfReader


SOURCE_ROOT = Path("/Users/tomasz/Documents/Content Elevated/Content Elevated Products")
WORKSPACE_ROOT = Path("/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for")
OUTPUT_ROOT = WORKSPACE_ROOT / "rebranded-products-full-rebrand"

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
    n = niche.lower()
    if "barber" in n:
        return THEMES["barber"]
    if "tattoo" in n:
        return THEMES["tattoo"]
    if any(word in n for word in ["aesthetic", "bridal", "hair", "lash", "makeup", "med spa", "nail", "stylist"]):
        return THEMES["beauty"]
    if any(word in n for word in ["attorney", "accountant", "cpa", "financial", "insurance", "mortgage", "broker"]):
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


def is_dark(theme: dict[str, str]) -> bool:
    return theme["paper"].startswith("#0")


def css(theme: dict[str, str]) -> str:
    dark = is_dark(theme)
    grid_opacity = ".11" if dark else ".18"
    page_bg = (
        f"linear-gradient(145deg,{theme['paper']},{theme['tint']} 70%,{theme['dark']})"
        if dark
        else f"linear-gradient(145deg,{theme['paper']},{theme['tint']} 72%,#ebe5dc)"
    )
    return f"""
@page {{ size: Letter; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #d6d6d3; color: {theme['ink']}; font-family: Inter, 'Helvetica Neue', Arial, sans-serif; }}
.book {{ width: 8.5in; margin: 0 auto; }}
.page {{ position: relative; width: 8.5in; min-height: 11in; overflow: hidden; page-break-after: always; padding: .58in; background: {page_bg}; }}
.page::before {{ content: ""; position: absolute; inset: 0; pointer-events: none; background:
  radial-gradient(circle at 86% 12%, color-mix(in srgb,{theme['accent']} 18%,transparent), transparent 2.35in),
  radial-gradient(circle at 10% 92%, color-mix(in srgb,{theme['accent2']} 14%,transparent), transparent 2.85in),
  linear-gradient(rgba(255,255,255,{grid_opacity}) 1px, transparent 1px),
  linear-gradient(90deg, rgba(255,255,255,{grid_opacity}) 1px, transparent 1px);
  background-size: auto, auto, .42in .42in, .42in .42in;
  mask-image: linear-gradient(180deg, black, rgba(0,0,0,.2)); }}
.page::after {{ content: ""; position: absolute; left: .58in; right: .58in; bottom: .62in; height: 1px; background: linear-gradient(90deg,{theme['accent']},transparent); opacity: .38; }}
.brand {{ position: relative; z-index: 3; display: flex; align-items: flex-start; justify-content: space-between; gap: 28px; }}
.brand-name {{ font-size: 10px; font-weight: 900; letter-spacing: .28em; text-transform: uppercase; }}
.brand-sub {{ margin-top: 8px; color: {theme['muted']}; font-size: 8px; font-weight: 800; letter-spacing: .18em; text-transform: uppercase; }}
.document-pill {{ border: 1px solid color-mix(in srgb,{theme['accent']} 28%,transparent); border-radius: 999px; padding: 10px 13px; color: {theme['accent']}; font-size: 8px; font-weight: 900; letter-spacing: .18em; text-transform: uppercase; background: rgba(255,255,255,{'.04' if dark else '.38'}); }}
.kicker {{ position: relative; z-index: 3; margin: .72in 0 18px; color: {theme['accent']}; font-size: 9px; font-weight: 900; letter-spacing: .24em; text-transform: uppercase; }}
.kicker::before {{ content: ""; display: inline-block; width: 42px; height: 1px; margin-right: 14px; vertical-align: middle; background: {theme['accent']}; }}
h1 {{ position: relative; z-index: 3; margin: 0; max-width: 6.45in; font-family: Georgia, 'Times New Roman', serif; font-size: 55px; line-height: .95; font-weight: 400; letter-spacing: -.045em; }}
h1 em {{ color: {theme['accent']}; font-style: italic; }}
h2 {{ margin: 0 0 18px; font-family: Georgia, 'Times New Roman', serif; font-size: 33px; line-height: 1.02; font-weight: 400; letter-spacing: -.035em; }}
h3 {{ margin: 20px 0 9px; color: {theme['accent']}; font-size: 10px; line-height: 1.25; font-weight: 900; letter-spacing: .16em; text-transform: uppercase; }}
p {{ margin: 0 0 9px; color: {theme['muted']}; font-size: 10.4px; line-height: 1.45; }}
.lead {{ position: relative; z-index: 3; max-width: 5.35in; margin-top: .26in; font-size: 14px; line-height: 1.55; }}
.cover-system {{ position: absolute; z-index: 3; left: .58in; right: .58in; bottom: .95in; display: grid; grid-template-columns: 1.08fr .92fr; gap: 18px; }}
.cover-panel {{ border: 1px solid color-mix(in srgb,{theme['accent']} 20%,transparent); border-radius: 24px; padding: 23px; background: rgba(255,255,255,{'.045' if dark else '.55'}); box-shadow: 0 24px 70px rgba(0,0,0,{'.2' if dark else '.07'}); }}
.cover-panel.dark {{ background: linear-gradient(135deg,{theme['dark']},color-mix(in srgb,{theme['dark']} 76%,{theme['accent']})); color: #f8f3ed; }}
.cover-panel.dark p {{ color: rgba(248,243,237,.76); }}
.smallcaps {{ color: {theme['accent2']}; font-size: 8px; font-weight: 900; letter-spacing: .18em; text-transform: uppercase; }}
.metric-grid {{ display: grid; grid-template-columns: repeat(2,1fr); gap: 9px; }}
.metric {{ min-height: .74in; border: 1px solid rgba(255,255,255,.14); border-radius: 16px; padding: 12px; background: rgba(255,255,255,.05); }}
.metric b {{ display: block; font-family: Georgia, serif; color: #fff; font-size: 24px; font-weight: 400; }}
.metric span {{ display: block; margin-top: 5px; color: rgba(255,255,255,.62); font-size: 7.6px; font-weight: 900; letter-spacing: .14em; line-height: 1.35; text-transform: uppercase; }}
.intro-card {{ position: relative; z-index: 3; margin-top: .38in; border: 1px solid color-mix(in srgb,{theme['accent']} 18%,transparent); border-radius: 28px; padding: 28px; background: rgba(255,255,255,{'.05' if dark else '.58'}); box-shadow: 0 20px 60px rgba(0,0,0,{'.18' if dark else '.06'}); }}
.steps {{ display: grid; grid-template-columns: repeat(2,1fr); gap: 12px; margin-top: 22px; }}
.step {{ border: 1px solid color-mix(in srgb,{theme['accent']} 16%,transparent); border-radius: 18px; padding: 16px; background: rgba(255,255,255,{'.05' if dark else '.44'}); }}
.step b {{ display: block; margin-bottom: 9px; font-family: Georgia, serif; color: {theme['accent']}; font-size: 23px; font-weight: 400; }}
.content {{ position: relative; z-index: 3; margin-top: .38in; border: 1px solid color-mix(in srgb,{theme['accent']} 18%,transparent); border-radius: 26px; padding: 28px; background: rgba(255,255,255,{'.052' if dark else '.62'}); box-shadow: 0 22px 62px rgba(0,0,0,{'.18' if dark else '.065'}); }}
.section-label {{ margin: 20px 0 10px; padding-top: 15px; border-top: 1px solid color-mix(in srgb,{theme['accent']} 18%,transparent); color: {theme['accent']}; font-size: 9px; font-weight: 900; letter-spacing: .17em; text-transform: uppercase; }}
.template-line {{ border-left: 2px solid {theme['accent']}; padding: 7px 0 7px 12px; background: linear-gradient(90deg,color-mix(in srgb,{theme['accent']} 10%,transparent),transparent 76%); }}
.footer {{ position: absolute; z-index: 3; left: .58in; right: .58in; bottom: .3in; display: flex; justify-content: space-between; color: {theme['muted']}; font-size: 8px; font-weight: 850; letter-spacing: .13em; text-transform: uppercase; }}
.page-number {{ color: {theme['accent']}; font-family: Georgia, serif; }}
@media print {{ body {{ background: white; }} .book {{ margin: 0; }} }}
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
  <div class="brand"><div><div class="brand-name">CONTENT ELEVATED</div><div class="brand-sub">{html.escape(niche)} Growth Bundle</div></div><div class="document-pill">{html.escape(theme['label'])}</div></div>
  <p class="kicker">{html.escape(descriptor)}</p>
  <h1>{title_html}</h1>
  <p class="lead">A redesigned, print-ready business system built for clarity, premium presentation, and real-world implementation.</p>
  <div class="cover-system">
    <div class="cover-panel dark"><p class="smallcaps">Designed for {html.escape(theme['tone'])}</p><p>Use this file as an operating asset: customize the language, move the strongest ideas into your weekly workflow, and keep the system close to revenue moments.</p></div>
    <div class="cover-panel dark"><div class="metric-grid"><div class="metric"><b>01</b><span>Read the system</span></div><div class="metric"><b>02</b><span>Customize quickly</span></div><div class="metric"><b>03</b><span>Use weekly</span></div><div class="metric"><b>CE</b><span>Premium file</span></div></div></div>
  </div>
  <div class="footer"><span>{html.escape(niche)}</span><span class="page-number">01</span></div>
</section>""",
        f"""<section class="page">
  <div class="brand"><div><div class="brand-name">CONTENT ELEVATED</div><div class="brand-sub">{html.escape(niche)} Growth Bundle</div></div><div class="document-pill">Start Here</div></div>
  <p class="kicker">Implementation Notes</p>
  <h2>Turn this file into action.</h2>
  <div class="intro-card">
    <p>This redesigned version keeps the original content intact while improving hierarchy, pacing, readability, and perceived value. Work through it section by section and adapt the brackets, client language, and offers to the business.</p>
    <div class="steps"><div class="step"><b>01</b><p>Skim once for strategy and context.</p></div><div class="step"><b>02</b><p>Highlight the pages that match the next business priority.</p></div><div class="step"><b>03</b><p>Customize prompts, scripts, and templates before using them live.</p></div><div class="step"><b>04</b><p>Save working versions into the client or content workflow.</p></div></div>
  </div>
  <div class="footer"><span>{html.escape(title)}</span><span class="page-number">02</span></div>
</section>""",
    ]
    for index, chunk in enumerate(chunks, start=3):
        pages.append(
            f"""<section class="page">
  <div class="brand"><div><div class="brand-name">CONTENT ELEVATED</div><div class="brand-sub">{html.escape(niche)} Growth Bundle</div></div><div class="document-pill">{html.escape(descriptor)}</div></div>
  <div class="content">{render_blocks(chunk)}</div>
  <div class="footer"><span>{html.escape(title)}</span><span class="page-number">{index:02d}</span></div>
</section>"""
        )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f"<title>{html.escape(title)}</title><style>{css(theme)}</style></head><body><main class=\"book\">"
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
    title = display_title(path, niche)
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
