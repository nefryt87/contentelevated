from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path("rebranded-products-sample-direction")
OS_ROOT = Path("content-elevated-product-os")
MASTER = OS_ROOT / "data" / "product-master.csv"
OUT_CSV = OS_ROOT / "data" / "bundle-inventory.csv"
OUT_JSON = OS_ROOT / "data" / "bundle-inventory.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def title_for(path: Path, text: str) -> str:
    match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return path.stem.replace("-", " ").title()


def count_pages(text: str) -> int:
    return len(re.findall(r"<section\s+class=\"[^\"]*\bpage\b", text, re.I))


def count_prompts(text: str) -> int:
    nums = [int(n) for n in re.findall(r"Prompt\s*#\s*(\d+)", text, re.I)]
    if nums:
        return max(nums)
    explicit = re.findall(r"(\d+)\s+(?:copy-?paste\s+|ai\s+)?prompts?\b", text, re.I)
    return max([int(n) for n in explicit], default=0)


def count_templates(text: str) -> int:
    # Conservative count for email/script/template files. Avoid overstating.
    h3_templates = len(re.findall(r"<h3>.*?(?:Template|Email|Script|Reminder|Follow-Up|Request|Response).*?</h3>", text, re.I | re.S))
    body_blocks = len(re.findall(r"\bBODY\b", text))
    numbered_templates = len(re.findall(r"Template\s*#?\s*\d+", text, re.I))
    return max(h3_templates, body_blocks, numbered_templates)


def is_internal(path: Path, text: str, slug: str) -> tuple[bool, list[str]]:
    lower = text.lower()
    reasons: list[str] = []
    if any(t in path.name for t in ["launch-kit", "master-reference"]):
        reasons.append("filename suggests internal launch/reference file")
    if any(t in path.name for t in ["sample", "concept", "redesign"]):
        reasons.append("filename suggests review/sample file")
    checks = {
        "gumroad": "mentions Gumroad",
        "stan store": "mentions Stan Store",
        "consulting upsell": "mentions consulting upsell",
        "launch price": "mentions launch pricing",
        "what's still to build": "mentions unfinished/internal build notes",
        "what still to build": "mentions unfinished/internal build notes",
        "sales channels": "mentions sales channels",
        "listing copy": "mentions listing copy",
        "convertkit": "mentions ConvertKit/admin email setup",
    }
    for needle, reason in checks.items():
        if needle in lower:
            reasons.append(reason)
    if slug != "etsy-sellers" and "etsy" in lower and any(x in lower for x in ["gumroad", "listing", "marketplace", "sales channel", "launch price"]):
        reasons.append("mentions Etsy as marketplace/listing channel")
    return bool(reasons), sorted(set(reasons))


def main() -> None:
    products = list(csv.DictReader(MASTER.open(newline="", encoding="utf-8")))
    inventory = []
    for product in products:
        slug = product["slug"]
        folder = Path(product["folder_path"])
        files = []
        customer_pages = 0
        customer_prompts = 0
        customer_templates = 0
        internal_count = 0

        for html in sorted(folder.glob("*.html")):
            text = read_text(html)
            internal, reasons = is_internal(html, text, slug)
            pages = count_pages(text)
            title = title_for(html, text)
            prompts = count_prompts(text) if re.search(r"prompt|playbook|lead magnet", title, re.I) else 0
            templates = count_templates(text)
            if internal:
                internal_count += 1
            else:
                customer_pages += pages
                customer_prompts += prompts
                customer_templates += templates
            files.append(
                {
                    "file": html.name,
                    "title": title,
                    "pages": pages,
                    "prompts": prompts,
                    "templates": templates,
                    "internal": internal,
                    "internal_reasons": reasons,
                }
            )

        sheets = sorted((folder / "spreadsheets").glob("*")) if (folder / "spreadsheets").exists() else []
        row = {
            "slug": slug,
            "product_name": product["product_name"],
            "category": product["category"],
            "customer_pdf_count": sum(1 for f in files if not f["internal"]),
            "internal_file_count": internal_count,
            "spreadsheet_count": len(sheets),
            "total_customer_pages": customer_pages,
            "prompt_count": customer_prompts,
            "template_count_estimate": customer_templates,
            "spreadsheet_files": [s.name for s in sheets],
            "files": files,
        }
        inventory.append(row)

        internal_dir = OS_ROOT / "internal" / slug
        internal_dir.mkdir(parents=True, exist_ok=True)
        lines = [
            f"# {product['product_name']} Bundle Inventory",
            "",
            f"- Customer-facing PDFs/HTML files: {row['customer_pdf_count']}",
            f"- Internal/review files: {row['internal_file_count']}",
            f"- Spreadsheets: {row['spreadsheet_count']}",
            f"- Total customer-facing pages: {row['total_customer_pages']}",
            f"- Prompt count detected: {row['prompt_count'] or 'none detected'}",
            f"- Template count estimate: {row['template_count_estimate'] or 'none detected'}",
            "",
            "## Customer-Facing Files",
            "",
        ]
        for f in files:
            if not f["internal"]:
                bits = [f"{f['pages']} pages"]
                if f["prompts"]:
                    bits.append(f"{f['prompts']} prompts")
                if f["templates"]:
                    bits.append(f"{f['templates']} templates")
                lines.append(f"- `{f['title']}` (`{f['file']}`) — {', '.join(bits)}")
        if sheets:
            lines += ["", "## Spreadsheets", ""]
            for sheet in sheets:
                lines.append(f"- `{sheet.name}`")
        internal_files = [f for f in files if f["internal"]]
        if internal_files:
            lines += ["", "## Internal / Review Before Upload", ""]
            for f in internal_files:
                lines.append(f"- `{f['title']}` (`{f['file']}`) — {'; '.join(f['internal_reasons'])}")
        (internal_dir / "bundle-inventory.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    flat_fields = [
        "slug",
        "product_name",
        "category",
        "customer_pdf_count",
        "internal_file_count",
        "spreadsheet_count",
        "total_customer_pages",
        "prompt_count",
        "template_count_estimate",
        "spreadsheet_files",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=flat_fields)
        writer.writeheader()
        for row in inventory:
            flat = {k: row[k] for k in flat_fields}
            flat["spreadsheet_files"] = "; ".join(row["spreadsheet_files"])
            writer.writerow(flat)
    OUT_JSON.write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_JSON}")
    print(f"Updated {len(inventory)} bundle inventory files.")


if __name__ == "__main__":
    main()
