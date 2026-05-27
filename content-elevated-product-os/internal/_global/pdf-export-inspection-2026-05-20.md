# PDF Export Inspection - 2026-05-20

## Current Verdict

The current `customer-pdf-export` folder is not upload-ready.

This is good to know now, before Payhip upload. Chrome can create the PDF files, but the print layout is not stable enough yet.

## What Was Inspected

Output folder:

`content-elevated-product-os/exports/customer-pdf-export/`

Automated reports:

- `VALIDATION_REPORT.md`
- `PDF_LAYOUT_RISK_REPORT.md`

Visual contact sheets:

- `content-elevated-product-os/exports/customer-pdf-export/_visual-audit/phase-1/`

## Findings

Validation:

- 44 PDFs exported.
- 7 export items are still missing.
- Missing products/files are currently concentrated in Med Spas, Nutritionists, and Wedding Photographers.

Layout risk:

- 52 files need attention.
- The most common issue is exported PDFs having more pages than the source manifest expected.
- Extra pages usually mean print overflow: content is continuing beyond the designed page frame, creating blank pages or orphaned text fragments.

Visual proof:

- `dentists/01-ai-playbook-dentists.pdf` visibly confirms the issue.
- The contact sheet shows orphaned page fragments and mostly blank overflow pages.
- This matches the user's Mac Preview concern about elements overlapping/colliding.

## Root Cause

The source HTML uses premium fixed-page layouts with:

- fixed Letter-sized page frames,
- absolute-positioned footers,
- decorative borders,
- long cards/text blocks,
- dense source content.

When a block is too tall for the designed page, Chrome creates extra PDF pages or splits content in awkward places. That causes the exported PDF to look different than the browser preview.

## New Production Rule

Do not run or upload a full batch before a demo export is visually approved.

Use this sequence:

1. Demo export 1-2 PDFs per product.
2. Validate the demo.
3. Run layout-risk audit.
4. Generate visual contact sheets.
5. Fix layout/source issues.
6. Run full export only after the demo is clean.

## Demo Export Command

```zsh
cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"
python3 scripts/export_customer_pdfs_outside_codex.py --batch phase-1 --files-per-product 2 --output content-elevated-product-os/exports/customer-pdf-demo --slow --timeout 45
python3 scripts/validate_customer_pdf_export.py --batch phase-1 --output content-elevated-product-os/exports/customer-pdf-demo
python3 scripts/audit_pdf_layout_risk.py --batch phase-1 --output content-elevated-product-os/exports/customer-pdf-demo
/Users/tomasz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/create_pdf_contact_sheets.py --root content-elevated-product-os/exports/customer-pdf-demo --batch phase-1 --max-pages 35
```

## Fix Direction

The next work should focus on print hardening, not visual redesign:

- Keep approved covers/design direction.
- Make interior pages print-safe.
- Reserve reliable footer/border spacing.
- Split dense cards into more intentional pages.
- Reduce long single-card text blocks.
- Accept a few extra intentional pages when needed, but no accidental blank pages or orphan fragments.

## Upload Rule

Nothing from `customer-pdf-export` should be uploaded to Payhip until:

- validation errors are zero,
- layout-risk items are reviewed,
- contact sheets are visually clean,
- a small demo export passes first.

## Demo Export Follow-Up - 2026-05-20

The first demo export completed successfully at:

`content-elevated-product-os/exports/customer-pdf-demo/`

Results:

- Products processed: 8
- Export errors: 0
- PDFs exported: 16
- Validation errors: 0
- Layout-risk items: 12 of 16 PDFs

Contact sheets were generated at:

`content-elevated-product-os/exports/customer-pdf-demo/_visual-audit/phase-1/`

Visual scan confirmed that the export pipeline now creates files reliably, but the source pages still produce overflow fragments in several PDFs. Examples:

- Accountants AI Playbook: orphaned fragment pages and nearly blank overflow pages.
- Dentists AI Playbook: orphaned lower fragments and an extra blank/partial page.
- Wedding Photographers AI Playbook: multiple orphaned top/bottom fragments.
- Hair Stylist Month 1 Calendar: long content runs across many overflow pages.

The root print issue was traced to source pages using `min-height:11in`. That lets Chrome expand the page when content is too tall, creating accidental extra PDF pages. A mechanical hardening pass changed `min-height:11in` to `height:11in` across the print source directories so designed pages behave as fixed Letter pages. This needs a fresh external Terminal demo export before upload; Codex cannot reliably create Chrome PDFs inside the sandbox.

Next proof pass:

1. Re-run a demo export from normal Terminal.
2. Re-run validation and layout-risk audit.
3. Generate contact sheets.
4. Inspect whether any content is clipped after fixed-page hardening.
5. If clipping appears, split/reduce those specific dense source pages instead of uploading.
