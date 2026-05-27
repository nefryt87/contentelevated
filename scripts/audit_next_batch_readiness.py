#!/usr/bin/env python3
"""Audit the recommended next batch for copy/design readiness risks."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
SOURCE_ROOT = ROOT / "rebranded-products-sample-direction"
OUT = ROOT / "content-elevated-product-os/internal/_global/next-batch-readiness-audit.md"

NEXT_BATCH = [
    "barbers",
    "dog-walkers-and-pet-sitters",
    "personal-trainers",
    "personal-chefs",
    "nannies-and-childcare-professionals",
    "florists",
    "event-planners",
    "videographers",
    "public-speakers",
    "personal-stylists",
    "life-and-business-coaches",
]

RISK_PATTERNS = {
    "broken glyph": re.compile(r"\ufffd|â|Â|�"),
    "production wording": re.compile(r"print[- ]ready|print ready html", re.I),
    "placeholder/internal": re.compile(r"\b(lorem ipsum|TODO|TBD|yourdomain\.com|you@example\.com|admin setup)\b", re.I),
    "old marketplace/admin": re.compile(r"\b(Gumroad|Stan Store|ConvertKit admin|launch pricing|sales channel)\b", re.I),
    "aggressive guarantee": re.compile(r"\b(guaranteed results|instant results|double your revenue|triple your revenue|skyrocket|explode your sales)\b", re.I),
    "uk spelling": re.compile(r"\b(optimise|optimised|personalised|customise|enquiry|enquiries)\b", re.I),
}


def main() -> None:
    products = {item["slug"]: item for item in json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))}
    lines = [
        "# Next Batch Readiness Audit",
        "",
        f"Audited: {date.today().isoformat()}",
        "",
        "Recommended next batch: approved or directionally approved products that should be easier to move into launch shape after Phase 1.",
        "",
    ]

    total_issues = 0
    for slug in NEXT_BATCH:
        product = products[slug]
        source_dir = SOURCE_ROOT / slug
        issues: list[str] = []
        html_files = [f for f in product["files"] if not f.get("internal")]
        for file_info in html_files:
            path = source_dir / file_info["file"]
            if not path.exists():
                issues.append(f"{file_info['file']}: missing source file")
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in RISK_PATTERNS.items():
                if pattern.search(text):
                    issues.append(f"{file_info['file']}: {label}")

        total_issues += len(issues)
        lines += [
            f"## {product['product_name']}",
            "",
            f"- Customer-facing files: {product['customer_pdf_count']}",
            f"- Customer-facing pages: {product['total_customer_pages']}",
            f"- Spreadsheets: {product['spreadsheet_count']}",
            f"- Status: {'Needs cleanup' if issues else 'Clean automated pass'}",
        ]
        if issues:
            lines += ["", "### Issues", ""]
            lines.extend(f"- {issue}" for issue in issues)
        lines.append("")

    lines += [
        "## Summary",
        "",
        f"- Total automated issues found: {total_issues}",
        "- These checks do not replace human visual proofing or niche-specific copy review.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
