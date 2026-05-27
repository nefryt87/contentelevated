from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "rebranded-products-sample-direction"
OS_ROOT = ROOT / "content-elevated-product-os"


CATEGORY_BY_SLUG = {
    "accountants-and-cpas": "Professional Services",
    "attorneys": "Professional Services",
    "broker-toolkit": "Professional Services",
    "financial-advisors": "Professional Services",
    "insurance-agents": "Professional Services",
    "mortgage-brokers": "Professional Services",
    "aestheticians": "Beauty",
    "bridal-hair-and-makeup-artists": "Beauty",
    "hair-stylists": "Beauty",
    "lash-technicians": "Beauty",
    "makeup-artists": "Beauty",
    "med-spas": "Beauty",
    "nail-technicians": "Beauty",
    "barbers": "Beauty",
    "car-wash-businesses": "Home Services",
    "electricians": "Home Services",
    "hvac-contractors": "Home Services",
    "plumbers": "Home Services",
    "chiropractors": "Health & Wellness",
    "dentists": "Health & Wellness",
    "massage-therapists": "Health & Wellness",
    "nutritionists": "Health & Wellness",
    "physical-therapists": "Health & Wellness",
    "event-planners": "Creatives & Events",
    "florists": "Creatives & Events",
    "interior-designers": "Creatives & Events",
    "party-planners": "Creatives & Events",
    "public-speakers": "Creatives & Events",
    "tattoo-artists": "Creatives & Events",
    "videographers": "Creatives & Events",
    "wedding-photographers": "Creatives & Events",
    "dog-walkers-and-pet-sitters": "Local Services",
    "etsy-sellers": "E-Commerce",
    "life-and-business-coaches": "Coaches & Educators",
    "nannies-and-childcare-professionals": "Local Services",
    "personal-chefs": "Hospitality",
    "personal-stylists": "Personal Services",
    "personal-trainers": "Health & Wellness",
}


def title_from_slug(slug: str) -> str:
    replacements = {
        "cpas": "CPAs",
        "hvac": "HVAC",
        "seo": "SEO",
        "hmua": "HMUA",
        "ai": "AI",
    }
    words = []
    for word in slug.replace("-", " ").split():
        words.append(replacements.get(word, word.capitalize()))
    return " ".join(words).replace(" And ", " & ")


def product_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for folder in sorted(path for path in OUTPUT_ROOT.iterdir() if path.is_dir()):
        html_files = sorted(folder.rglob("*.html"))
        sheets = sorted(folder.rglob("*.xlsx")) + sorted(folder.rglob("*.xls")) + sorted(folder.rglob("*.csv"))
        if not html_files and not sheets:
            continue
        product_name = title_from_slug(folder.name)
        rows.append(
            {
                "slug": folder.name,
                "product_name": f"{product_name} Growth Bundle",
                "niche": product_name,
                "category": CATEGORY_BY_SLUG.get(folder.name, "Needs Category"),
                "html_file_count": str(len(html_files)),
                "spreadsheet_count": str(len(sheets)),
                "index_path": str((folder / "index.html").relative_to(ROOT)) if (folder / "index.html").exists() else "",
                "folder_path": str(folder.relative_to(ROOT)),
                "website_status": "needs copy",
                "payhip_status": "needs copy",
                "editorial_status": "needs proofread",
                "marketing_priority": "standard",
                "payhip_url": "",
                "price": "",
                "notes": "",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = product_rows()
    (OS_ROOT / "data").mkdir(parents=True, exist_ok=True)
    write_csv(OS_ROOT / "data" / "product-master.csv", rows)
    (OS_ROOT / "data" / "product-master.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Created product OS database with {len(rows)} products.")
    print(OS_ROOT / "data" / "product-master.csv")


if __name__ == "__main__":
    main()
