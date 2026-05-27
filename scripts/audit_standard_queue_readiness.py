#!/usr/bin/env python3
"""Audit standard-queue products for source package and buyer-facing text risks."""

from __future__ import annotations

import json
import re
from datetime import date

from standard_queue import ROOT, standard_queue_slugs


INVENTORY_PATH = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
SOURCE_ROOT = ROOT / "rebranded-products-sample-direction"
PACKAGE_ROOT = ROOT / "content-elevated-product-os/exports/standard-queue-source-package"
OUT = ROOT / "content-elevated-product-os/internal/_global/standard-queue-readiness-audit.md"

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
        "# Standard Queue Readiness Audit",
        "",
        f"Audited: {date.today().isoformat()}",
        "",
        "This audit checks the remaining standard-queue products for missing packaged sources and common buyer-facing text risks.",
        "",
    ]

    total_issues = 0
    for slug in standard_queue_slugs():
        product = products[slug]
        source_dir = SOURCE_ROOT / slug
        package_dir = PACKAGE_ROOT / slug
        issues: list[str] = []

        if not package_dir.exists():
            issues.append("source package folder missing")
        if not (package_dir / "MANIFEST.md").exists():
            issues.append("source package manifest missing")

        html_files = [f for f in product["files"] if not f.get("internal")]
        for file_info in html_files:
            path = source_dir / file_info["file"]
            packaged = package_dir / "html" / file_info["file"]
            if not path.exists():
                issues.append(f"{file_info['file']}: missing source file")
                continue
            if not packaged.exists():
                issues.append(f"{file_info['file']}: missing packaged copy")

            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in RISK_PATTERNS.items():
                if pattern.search(text):
                    issues.append(f"{file_info['file']}: {label}")

        for sheet in product.get("spreadsheet_files", []):
            if not (package_dir / "spreadsheets" / sheet).exists():
                issues.append(f"{sheet}: missing packaged spreadsheet")

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
        "- These checks do not replace final visual proofing or niche-specific copy polish.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
