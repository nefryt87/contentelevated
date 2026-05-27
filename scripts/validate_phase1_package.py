#!/usr/bin/env python3
"""Validate the Phase 1 Payhip source package."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
PACKAGE_ROOT = ROOT / "content-elevated-product-os/exports/phase-1-payhip-source-package"
REPORT_PATH = ROOT / "content-elevated-product-os/internal/_global/phase-1-package-validation.md"

PHASE_1_SLUGS = [
    "hair-stylists",
    "med-spas",
    "dentists",
    "nutritionists",
    "hvac-contractors",
    "accountants-and-cpas",
    "wedding-photographers",
    "etsy-sellers",
]

RISK_PATTERNS = {
    "internal platform reference": re.compile(r"\b(Gumroad|Stan Store|Etsy marketplace|ConvertKit admin|launch pricing)\b", re.I),
    "placeholder text": re.compile(r"\b(lorem ipsum|TODO|TBD|yourdomain\.com|you@example\.com)\b", re.I),
    "print-ready wording": re.compile(r"print[- ]ready|print ready html", re.I),
    "broken glyph": re.compile(r"\ufffd|â|Â|�"),
    "aggressive guarantee": re.compile(r"\b(guaranteed results|instant results|double your revenue|triple your revenue|skyrocket|explode your sales)\b", re.I),
}


def main() -> None:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    products = {item["slug"]: item for item in inventory}
    lines = [
        "# Phase 1 Package Validation",
        "",
        f"Validated: {date.today().isoformat()}",
        "",
    ]

    overall_issues = 0
    for slug in PHASE_1_SLUGS:
        product = products[slug]
        html_dir = PACKAGE_ROOT / slug / "html"
        sheet_dir = PACKAGE_ROOT / slug / "spreadsheets"
        expected_html = [f["file"] for f in product["files"] if not f.get("internal")]
        actual_html = sorted(p.name for p in html_dir.glob("*.html")) if html_dir.exists() else []
        actual_sheets = sorted(p.name for p in sheet_dir.glob("*.xlsx")) if sheet_dir.exists() else []
        expected_sheets = sorted(product.get("spreadsheet_files", []))

        issues: list[str] = []
        missing = sorted(set(expected_html) - set(actual_html))
        extra = sorted(set(actual_html) - set(expected_html))
        if missing:
            issues.append(f"Missing HTML: {', '.join(missing)}")
        if extra:
            issues.append(f"Unexpected HTML: {', '.join(extra)}")
        if expected_sheets != actual_sheets:
            issues.append(f"Spreadsheet mismatch. Expected {expected_sheets or 'none'}, found {actual_sheets or 'none'}")

        text_issues: list[str] = []
        for html_name in actual_html:
            text = (html_dir / html_name).read_text(encoding="utf-8", errors="replace")
            for label, pattern in RISK_PATTERNS.items():
                if pattern.search(text):
                    text_issues.append(f"{html_name}: {label}")

        issues.extend(text_issues)
        overall_issues += len(issues)

        lines += [
            f"## {product['product_name']}",
            "",
            f"- Expected HTML files: {len(expected_html)}",
            f"- Packaged HTML files: {len(actual_html)}",
            f"- Expected spreadsheets: {len(expected_sheets)}",
            f"- Packaged spreadsheets: {len(actual_sheets)}",
            f"- Inventory page total: {product['total_customer_pages']}",
        ]
        if issues:
            lines += ["- Status: Needs review", "", "### Issues", ""]
            lines.extend(f"- {issue}" for issue in issues)
        else:
            lines += ["- Status: Clean package pass"]
        lines.append("")

    lines += [
        "## Summary",
        "",
        f"- Total issues found: {overall_issues}",
        "- PDF rendering is still a separate final-export step.",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT_PATH)


if __name__ == "__main__":
    main()
