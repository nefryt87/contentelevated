#!/usr/bin/env python3
"""Export product copy handoff JSON files into upload-friendly CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GLOBAL = ROOT / "content-elevated-product-os/internal/_global"

EXPORTS = [
    (
        GLOBAL / "phase-1-website-copy-handoff.json",
        ROOT / "content-elevated-product-os/exports/phase-1-listing-copy-export.csv",
    ),
    (
        GLOBAL / "next-batch-website-copy-handoff.json",
        ROOT / "content-elevated-product-os/exports/next-batch-listing-copy-export.csv",
    ),
    (
        GLOBAL / "standard-queue-website-copy-handoff.json",
        ROOT / "content-elevated-product-os/exports/standard-queue-listing-copy-export.csv",
    ),
]


def join_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def main() -> None:
    total = 0
    for source, out in EXPORTS:
        records = json.loads(source.read_text(encoding="utf-8"))
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "internal_slug",
                    "website_title",
                    "website_slug",
                    "payhip_url",
                    "headline",
                    "subhead",
                    "summary",
                    "inventory_bullets",
                    "outcome_bullets",
                    "inside_bullets",
                    "product_details",
                ],
            )
            writer.writeheader()
            for record in records:
                writer.writerow(
                    {
                        "internal_slug": record.get("internal_slug", ""),
                        "website_title": record.get("website_title", ""),
                        "website_slug": record.get("website_slug", ""),
                        "payhip_url": record.get("payhip_url", ""),
                        "headline": record.get("h1", ""),
                        "subhead": record.get("subhead", ""),
                        "summary": record.get("summary", ""),
                        "inventory_bullets": join_list(record.get("inventory", [])),
                        "outcome_bullets": join_list(record.get("outcomes", [])),
                        "inside_bullets": join_list(record.get("inside", [])),
                        "product_details": join_list(record.get("details", [])),
                    }
                )
                total += 1
        print(out)
    print(f"Exported {total} listing-copy records")


if __name__ == "__main__":
    main()
