# PDF Export Terminal Runbook

Use this when Codex cannot export PDFs because macOS blocks browser access inside the sandbox.

## Best One-Click Option

Open this file from Finder:

`/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_pdf_export_outside_codex.command`

Choose:

- `1` for the Phase 1 launch batch
- `2` for the next approved batch
- `3` for the standard queue
- `4` for everything

The finished PDFs will be created here:

`/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/content-elevated-product-os/exports/customer-pdf-export/`

Each product folder will include:

- `pdfs/` with exported customer PDFs
- `spreadsheets/` when that product has spreadsheet files
- `MANIFEST.md` with file-level export notes

The whole export folder also includes:

- `EXPORT_SUMMARY.md`

## Terminal Option

From Terminal:

```zsh
cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"
python3 scripts/export_customer_pdfs_outside_codex.py --batch phase-1 --slow
```

Other batch options:

```zsh
python3 scripts/export_customer_pdfs_outside_codex.py --batch next --slow
python3 scripts/export_customer_pdfs_outside_codex.py --batch standard --slow
python3 scripts/export_customer_pdfs_outside_codex.py --batch all --slow
```

Export only specific products:

```zsh
python3 scripts/export_customer_pdfs_outside_codex.py --batch next --only barbers personal-trainers --slow
```

## Proofing Checklist

Before uploading to Payhip, spot-check each exported product:

- Cover page renders cleanly.
- Footer and page number have breathing room.
- No text is cropped.
- Tables are readable.
- Backgrounds and brand colors exported.
- No “print-ready HTML” or internal production language appears.
- Spreadsheets are included when expected.

## Validation After Export

After export, run:

```zsh
cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"
python3 scripts/validate_customer_pdf_export.py --batch phase-1
```

Other options:

```zsh
python3 scripts/validate_customer_pdf_export.py --batch next
python3 scripts/validate_customer_pdf_export.py --batch standard
python3 scripts/validate_customer_pdf_export.py --batch all
```

This creates:

`content-elevated-product-os/exports/customer-pdf-export/VALIDATION_REPORT.md`

Use the validation report before uploading anything to Payhip.

## Demo Export Workflow

Before exporting a full batch, run a small demo:

```zsh
cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"
python3 scripts/export_customer_pdfs_outside_codex.py --batch phase-1 --files-per-product 2 --output content-elevated-product-os/exports/customer-pdf-demo --slow --timeout 45
python3 scripts/validate_customer_pdf_export.py --batch phase-1 --output content-elevated-product-os/exports/customer-pdf-demo
python3 scripts/audit_pdf_layout_risk.py --batch phase-1 --output content-elevated-product-os/exports/customer-pdf-demo
```

For one product only:

```zsh
python3 scripts/export_customer_pdfs_outside_codex.py --batch phase-1 --only dentists --files-per-product 2 --output content-elevated-product-os/exports/customer-pdf-demo --slow --timeout 45
```

Use demo export before every new batch so layout issues show up before the full catalog export.

## Phase 1 Risk Export Workflow

Use this before another full Phase 1 export. It targets the exact files/products that exposed the systemic layout issue: Etsy Sellers AI Playbook and the HVAC bundle.

Open this file from Finder, or run it from Terminal:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_phase1_risk_export_outside_codex.command
```

It creates:

`content-elevated-product-os/exports/customer-pdf-phase-1-risk-test-v1/`

Then it runs validation, page-count risk audit, and contact-sheet creation. Review:

`content-elevated-product-os/exports/customer-pdf-phase-1-risk-test-v1/_visual-audit/phase-1/`

It also creates:

`content-elevated-product-os/exports/customer-pdf-phase-1-risk-test-v1/phase-1-visual-review-index.html`

If these sheets look clean, proceed to the full Phase 1 re-export.

Full Phase 1 final candidate helper:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_phase1_final_export_outside_codex.command
```

## Visual Contact Sheet Audit

After a demo or full export, generate contact sheets so each PDF can be scanned quickly without opening every file page-by-page:

```zsh
cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"
/Users/tomasz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/create_pdf_contact_sheets.py --root content-elevated-product-os/exports/customer-pdf-export --batch phase-1 --max-pages 35
```

For demo exports, change the root:

```zsh
/Users/tomasz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/create_pdf_contact_sheets.py --root content-elevated-product-os/exports/customer-pdf-demo --batch phase-1 --max-pages 35
```

Contact sheets are saved in:

`content-elevated-product-os/exports/customer-pdf-export/_visual-audit/`

Use these sheets to catch blank pages, orphaned content fragments, clipped footers, and text collisions quickly.

Optional review dashboard:

```zsh
python3 scripts/build_pdf_visual_review_index.py --root content-elevated-product-os/exports/customer-pdf-export --batch phase-1
```

## Layout Risk Audit

After any full export, run:

```zsh
python3 scripts/audit_pdf_layout_risk.py --batch phase-1
```

This compares expected HTML/source page counts against exported PDF page counts. Extra exported pages usually mean overflow or layout collision risk; fewer exported pages can mean clipping.

## Source Density Guard

Before export, the active source packages should have no fixed page with more than four stacked cards:

```zsh
python3 scripts/split_dense_pdf_cards.py --max-cards 4
```

This script splits overloaded `asset-card` and `data-card` pages and updates package manifests. It exists because automated PDF page-count checks can pass while Apple Preview still shows visual collisions.

Do not revert this by compressing long pages back into fewer pages. More pages is acceptable when it prevents overlap, clipping, and lag.

## Playwright Export Option

Playwright is installed locally and a browser-native exporter exists:

```zsh
node scripts/export_customer_pdfs_playwright.js --batch phase-1 --only hvac-contractors --html-pattern "*.html" --output content-elevated-product-os/exports/customer-pdf-playwright-test --timeout 120000
```

Important: run Playwright from normal Terminal, not from inside Codex. Inside Codex, Chromium fails with macOS sandbox/MachPort permission errors.

## Phase 2 Brand Kit Refresh Helper

After the Phase 1 risk/final flow is stable, refresh the patched Phase 2 Brand Kit PDFs:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_phase2_brandkit_fix_outside_codex.command
```

## Flagship Product Export Helpers

Use these before broad batch export. They are focused, faster, and easier to visually approve.

Hair Stylists:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_hair_stylist_flagship_export_outside_codex.command
```

Med Spas:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_med_spa_flagship_export_outside_codex.command
```

Med Spa expected output:

`content-elevated-product-os/exports/customer-pdf-med-spa-flagship-v1/`

Videographers:

```zsh
/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/scripts/run_videographer_flagship_export_outside_codex.command
```

Videographer expected output:

`content-elevated-product-os/exports/customer-pdf-videographer-flagship-v1/`

Review the generated visual dashboard/contact sheets before uploading anything to Payhip.

## 2026-05-20 Print Hardening Note

The source HTML pages were updated so `.page` uses exact Letter-page height instead of `min-height:11in`. This should prevent Chrome from generating accidental orphan-fragment pages.

Because exact-height pages can hide content if a page is too dense, every demo export still needs contact-sheet review. If a contact sheet shows clipped bottom content, do not revert the global hardening. Instead, fix that specific source page by splitting the dense content across another designed page, tightening copy, or reducing card spacing.

## Payhip Upload Rule

Upload only customer-facing PDFs and spreadsheets. Do not upload internal notes, manifests, source HTML files, or listing-copy files.
