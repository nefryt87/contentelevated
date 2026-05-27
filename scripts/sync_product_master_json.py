#!/usr/bin/env python3
"""Regenerate product-master.json from product-master.csv."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "content-elevated-product-os/data/product-master.csv"
JSON_PATH = ROOT / "content-elevated-product-os/data/product-master.json"


def main() -> None:
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    JSON_PATH.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"Synced {len(rows)} products to {JSON_PATH}")


if __name__ == "__main__":
    main()
