#!/usr/bin/env python3
"""Shared standard-queue product helpers."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "content-elevated-product-os/data/product-master.csv"

PHASE_1 = {
    "hair-stylists",
    "med-spas",
    "dentists",
    "nutritionists",
    "hvac-contractors",
    "accountants-and-cpas",
    "wedding-photographers",
    "etsy-sellers",
}

NEXT_BATCH = {
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
}


def load_master() -> dict[str, dict[str, str]]:
    with MASTER.open(newline="", encoding="utf-8") as f:
        return {row["slug"]: row for row in csv.DictReader(f)}


def standard_queue_slugs() -> list[str]:
    rows = load_master()
    return [
        slug for slug in rows
        if slug not in PHASE_1 and slug not in NEXT_BATCH
    ]
