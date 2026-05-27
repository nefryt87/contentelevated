# Phase 1 Final Launch Gate Report

Updated: 2026-05-21

## CEO Decision

Phase 1 is paused for a controlled risk re-export before Payhip upload.

Nutritionists Brand Kit was fixed, re-exported, visually contact-sheet checked, and restored into `customer-pdf-phase-1-final-v2`. After that, human review found two broader layout failures:

- `etsy-sellers/pdfs/01-ai-playbook-etsy-sellers.pdf`: visual breakdown starting around page 16.
- `hvac-contractors/pdfs/05-phone-scripts-hvac.pdf`: page 04/05 crowding plus laggy PDF behavior.

Root cause: overloaded fixed-height pages. Etsy used stacked `asset-card` pages; HVAC used stacked `data-card` pages, so the first source splitter missed the HVAC design system.

The operational priority is still sales speed, but the current final-v2 PDFs are not upload-ready until the patched source is re-exported and visually checked.

Immediate gate:

1. Run `scripts/run_phase1_risk_export_outside_codex.command` from normal Terminal/Finder.
2. Review the generated contact sheets for Etsy AI Playbook and all HVAC files.
3. If the risk test is clean, run a full Phase 1 re-export from the patched source package.
4. Validate, layout-audit, generate contact sheets, and human-skim high-risk files before upload.
5. Replace Payhip bundle files only after the full Phase 1 final export passes the launch gate.

## Final Export

- Final export root: `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2`
- Upload files: `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/phase-1`
- Final review hub: `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/phase-1-final-review-index.html`
- Contact sheets: `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/_visual-audit/phase-1`

## Automated Checks

- Previous final-v2 PDFs checked: 65
- Previous validation errors: 0
- Previous layout-risk files needing attention: 0
- Previous contact sheets generated: 65
- Human review issues found: Nutritionists Brand Kit page 04 overlap, Etsy AI Playbook late-page breakdown, HVAC Phone Scripts page 04/05 breakdown and laggy behavior
- Product folders present: 8
- Manifests present: 8
- Current source density check: Phase 1 source package has 0 HTML files with more than 4 stacked `asset-card`/`data-card` blocks per fixed page.

## Product Upload Counts

| Product | PDFs | Spreadsheets | Status |
|---|---:|---:|---|
| Accountants & CPAs | 8 | 0 | Ready |
| Dentists | 8 | 0 | Ready |
| Etsy Sellers | 8 | 1 | Hold: risk re-export required |
| Hair Stylists | 9 | 2 | Ready |
| HVAC Contractors | 8 | 0 | Hold: risk re-export required |
| Med Spas | 8 | 0 | Ready |
| Nutritionists | 8 | 0 | Ready after fixed Brand Kit replacement |
| Wedding Photographers | 8 | 0 | Ready |

## Text/Placeholder Scan

Customer-facing export/source scan found no active launch blockers such as:

- `Print-ready HTML`
- `TODO`
- `FIXME`
- `lorem`
- `undefined`
- fake sample-only labels

The remaining bracketed text instances are intentional buyer-editable placeholders inside templates and prompts, such as `[Practice Name]`, `[booking link]`, `[service]`, or `[Shop Name]`.

## Lessons From Phase 1

- Never run a full PDF export without a small demo export first.
- Always validate PDFs after export.
- Always run the layout-risk audit after export.
- Always generate contact sheets and skim them before upload.
- Automated page-count/layout-risk checks do not catch all visual overlap. Human contact-sheet review is still required before upload.
- Keep `height:11in` for fixed print pages; avoid reverting to `min-height:11in`.
- Watch for corrupted/binary HTML sources if a product behaves strangely.
- Keep old failed/demo exports archived, not mixed with upload-ready files.

## Nutritionists Brand Kit Fix

Corrected source files:

- `content-elevated-product-os/exports/phase-1-payhip-source-package/nutritionists/html/04-brand-kit-nutritionists.html`
- `rebranded-products-sample-direction/nutritionists/04-brand-kit-nutritionists.html`
- duplicate working copies in `rebranded-products-full-rebrand`, `rebranded-products`, and `print-ready-pdfs`

Fix applied:

- Split the Brand Kit from 7 pages to 9 pages.
- Split overloaded page 04 palette content into two pages.
- Split overloaded Canva/template content into two pages.
- Removed/reduced heavy export effects: backdrop blur, large overlay gradients, and card shadows.
- Tightened print card styling while preserving readability.

Status:

- Fixed export completed at `content-elevated-product-os/exports/customer-pdf-phase-1-nutritionists-fix-v1/`.
- Validation errors: 0.
- Layout-risk files needing attention: 0.
- Fixed contact sheet for `04-brand-kit-nutritionists.pdf` looked clean.
- Corrected PDF/contact sheet were copied back into `customer-pdf-phase-1-final-v2`.

## Phase 1 Density Fix

Corrected source files:

- Etsy Sellers source pages with overloaded `asset-card` stacks were split into safer pages.
- Wedding Photographers source pages with overloaded `asset-card` stacks were split into safer pages.
- HVAC Contractors source pages with overloaded `data-card` stacks were split into safer pages.
- `scripts/split_dense_pdf_cards.py` now handles both `asset-card` and `data-card` blocks.

Current safeguards:

- Phase 1 and Phase 2 active source packages currently show 0 files with more than 4 stacked cards on one page.
- Manifest page counts were updated to match actual source page counts.
- New targeted risk helper: `scripts/run_phase1_risk_export_outside_codex.command`.

## Active Clean Folders

- Approved final PDFs: `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2`
- Phase 1 source package: `content-elevated-product-os/exports/phase-1-payhip-source-package`
- Next batch source package: `content-elevated-product-os/exports/next-batch-source-package`
- Standard queue source package: `content-elevated-product-os/exports/standard-queue-source-package`
- Archived old runs: `content-elevated-product-os/exports/_archive-old-runs-2026-05-21`

## Next Batch Rule

Next batch should be exported as a demo first, preferably known-risk files or first 1-2 files per product. Do not jump straight into a full final upload until the demo validates cleanly and contact sheets look right.
