# Phase 1 Launch Upload Checklist

Last updated: 2026-05-20

Use this as the final sales-start checklist after running the external PDF exporter.

## 1. Export PDFs Outside Codex

Run:

```zsh
cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"
python3 scripts/export_customer_pdfs_outside_codex.py --batch phase-1 --slow
```

Or open:

`scripts/run_pdf_export_outside_codex.command`

Expected output:

`content-elevated-product-os/exports/customer-pdf-export/phase-1/`

## 2. Confirm Export Summary

Open:

`content-elevated-product-os/exports/customer-pdf-export/EXPORT_SUMMARY.md`

Pass condition:

- Products processed: 8
- Errors: 0
- Phase 1 PDFs exported for all products
- Hair Stylists and Etsy Sellers spreadsheets copied

Then run:

```zsh
python3 scripts/validate_customer_pdf_export.py --batch phase-1
```

Open:

`content-elevated-product-os/exports/customer-pdf-export/VALIDATION_REPORT.md`

## 3. Spot-Proof Before Payhip

Proof the first PDF and lead magnet for each product first, then spot-check calendars and template packs.

Check:

- Covers render properly.
- Page numbers and footer text have breathing room.
- No text is cropped or unreadable.
- Backgrounds, colors, and borders exported.
- No internal language appears.
- Spreadsheet files are included where expected.

## 4. Upload/Reupload In Payhip

Use:

`content-elevated-product-os/internal/_global/upload-execution-command-sheet.md`

Upload only:

- `pdfs/*.pdf`
- `spreadsheets/*.xlsx`

Do not upload:

- Source HTML
- `MANIFEST.md`
- Internal notes
- Listing CSVs
- Launch strategy docs
- Hair Stylists internal launch/reference files

## 5. Confirm Product Admin Details

Before marking a product complete:

- Confirm price.
- Confirm Payhip URL.
- Save cover image locally under `content-elevated-product-os/assets/product-covers/`.
- Save Payhip before/after screenshot under `content-elevated-product-os/assets/payhip-screenshots/`.

Phase 1 missing confirmations:

- Hair Stylists: Payhip URL, price, cover
- Med Spas: price, cover
- Dentists: price, cover
- Nutritionists: price, cover
- HVAC Contractors: price, cover
- Accountants & CPAs: price, cover
- Wedding Photographers: price, cover
- Etsy Sellers: price, cover

## 6. Website Update

Use:

- `content-elevated-product-os/internal/_global/phase-1-website-copy-handoff.json`
- `content-elevated-product-os/internal/_global/phase-1-website-copy-handoff.md`

Website update rules:

- Product CTAs should go to the matching Payhip URL.
- Product pages should describe secure checkout and instant delivery through Payhip.
- Do not publish Hair Stylists until its Payhip URL is confirmed.
- Keep inventory counts aligned with the upload files.

## 7. Mark Complete

Update after upload:

- `content-elevated-product-os/internal/_global/phase-1-payhip-action-board.md`
- `content-elevated-product-os/internal/_global/phase-1-payhip-action-board.csv`
- `content-elevated-product-os/data/product-master.csv`
- `content-elevated-product-os/data/product-master.json`

Then move to the next approved batch.
