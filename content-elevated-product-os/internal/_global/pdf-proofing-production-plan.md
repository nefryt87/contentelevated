# PDF Proofing + Production Plan

Last updated: 2026-05-20

## Current Finding

The first Phase 1 PDF export is not upload-ready.

Validation:

- `VALIDATION_REPORT.md`: 44 PDFs exported, 7 missing items at the last check.
- `PDF_LAYOUT_RISK_REPORT.md`: 52 files flagged for missing exports or page-count/layout risk.

Key issue:

- Chrome is generating PDFs, but many exported PDFs have more pages than the source HTML/manifest expected.
- This usually means the fixed HTML page design is overflowing during print export.
- User visually confirmed overlap/collision in Mac Preview on `01-ai-playbook-dentists.pdf`.

## Decision

Do not continue full-catalog export blindly.

Use a demo export workflow:

1. Export only 1-2 PDFs per product.
2. Run validation.
3. Run layout-risk audit.
4. Visually proof the demo PDFs in Preview.
5. Fix source/layout.
6. Only then export the full batch.

## Demo Export Command

```zsh
cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"
python3 scripts/export_customer_pdfs_outside_codex.py --batch phase-1 --files-per-product 2 --output content-elevated-product-os/exports/customer-pdf-demo --slow --timeout 45
python3 scripts/validate_customer_pdf_export.py --batch phase-1 --output content-elevated-product-os/exports/customer-pdf-demo
python3 scripts/audit_pdf_layout_risk.py --batch phase-1 --output content-elevated-product-os/exports/customer-pdf-demo
```

One-product demo:

```zsh
python3 scripts/export_customer_pdfs_outside_codex.py --batch phase-1 --only dentists --files-per-product 2 --output content-elevated-product-os/exports/customer-pdf-demo --slow --timeout 45
python3 scripts/audit_pdf_layout_risk.py --batch phase-1 --output content-elevated-product-os/exports/customer-pdf-demo
```

## Root Cause To Fix

The current print HTML often uses:

- fixed-size page cards
- absolute footers
- decorative border overlays
- long text blocks/cards
- source content collapsed into long paragraphs

When a content block exceeds the designed page height, Chrome creates extra PDF pages or lets content collide with page chrome.

## Fix Strategy

For production HTML:

- Avoid absolute footers on content-heavy pages, or reserve guaranteed bottom padding.
- Avoid long cards that can run into footers.
- Split long text blocks into smaller cards/pages.
- For dense playbooks/calendars, allow more pages intentionally instead of forcing too much into one designed page.
- Keep cover pages fixed and cinematic.
- Make interior pages more print-document robust: smaller type, tighter but readable line-height, safer vertical rhythm, and no content under borders/footers.

## Upload Rule

Only upload files after:

- validation errors are zero,
- layout-risk report is acceptable,
- at least one human visual proof pass is complete in Mac Preview.
