#!/usr/bin/env python3
"""Build an HTML review dashboard for generated PDF contact sheets."""

from __future__ import annotations

import argparse
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPORT_ROOT = ROOT / "content-elevated-product-os" / "exports" / "customer-pdf-export"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a PDF visual review index.")
    parser.add_argument("--root", type=Path, default=DEFAULT_EXPORT_ROOT)
    parser.add_argument("--batch", default="phase-1")
    parser.add_argument("--title", default="Content Elevated PDF Visual Review")
    return parser.parse_args()


def label_from_sheet(sheet: Path) -> tuple[str, str]:
    product = sheet.parent.name
    name = sheet.stem.replace("-contact-sheet", "").replace("-", " ").title()
    return product.replace("-", " ").title(), name


def main() -> None:
    args = parse_args()
    root = args.root.expanduser().resolve()
    audit_root = root / "_visual-audit" / args.batch
    sheets = sorted(audit_root.rglob("*-contact-sheet.png"))
    if not sheets:
        raise SystemExit(f"No contact sheets found at {audit_root}")

    cards = []
    for sheet in sheets:
        product, name = label_from_sheet(sheet)
        rel = sheet.relative_to(root)
        cards.append(
            f"""
            <article class="card">
              <a href="{html.escape(str(rel))}">
                <img src="{html.escape(str(rel))}" alt="{html.escape(product)} - {html.escape(name)}">
                <span class="product">{html.escape(product)}</span>
                <b>{html.escape(name)}</b>
              </a>
            </article>
            """
        )

    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(args.title)}</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg:#07090d;
      --panel:#10141b;
      --line:rgba(255,255,255,.1);
      --text:#f5f7fb;
      --muted:#9aa5b4;
      --accent:#78d7ff;
    }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0;
      background:
        radial-gradient(circle at 20% 0%, rgba(120,215,255,.16), transparent 34rem),
        radial-gradient(circle at 80% 12%, rgba(131,107,255,.12), transparent 30rem),
        var(--bg);
      color:var(--text);
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    }}
    header {{
      padding:48px clamp(18px,4vw,56px) 26px;
      border-bottom:1px solid var(--line);
    }}
    p, h1 {{ margin:0; }}
    .eyebrow {{
      color:var(--accent);
      font-size:12px;
      font-weight:800;
      letter-spacing:.18em;
      text-transform:uppercase;
    }}
    h1 {{
      margin-top:12px;
      font-size:clamp(34px,5vw,76px);
      letter-spacing:-.04em;
      line-height:.95;
    }}
    .summary {{
      margin-top:16px;
      max-width:760px;
      color:var(--muted);
      font-size:16px;
      line-height:1.6;
    }}
    main {{
      padding:34px clamp(18px,4vw,56px) 64px;
      display:grid;
      grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
      gap:18px;
    }}
    .card {{
      overflow:hidden;
      border:1px solid var(--line);
      border-radius:18px;
      background:linear-gradient(180deg, rgba(255,255,255,.055), rgba(255,255,255,.025));
      box-shadow:0 24px 90px rgba(0,0,0,.22);
    }}
    .card a {{
      display:block;
      min-height:100%;
      color:inherit;
      text-decoration:none;
      padding:12px 12px 16px;
    }}
    img {{
      display:block;
      width:100%;
      aspect-ratio:4/3;
      object-fit:cover;
      object-position:top center;
      border-radius:12px;
      background:#fff;
    }}
    .product {{
      display:block;
      margin:14px 4px 4px;
      color:var(--accent);
      font-size:11px;
      font-weight:800;
      letter-spacing:.14em;
      text-transform:uppercase;
    }}
    b {{
      display:block;
      margin:0 4px;
      font-size:16px;
      line-height:1.25;
    }}
  </style>
</head>
<body>
  <header>
    <p class="eyebrow">{html.escape(args.batch)} visual audit</p>
    <h1>{html.escape(args.title)}</h1>
    <p class="summary">{len(sheets)} contact sheets found. Open each card and scan for clipped bottom text, overlapping cards, crowded footers, blank fragments, and laggy heavy pages before upload.</p>
  </header>
  <main>
    {''.join(cards)}
  </main>
</body>
</html>
"""
    output = root / f"{args.batch}-visual-review-index.html"
    output.write_text(page, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
