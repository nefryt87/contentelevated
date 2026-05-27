#!/usr/bin/env python3
"""Fill known Phase 1 Payhip URLs into per-product trackers."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "content-elevated-product-os/internal"
PRODUCT_MASTER = ROOT / "content-elevated-product-os/data/product-master.csv"

KNOWN = {
    "med-spas": "https://payhip.com/b/uRbgW",
    "dentists": "https://payhip.com/b/RXUZc",
    "nutritionists": "https://payhip.com/b/xz0Tr",
    "hvac-contractors": "https://payhip.com/b/r9Jay",
    "accountants-and-cpas": "https://payhip.com/b/9zcAT",
    "wedding-photographers": "https://payhip.com/b/r5HSz",
    "etsy-sellers": "https://payhip.com/b/x7D4I",
}


def checkout(url: str) -> str:
    return f"https://payhip.com/buy?link={url.rstrip('/').split('/')[-1]}"


def update_tracker(slug: str, url: str) -> None:
    path = INTERNAL / slug / "payhip-url-and-price.md"
    if not path.exists():
        return
    title = path.read_text(encoding="utf-8").splitlines()[0]
    lines = [
        title,
        "",
        f"- Payhip product URL: {url}",
        f"- Checkout URL: {checkout(url)}",
        "- Current price: confirm in Payhip",
        "- Sale/launch price: confirm in Payhip",
        "- Cover image saved locally: no",
        "- Notes: URL pulled from current website product data. Price and cover still need confirmation from Payhip.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def update_master() -> None:
    rows: list[dict[str, str]] = []
    with PRODUCT_MASTER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            if row["slug"] in KNOWN:
                row["payhip_url"] = KNOWN[row["slug"]]
                row["notes"] = (row.get("notes", "").rstrip(".") + ". Payhip URL pulled from current website data; price and cover still need confirmation.").lstrip(". ")
            rows.append(row)
    with PRODUCT_MASTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    for slug, url in KNOWN.items():
        update_tracker(slug, url)
    update_master()
    print(f"Updated {len(KNOWN)} Phase 1 Payhip trackers")


if __name__ == "__main__":
    main()
