#!/usr/bin/env python3
"""Build the executive launch command center for Content Elevated."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "content-elevated-product-os/data/product-master.csv"
INVENTORY = ROOT / "content-elevated-product-os/data/bundle-inventory.json"
OUT = ROOT / "content-elevated-product-os/internal/_global/launch-command-center.md"

PHASE_1 = [
    "hair-stylists",
    "med-spas",
    "dentists",
    "nutritionists",
    "hvac-contractors",
    "accountants-and-cpas",
    "wedding-photographers",
    "etsy-sellers",
]

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


def load_master() -> dict[str, dict[str, str]]:
    with MASTER.open(newline="", encoding="utf-8") as f:
        return {row["slug"]: row for row in csv.DictReader(f)}


def load_inventory() -> dict[str, dict[str, object]]:
    return {row["slug"]: row for row in json.loads(INVENTORY.read_text(encoding="utf-8"))}


def batch_for(slug: str) -> str:
    if slug in PHASE_1:
        return "Phase 1"
    if slug in NEXT_BATCH:
        return "Next approved batch"
    return "Standard queue"


def main() -> None:
    master = load_master()
    inventory = load_inventory()
    all_slugs = list(master)
    missing_urls = [slug for slug, row in master.items() if not row.get("payhip_url")]
    total_pages = sum(int(inventory[slug]["total_customer_pages"]) for slug in all_slugs)
    total_files = sum(int(inventory[slug]["customer_pdf_count"]) for slug in all_slugs)
    total_sheets = sum(int(inventory[slug]["spreadsheet_count"]) for slug in all_slugs)

    lines = [
        "# Content Elevated Launch Command Center",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "This is the highest-level operating board. Use it first when resuming work so we do not burn time or credits rediscovering the project.",
        "",
        "## North Star",
        "",
        "Get redesigned bundles into Payhip and connected to `contentelevatedhq.com` as quickly as possible, while keeping enough quality control to avoid uploading messy or off-brand files.",
        "",
        "## Current Reality",
        "",
        f"- Total bundle products tracked: {len(all_slugs)}",
        f"- Customer-facing HTML/PDF source files tracked: {total_files}",
        f"- Customer-facing pages tracked: {total_pages}",
        f"- Spreadsheets tracked: {total_sheets}",
        f"- Products with Payhip URLs recorded: {len(all_slugs) - len(missing_urls)} / {len(all_slugs)}",
        f"- Products missing Payhip URLs: {len(missing_urls)}",
        "- Automated catalog scan: clean across all buyer-facing files.",
        "- Main blocker: final PDF export/proofing, because local browser PDF export is blocked in this environment.",
        "",
        "## Sales-First Priority Order",
        "",
        "1. **Launch Phase 1**: export final PDFs, proof them, upload to Payhip, connect/update website listings.",
        "2. **Launch Next Approved Batch**: repeat the exact same upload path for approved products.",
        "3. **Launch Standard Queue**: products are packaged and mechanically clean, but some need URL/cover confirmation and later visual proofing.",
        "4. **Only then expand into standalone products**: content calendar, brand kit, prompt library, client templates, etc.",
        "",
        "## Do Not Spend Credits On Yet",
        "",
        "- Redesigning approved bundles unless the user spots a real issue.",
        "- Re-reading every source PDF or every HTML file without a specific question.",
        "- Deep research/proofreading all products before the first sales-ready upload batch exists.",
        "- Standalone product buildout before bundles are live with the upgraded files.",
        "- More design concepts for categories already approved.",
        "",
        "## Credit-Efficient Operating Rules",
        "",
        "- Use the generated inventory, handoff JSON, and action boards before opening individual product files.",
        "- Batch work by launch group: Phase 1, Next Approved Batch, Standard Queue.",
        "- Run automated scans after edits, not before every small thought.",
        "- Treat HTML packages as source of truth until PDF export works.",
        "- When visual QA is needed, review 1 representative file first, then spot-check the rest by exception.",
        "- Keep approvals parked in `user-approval-parking-lot.md` instead of stopping the workstream.",
        "",
        "## Active Workstreams",
        "",
        "| Workstream | Status | Next Action | Source |",
        "|---|---|---|---|",
        "| Phase 1 upload | Ready as HTML source, blocked on PDF export/proof | Export PDFs outside blocked local environment, proof, upload to Payhip | `exports/phase-1-payhip-source-package/` |",
        "| Next approved batch | Packaged and clean | Export/proof after Phase 1 | `exports/next-batch-source-package/` |",
        "| Standard queue | Packaged and clean | Confirm missing URLs/covers, then export/proof | `exports/standard-queue-source-package/` |",
        "| Website copy | Handoffs generated | Use JSON/CSV when updating storefront data | `exports/*listing-copy-export.csv` |",
        "| Standalone products | Planned only | Start after bundles are uploaded | `internal/{slug}/standalone-products.md` |",
        "",
        "## Missing Payhip URL Confirmations",
        "",
        "| Product | Batch | Note |",
        "|---|---|---|",
    ]

    for slug in missing_urls:
        row = master[slug]
        note = "Confirm directly in Payhip before website linking."
        if slug == "attorneys":
            note = "Website data suggests an Attorney URL exists; confirm before updating tracker."
        lines.append(f"| {row['product_name']} | {batch_for(slug)} | {note} |")

    lines += [
        "",
        "## Resume Checklist",
        "",
        "When starting a new session, do this in order:",
        "",
        "1. Open this command center.",
        "2. Open `work-session-checkpoint.md` only if more detail is needed.",
        "3. Check the latest relevant package audit.",
        "4. Work on the highest-priority active blocker.",
        "5. Rebuild affected boards/packages only after changes.",
        "6. Sync to `/Users/tomasz/Documents/Codex/Content-Elevated` before ending.",
        "",
        "## Key Files",
        "",
        "- Resume point: `internal/_global/work-session-checkpoint.md`",
        "- Project queue: `internal/_global/next-phase-work-board.md`",
        "- PDF/export SOP: `internal/_global/pdf-export-and-payhip-upload-sop.md`",
        "- Phase 1 action board: `internal/_global/phase-1-payhip-action-board.md`",
        "- Next batch action board: `internal/_global/next-batch-payhip-action-board.md`",
        "- Standard queue action board: `internal/_global/standard-queue-action-board.md`",
        "- Catalog coverage: `internal/_global/catalog-operations-coverage.md`",
        "",
    ]

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
