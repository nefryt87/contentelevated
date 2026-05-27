#!/usr/bin/env python3
"""Run a broad automated readiness audit across the redesigned catalog."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
SOURCE_ROOT = ROOT / "rebranded-products-sample-direction"
OUT = ROOT / "content-elevated-product-os/internal/_global/full-catalog-readiness-audit.md"

RISK_PATTERNS = {
    "broken glyph": re.compile(r"\ufffd|�|â|Â"),
    "production wording": re.compile(r"print[- ]ready|print ready html", re.I),
    "placeholder/internal": re.compile(r"\b(lorem ipsum|TODO|TBD|yourdomain\.com|you@example\.com|admin setup)\b", re.I),
    "old marketplace/admin": re.compile(r"\b(Gumroad|Stan Store|ConvertKit admin|launch pricing|sales channel)\b", re.I),
    "aggressive guarantee": re.compile(r"\b(guaranteed results|instant results|double your revenue|triple your revenue|skyrocket|explode your sales|guaranteed income)\b", re.I),
    "uk spelling": re.compile(r"\b(optimise|optimised|personalised|customise|enquiry|enquiries|organiser|organisers|organisation|specialising|speciality|favourite|honour)\b", re.I),
}


def main() -> None:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    lines = [
        "# Full Catalog Readiness Audit",
        "",
        f"Audited: {date.today().isoformat()}",
        "",
        "Automated scan across customer-facing files in `rebranded-products-sample-direction/`.",
        "",
    ]

    totals = defaultdict(int)
    products_with_issues = 0
    clean_products = 0

    for product in inventory:
        slug = product["slug"]
        source_dir = SOURCE_ROOT / slug
        issues: list[str] = []
        for file_info in product["files"]:
            if file_info.get("internal"):
                continue
            path = source_dir / file_info["file"]
            if not path.exists():
                issues.append(f"{file_info['file']}: missing source file")
                totals["missing source file"] += 1
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in RISK_PATTERNS.items():
                if pattern.search(text):
                    issues.append(f"{file_info['file']}: {label}")
                    totals[label] += 1

        if issues:
            products_with_issues += 1
            lines += [
                f"## {product['product_name']}",
                "",
                f"- Category: {product['category']}",
                f"- Files: {product['customer_pdf_count']}",
                f"- Pages: {product['total_customer_pages']}",
                "",
            ]
            lines.extend(f"- {issue}" for issue in issues)
            lines.append("")
        else:
            clean_products += 1

    lines += [
        "## Summary",
        "",
        f"- Products with no automated issues: {clean_products}",
        f"- Products needing cleanup: {products_with_issues}",
        "",
        "### Issue Totals",
        "",
    ]
    if totals:
        for label, count in sorted(totals.items()):
            lines.append(f"- {label}: {count}")
    else:
        lines.append("- No automated issues found.")

    lines += [
        "",
        "## Reminder",
        "",
        "This audit catches mechanical risks. It does not replace visual review, niche-fit review, proofreading, or legal/industry compliance review.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
