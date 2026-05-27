# PDF Final QA Command Center

Updated: 2026-05-26

## Current Decision

Do not upload Phase 1 or Phase 2 PDFs to Payhip until the current source patches are re-exported and contact-sheet reviewed.

The issue is not “PDF export failed.” The issue is that some pages were too dense for fixed Letter-size output, so the PDFs could pass automation while still showing overlap or clipping in Apple Preview.

Hair Stylists, Med Spas, and Videographers are now flagship-first products. Treat them as focused export/proof/upload lanes before trying to push the whole catalog.

## Root Cause

- Fixed HTML pages are exactly 8.5 x 11 inches.
- Dense pages with too many stacked cards can visually collide with borders/footers after PDF print.
- Etsy used `asset-card` blocks.
- HVAC used `data-card` blocks.
- The first splitter only handled `asset-card`, so HVAC escaped the protection.

## Source Guardrail

Active rule:

- No source page should contain more than 4 stacked `asset-card` or `data-card` blocks.
- If one card has unusually long copy, split even more aggressively.
- More pages is better than overlap, clipping, or lag.

Current source status:

- Phase 1 source package: 0 pages over the card limit.
- Phase 2 source package: 0 pages over the card limit.
- Standard queue source package: 0 pages over the card limit.
- HVAC was patched across the full bundle, not only the one failed Phone Scripts file.

## Known Risk Files

These must be checked by human eye before full launch:

- `phase-1/etsy-sellers/pdfs/01-ai-playbook-etsy-sellers.pdf`
- `phase-1/hvac-contractors/pdfs/01-ai-playbook-hvac-contractors.pdf`
- `phase-1/hvac-contractors/pdfs/02-90day-content-calendar-hvac-month-1.pdf`
- `phase-1/hvac-contractors/pdfs/02-90day-content-calendar-hvac-month-2.pdf`
- `phase-1/hvac-contractors/pdfs/02-90day-content-calendar-hvac-month-3.pdf`
- `phase-1/hvac-contractors/pdfs/03-email-templates-hvac.pdf`
- `phase-1/hvac-contractors/pdfs/04-brand-kit-hvac.pdf`
- `phase-1/hvac-contractors/pdfs/05-phone-scripts-hvac.pdf`
- `phase-1/hvac-contractors/pdfs/lm-hvac-contractors.pdf`

## Next Action

Run the flagship helpers from normal Terminal/Finder first:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_hair_stylist_flagship_export_outside_codex.command
```

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_med_spa_flagship_export_outside_codex.command
```

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_videographer_flagship_export_outside_codex.command
```

Then run the risk export helper from normal Terminal/Finder before broad Phase 1:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_phase1_risk_export_outside_codex.command
```

Then review:

`content-elevated-product-os/exports/customer-pdf-phase-1-risk-test-v1/_visual-audit/phase-1/`

The helper also creates a dashboard:

`content-elevated-product-os/exports/customer-pdf-phase-1-risk-test-v1/phase-1-visual-review-index.html`

Pass criteria:

- No clipped bottom text.
- No card overlaps.
- Footer and page number have breathing room.
- Long pages do not feel sluggish in Preview.
- Text remains readable at normal zoom.

## If Risk Test Passes

Run the full Phase 1 helper from normal Terminal/Finder:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_phase1_final_export_outside_codex.command
```

Then skim the generated visual review dashboard before Payhip upload.

## If Risk Test Fails

Do not full-export.

Fix the source first:

1. Identify the exact page and source HTML.
2. Split the crowded section again, usually to 2-3 cards per page.
3. Reduce heavy PDF effects if the file is laggy: large shadows, blur, big translucent gradients.
4. Re-run only the failed risk file.

## Phase 2 Rule

Phase 2 already exported once clean by automation, but contact-sheet review found bottom-edge crowding in several Brand Kit files. Re-export the patched source before upload.

Targeted Phase 2 Brand Kit export:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_phase2_brandkit_fix_outside_codex.command
```

## Upload Gate

Call a batch upload-ready only after:

- Source density guard passes.
- PDF export has 0 errors.
- Validation has 0 errors.
- Layout-risk audit has 0 attention files.
- Contact sheets have been human-reviewed for all known-risk PDFs.
- The generated visual review dashboard has been skimmed end-to-end.
- A few PDFs are opened directly in Apple Preview and feel responsive.
