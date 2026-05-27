# PDF Export + Payhip Upload SOP

Last updated: 2026-05-20

This is the operating procedure for turning approved HTML source packages into Payhip-ready customer files.

## Source Of Truth

Phase 1 source package:

- `content-elevated-product-os/exports/phase-1-payhip-source-package/`
- `content-elevated-product-os/exports/phase-1-payhip-source-package.zip`

Next batch source package:

- `content-elevated-product-os/exports/next-batch-source-package/`
- `content-elevated-product-os/exports/next-batch-source-package.zip`

Each product folder contains:

- `html/`: customer-facing files that need to be exported to PDF.
- `spreadsheets/`: spreadsheets to upload as-is, when present.
- `MANIFEST.md`: exact file list and expected page counts.

## Final PDF Export Requirement

Export each HTML file to PDF with:

- Background graphics enabled.
- Letter page size.
- No browser headers/footers.
- File name matching the HTML name, replacing `.html` with `.pdf`.

Example:

- `html/01-ai-playbook-hvac-contractors.html`
- becomes `01-ai-playbook-hvac-contractors.pdf`

## Current Automation Blocker

Automated PDF export was attempted inside Codex and blocked by the sandbox/browser environment:

- Direct Google Chrome headless did not produce PDFs; old headless exited with code 134.
- Chrome still attempted protected `~/Library/Application Support/Google/Chrome/Crashpad/...` paths even with temp profile, temp home, and crash-reporter flags.
- macOS `open -na "Google Chrome"` cannot be used here because Codex shell sandbox approval is unavailable.
- Swift/WebKit default SDK failed because `MacOSX26.2.sdk` expects Swift 6.2 while installed Swift is 6.1.2.
- Swift/WebKit with `MacOSX15.5.sdk` compiled further but still timed out due WebKit needing sandbox-blocked Apple services and protected Library/cache paths.
- `cupsfilter` has no HTML-to-PDF filter available.
- Bundled Python lacks `weasyprint`, `playwright`, `selenium`, `pyppeteer`, and `pdfkit`; `reportlab` would not preserve the HTML design.
- Bundled Node has Playwright core paths but not a usable browser binary for direct PDF export.
- Browser plugin can render and inspect the in-app browser, but the exposed controller does not include raw `page.pdf()`.

Do not repeat these attempts inside Codex. Do not treat this as a content failure. The source packages validate clean; the blocker is the rendering environment.

2026-05-20 retest after macOS permissions:

- Codex gained visibility into `~/Library`, but browser export still failed inside the active sandbox.
- Chrome headless still exited with code 134.
- Swift/WebKit still could not create required WebKit/cache folders and timed out.
- Use the external Terminal exporter unless Codex has been fully restarted and retested.

## Current Recommended Export Path

Run the external exporter from normal macOS Terminal, outside the Codex sandbox:

```zsh
cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"
python3 scripts/export_customer_pdfs_outside_codex.py --batch phase-1 --slow
```

For the clickable helper, open:

`scripts/run_pdf_export_outside_codex.command`

Full runbook:

`content-elevated-product-os/internal/_global/pdf-export-terminal-runbook.md`

## Recommended Export Paths

### Option A: Browser Print

1. Open each HTML file in Chrome.
2. Print.
3. Destination: Save as PDF.
4. More settings:
   - Paper size: Letter
   - Margins: None or default if the design already controls the page
   - Background graphics: enabled
   - Headers and footers: disabled
5. Save PDF beside the source package or into a final upload folder.

### Option B: Playwright Environment

Use this when Playwright browsers are installed:

1. Install Playwright browser binaries.
2. Export every HTML file with `printBackground: true` and `preferCSSPageSize: true`.
3. Validate PDF page counts against each product `MANIFEST.md`.

### Option C: Design/Export Tool

Use a dedicated HTML-to-PDF or browser-rendered export tool that respects CSS page size and print backgrounds.

## Payhip Upload Order

For each product:

1. Open that product’s `MANIFEST.md`.
2. Export all files listed under `Convert These HTML Files To PDF`.
3. Include spreadsheets listed under `Upload These Spreadsheets Too`.
4. Visually proof the generated PDFs.
5. Confirm final price and product URL in Payhip.
6. Replace the old/basic Payhip files with the newly exported PDFs and spreadsheets.
7. Confirm checkout and instant delivery still work.
8. Update:
   - `internal/[slug]/payhip-url-and-price.md`
   - `internal/_global/phase-1-payhip-action-board.csv`
   - `data/product-master.csv`

## Visual Proof Checklist

Check every exported PDF for:

- No cropped text.
- No text too close to border lines.
- No visible production language.
- No broken glyphs.
- Page numbers/footers do not collide with borders.
- Tables are readable.
- Cover page feels niche-specific.
- Spreadsheet files are included when expected.

## Phase 1 Manual Gaps

- Hair Stylists needs confirmed Payhip product URL.
- Every Phase 1 product still needs confirmed price.
- Every Phase 1 product still needs cover saved locally.
- Website product data should be enriched after Payhip URLs/files are confirmed.
