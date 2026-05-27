# Memory For Future Codex Sessions

Use this file first after any chat compression or new session.

## Business

- Business name: Content Elevated.
- Website/domain: `contentelevatedhq.com`.
- Live store: `https://payhip.com/ContentElevated`.
- Payhip is the checkout and digital delivery platform.
- Website is the premium storefront.
- Products sell AI-powered growth bundles for service businesses and creators.

## Current Store State

- Products already exist on Payhip as bundles.
- Existing Payhip listings currently use the original/basic PDFs.
- Redesigned/proofread product files will need to be uploaded to replace the old Payhip files.
- Do not create duplicate bundle listings unless explicitly requested.

## Product Library State

- Rebranded HTML products live in `rebranded-products-sample-direction`.
- Product operating system lives in `content-elevated-product-os`.
- Internal product workspaces live in `content-elevated-product-os/internal/[product-slug]/`.
- Master product tracker is `content-elevated-product-os/data/product-master.csv`.
- Bundle inventory tracker is `content-elevated-product-os/data/bundle-inventory.csv`.
- Single-product expansion tracker is `content-elevated-product-os/data/single-product-roadmap.csv`.

## Future Product Strategy

- Current products are bundles.
- Future individual products should be created from high-value bundle components:
  - Content calendars
  - Brand kits
  - AI playbooks
  - Prompt libraries
  - Client templates
  - Retention/rebooking systems
  - Lead magnets
- Each individual product needs copy, cover image, price, Payhip URL, website page, and marketing assets.

## Cover Image Strategy

- Payhip already has cover photos/mockups uploaded.
- Save all cover images locally under `content-elevated-product-os/assets/product-covers/`.
- Save website/mockup versions under `content-elevated-product-os/assets/product-mockups/`.
- Save Payhip listing screenshots under `content-elevated-product-os/assets/payhip-screenshots/`.
- Use product slugs for filenames.

## Launch Priority

Launch/polish first:

1. Hair Stylists
2. Med Spas
3. Dentists
4. Nutritionists
5. HVAC Contractors
6. Accountants & CPAs
7. Wedding Photographers
8. Etsy Sellers

## Current Sprint

- Phase 1 launch batch is packaged as validated HTML source files and has a clean final PDF export.
- Phase 1 products: Hair Stylists, Med Spas, Dentists, Nutritionists, HVAC Contractors, Accountants & CPAs, Wedding Photographers, Etsy Sellers.
- Phase 1 source package: `content-elevated-product-os/exports/phase-1-payhip-source-package/`.
- Phase 1 listing copy CSV: `content-elevated-product-os/exports/phase-1-listing-copy-export.csv`.
- Final Phase 1 customer PDF export: `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/`.
- Phase 1 final-v2 status on 2026-05-21: automated checks passed; human review found a visual issue in `nutritionists/pdfs/04-brand-kit-nutritionists.pdf`; the Brand Kit was fixed, re-exported, visually contact-sheet checked, and restored into final-v2.
- Nutritionists Brand Kit issue/resolution: page 04 overlap and laggy PDF performance. Source HTML was fixed by splitting 7 pages into 9 pages and reducing heavy effects. Fixed export lives at `content-elevated-product-os/exports/customer-pdf-phase-1-nutritionists-fix-v1/`; final-v2 now contains the corrected PDF/contact sheet.
- Upload-ready Phase 1 files live at `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/phase-1/`.
- Phase 1 final review hub: `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/phase-1-final-review-index.html`.
- Phase 1 contact sheets live at `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/_visual-audit/phase-1/`.
- Phase 1 final launch gate report: `content-elevated-product-os/internal/_global/phase-1-final-launch-gate-report.md`.
- Phase 1 upload handoff: `content-elevated-product-os/internal/_global/phase-1-final-v2-upload-handoff.md`.
- Older PDF demo/failed/final-v1 export attempts were moved out of the active export lane into `content-elevated-product-os/exports/_archive-old-runs-2026-05-21/`.
- PDF export inspection on 2026-05-20 found the first Phase 1 export was not upload-ready: validation showed missing files, page-count audit showed widespread overflow risk, and dentist visual contact sheet confirmed orphaned fragments/blank extra pages. The fixed final-v2 export resolved this.
- Use demo export + contact-sheet proofing before any future full batch export.
- Detailed inspection note: `content-elevated-product-os/internal/_global/pdf-export-inspection-2026-05-20.md`.
- Reusable visual proofing script: `scripts/create_pdf_contact_sheets.py`.
- Next approved batch is packaged as validated HTML source files.
- Next approved batch products: Barbers, Dog Walkers & Pet Sitters, Personal Trainers, Personal Chefs, Nannies & Childcare Professionals, Florists, Event Planners, Videographers, Public Speakers, Personal Stylists, Life & Business Coaches.
- Next batch source package: `content-elevated-product-os/exports/next-batch-source-package/`.
- Next batch review hub: `content-elevated-product-os/exports/next-batch-source-package/review-index.html`.
- Next batch listing copy CSV: `content-elevated-product-os/exports/next-batch-listing-copy-export.csv`.
- Phase 2 full PDF export completed at `content-elevated-product-os/exports/customer-pdf-phase-2-full-v1/` with 84 PDFs, validation errors 0, page-count/layout-risk attention 0, and 84 contact sheets.
- Human contact-sheet review found no catastrophic overlap, but several Brand Kit files had bottom-edge crowding in long card stacks. Source HTML has been split into safer card groups. Current active rule: no Phase 1 or Phase 2 source page should have more than 4 stacked `asset-card`/`data-card` blocks.
- Phase 1 follow-up human review found two systemic failures after Nutritionists was fixed:
  - Etsy Sellers AI Playbook started visually breaking down around page 16.
  - HVAC Phone Scripts was laggy and page 04/05 visually broke down.
- Root cause: overloaded fixed-height page stacks. Etsy used `asset-card`; HVAC used `data-card`, so the first density splitter missed HVAC. `scripts/split_dense_pdf_cards.py` now handles both.
- Phase 1 source package has been patched for Etsy/Wedding/HVAC density; HVAC source package now has no page with more than 4 `asset-card`/`data-card` blocks, and phone scripts was split more aggressively to 9 pages.
- Standard queue source package was also hardened for the same density issue across Car Wash, Electricians, and Plumbers.
- Source-density audit script: `scripts/audit_html_source_density.py --batch all --max-cards 4`. Latest result: 0 pages needing attention across Phase 1, Phase 2, and standard queue.
- New targeted-export tooling: `scripts/export_customer_pdfs_outside_codex.py --html-pattern '04-brand-kit*.html'`; `scripts/validate_customer_pdf_export.py --pdf-pattern '04-brand-kit*.pdf'`; `scripts/audit_pdf_layout_risk.py --pdf-pattern '04-brand-kit*.pdf'`; `scripts/create_pdf_contact_sheets.py --pdf-pattern '04-brand-kit*.pdf'`.
- The validation/audit/contact-sheet tools now accept multiple `--pdf-pattern` values in one run.
- New one-click external risk test helper: `scripts/run_phase1_risk_export_outside_codex.command`.
- Full Phase 1 final export helper: `scripts/run_phase1_final_export_outside_codex.command`.
- Phase 2 Brand Kit refresh helper: `scripts/run_phase2_brandkit_fix_outside_codex.command`.
- Visual review dashboard builder: `scripts/build_pdf_visual_review_index.py`. It converts generated contact sheets into one HTML dashboard, e.g. `phase-1-visual-review-index.html`.
- Standard queue action board: `content-elevated-product-os/internal/_global/standard-queue-action-board.md`.
- Individual product/proofing system: `content-elevated-product-os/internal/_global/individual-product-and-proofing-system.md`.
- Standalone product maps exist for all 38 products at `content-elevated-product-os/internal/[product-slug]/standalone-products.md`.
- Review sample index: `rebranded-products-sample-direction/approval-samples.html`.
- Approved samples already applied to the full bundle:
  - `rebranded-products-sample-direction/dog-walkers-and-pet-sitters/dog-walkers-redesign-sample.html`
  - `rebranded-products-sample-direction/personal-stylists/personal-stylists-redesign-sample.html`
  - `rebranded-products-sample-direction/life-and-business-coaches/life-business-coaches-redesign-sample.html`
- Final PDF export is blocked inside the Codex sandbox by macOS/browser permission limits; do not retry the failed paths below. Use `internal/_global/pdf-export-terminal-runbook.md` and run the exporter from normal Terminal.
- Current operational source of truth: `internal/_global/work-session-checkpoint.md`.

## PDF Export Memory: Do Not Repeat These Attempts

The HTML packages are valid. The PDF issue is environmental, not a design/content failure.

Failed or blocked inside Codex:

- Google Chrome headless direct export from `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` did not produce PDFs; old headless exited with code 134.
- Chrome version tested: `Google Chrome 148.0.7778.178`.
- Adding Chrome flags like `--no-sandbox`, `--disable-dev-shm-usage`, `--disable-crash-reporter`, custom `HOME`, and custom `--user-data-dir` did not fix it. Chrome/Crashpad still tried protected `~/Library/Application Support/Google/Chrome/...` paths.
- Opening Chrome via macOS `open -na "Google Chrome"` is blocked by the Codex sandbox approval policy, so do not use it here.
- Swift/WebKit exporter initially failed because default SDK `MacOSX26.2.sdk` requires Swift 6.2 while installed Swift is 6.1.2.
- Swift/WebKit with `SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk` fixed the SDK mismatch but still timed out because WebKit needs sandbox-blocked Apple services and protected Library/cache paths.
- `HOME=/private/tmp/...`, `CFFIXED_USER_HOME=/private/tmp/...`, and temporary module caches did not make WebKit usable inside Codex.
- `cupsfilter` cannot convert `text/html` to PDF on this machine.
- Bundled Python has `reportlab` but not `weasyprint`, `playwright`, `selenium`, `pyppeteer`, or `pdfkit`; reportlab would not preserve the HTML/CSS design.
- Bundled Node has `playwright-core` but no browser binary available for direct Playwright PDF export.
- Browser plugin can inspect/render the in-app browser, but its exposed wrapper does not provide raw `page.pdf()` access.

Current approved path:

- Run `scripts/export_customer_pdfs_outside_codex.py` from normal macOS Terminal, outside Codex.
- For targeted fixes, use the new `--html-pattern` option from normal Terminal. Do not run Chrome PDF export from inside Codex unless this environment is restarted and explicitly retested.
- One-click helper: `scripts/run_pdf_export_outside_codex.command`.
- Phase 1 risk-test helper: `scripts/run_phase1_risk_export_outside_codex.command`.
- Runbook: `content-elevated-product-os/internal/_global/pdf-export-terminal-runbook.md`.

Playwright note:

- User installed Playwright locally on 2026-05-21 (`playwright` 1.60.0 present).
- `scripts/export_customer_pdfs_playwright.js` exists for browser-native PDF export and supports `--batch`, `--only`, `--html-pattern`, `--output`, `--timeout`, and `--headful`.
- Running Playwright Chromium from inside Codex failed with macOS MachPort/sandbox permission errors, so use it only from normal Terminal unless the Codex environment is restarted and retested.
- WeasyPrint is not the preferred export path for these high-design HTML PDFs because our layouts rely on browser rendering/CSS behavior that Chrome/Playwright handles more predictably.

Retest after granting macOS permissions:

- On 2026-05-20, after the user granted additional permissions, Codex could list protected Library paths, but the active sandbox still blocked browser PDF export.
- Chrome headless still exited with code 134 from inside Codex.
- Swift/WebKit still failed creating `~/Library/WebKit/html_to_pdf_webkit.swift/...` and `~/Library/Caches/html_to_pdf_webkit.swift/...` support folders, then timed out.
- Conclusion: granting privacy permissions during a live session is not enough for this environment. Either restart Codex and retest once, or use the external Terminal exporter, which remains the recommended path.

## Internal Files Rule

- Listing copy, website copy, launch notes, upload notes, product strategy, pricing tests, Payhip admin notes, and audit notes belong in `content-elevated-product-os/internal/[product-slug]/`.
- Customer-facing redesigned bundle files belong in `rebranded-products-sample-direction/[product-slug]/`.
- Do not upload internal files to Payhip unless they are intentionally rewritten for the buyer.

## Listing Copy Inventory Rule

- Product descriptions should clearly state what buyers get: number of polished PDF guides/workbooks, customer-facing page count, spreadsheet count, prompt count if confirmed, template/script/system count when useful, and any internal files excluded from upload.
- Use `scripts/build_bundle_inventory.py` to rebuild inventory after product files change.
- Use `content-elevated-product-os/internal/[product-slug]/bundle-inventory.md` when writing Payhip and website copy.

## Working Rule

Do not rely on long chat history. Use the OS files, trackers, templates, and skill before making decisions.

## Flagship Niche Workflow

When the user picks the next flagship niche, follow this exact lane instead of improvising:

1. Confirm the product exists in `content-elevated-product-os/data/product-master.csv`, `bundle-inventory.csv`, `rebranded-products-sample-direction/[slug]/`, and `content-elevated-product-os/internal/[slug]/`.
2. If the product does not exist, say so clearly and recommend the closest existing product or a new-product creation path.
3. Inventory the bundle first: customer PDF source files, page count, prompt count, template/system count, spreadsheet count, Payhip URL, price status, cover status.
4. Open the original/source PDFs only when needed to recover missing meaning or fix extraction artifacts.
5. Perform a flagship audit:
   - buyer value
   - grammar and awkward copy
   - niche-specific accuracy
   - design quality
   - layout/export risk
   - compliance/claims risk when applicable
   - missing assets or upsell opportunities
6. Rebuild or upgrade the source HTML only when the current source is not launch-ready.
7. Keep each flagship niche tailored to its market. Do not reuse one generic design system across unrelated niches.
8. Update internal docs under `content-elevated-product-os/internal/[slug]/`, including inventory, Payhip copy, website copy, product workspace, audit notes, upload packet, and launch readiness.
9. Package the source using the correct package script and run source validation/source-density audits.
10. Add a focused external Terminal export helper for that flagship product.
11. Do not call the product upload-ready until PDF export, validation, layout-risk audit, contact sheets, and human visual proof are clean.
12. Update global memory and command-center docs before ending the work.

Flagship products already handled:

- Hair Stylists: first flagship. Clean source promoted, Start Here added, calendar split, export helper created.
- Med Spas: second flagship. Full premium clinical/aesthetic rebuild complete, source validation clean, export helper created.

Potential next flagship note:

- There is no dedicated Real Estate Agents Growth Bundle in the current master tracker/source library as of 2026-05-22.
- Closest existing real-estate-adjacent products are Mortgage Brokers, Interior Designers, HVAC Contractors, Plumbers, Personal Chefs, and Attorneys, which contain realtor/referral-partner content.
- If the user wants a true Real Estate Agents bundle, treat it as a new flagship product build, not a refresh of an existing tracked bundle.

## 2026-05-21 Hair Stylist Flagship Pivot

- The Hair Stylists Growth Bundle is now the priority flagship product to perfect first and sell ASAP.
- User wants one rock-solid product before continuing broad batch exports.
- Broken generated Hair Stylist HTML sources were backed up to `content-elevated-product-os/internal/hair-stylists/launch-readiness/superseded-generated-html-backup/`.
- Active Hair Stylist source was replaced with the cleaner earlier source set from `print-ready-pdfs/hair-stylist/`.
- The 90-day calendar was split into three standalone monthly HTML files:
  - `90-day-salon-content-calendar-month-1.html` - 11 pages
  - `90-day-salon-content-calendar-month-2.html` - 12 pages
  - `90-day-salon-content-calendar-month-3.html` - 15 pages
- Added new buyer-facing quick-start file:
  - `start-here-hair-stylist-growth-system.html` - 6 pages
- Current Hair Stylist active package inventory:
  - 10 PDF sources
  - 124 customer-facing pages
  - 2 spreadsheets
  - 57 dedicated prompts
- Hair Stylist artifact scan is clean: no footer/page-number cards, no known fragment headings, no numeric-only script cards.
- Hair Stylist source-density audit is clean.
- New focused export helper:
  - `scripts/run_hair_stylist_flagship_export_outside_codex.command`
- Next launch gate: run the Hair Stylist-only export from normal Terminal, review its visual dashboard/contact sheets, then improve spreadsheets if needed before Payhip upload.

## 2026-05-21 Brand Kit Color Swatches

- User requested Brand Kits show actual color swatches instead of only hex numbers.
- Added script: `scripts/add_brand_kit_color_swatches.py`.
- It injects shared `.color-swatch` styling and converts hex-only `<h3>#XXXXXX</h3>` headings into swatch+hex rows.
- Applied to source design files and active export packages.
- Refreshed Phase 1, next-batch, and standard queue source packages.

## 2026-05-21 Med Spa Flagship Rebuild

- Med Spas is the second priority flagship product after Hair Stylists.
- Old Med Spa generated HTML was not launch-ready: it had extraction artifacts, chopped headings, generic sections, and compliance-sensitive phrasing risk.
- Active Med Spa source was rebuilt from scratch in `rebranded-products-sample-direction/med-spas/`.
- Design direction: premium clinical aesthetic studio, light ivory/mist/sage/deep teal/blush palette, airy layouts, clean forms/tables, restrained luxury, no fake-gold crypto look.
- Content direction: high-trust med spa growth system focused on consult conversion, retention, client education, rebooking, content, email, and brand polish.
- Compliance posture: avoid guaranteed treatment outcomes, avoid before/after misuse, use provider-review language, respect local med spa advertising rules, and do not imply legal/medical advice.
- Current Med Spa active package inventory:
  - 9 PDF sources
  - 54 customer-facing pages
  - 45 prompts
  - 128 templates/scripts/systems
  - 0 spreadsheets
- Added buyer-facing quick-start file:
  - `start-here-med-spa-growth-system.html` - 6 pages
- The 90-day social calendar is split into three monthly files:
  - `02-90day-social-calendar-med-spa-month-1.html`
  - `02-90day-social-calendar-med-spa-month-2.html`
  - `02-90day-social-calendar-med-spa-month-3.html`
- Med Spa source-density audit is clean.
- Med Spa exact artifact scan is clean: no `Print-ready`, no numeric-only/chopped headings, no `undefined`, no `lorem`, no `HIPAA-compliant`, and no `guaranteed outcomes` phrase.
- Updated internal docs:
  - `internal/med-spas/bundle-inventory.md`
  - `internal/med-spas/payhip-listing-copy.md`
  - `internal/med-spas/website-product-copy.md`
  - `internal/med-spas/product-workspace.md`
  - `internal/med-spas/content-audit-notes.md`
  - `internal/med-spas/launch-readiness/med-spa-flagship-deep-audit.md`
  - `internal/med-spas/launch-readiness/med-spa-payhip-upload-packet.md`
- New Med Spa export helper:
  - `scripts/run_med_spa_flagship_export_outside_codex.command`
- Next launch gate: run the Med Spa-only export helper from normal Terminal, review its visual dashboard/contact sheets, then upload the PDF set to Payhip if clean.

## 2026-05-26 Videographers Flagship Rebuild

- Videographers is now the next flagship product after Hair Stylists and Med Spas.
- Product exists in the tracked catalog and Payhip URL is recorded:
  - `https://payhip.com/b/hofPG`
- Old Videographer source had strong visual direction but was not launch-ready because extracted content included broken fragments such as standalone placeholder endings.
- Active Videographer source was rebuilt from scratch in `rebranded-products-sample-direction/videographers/`.
- Design direction: premium cinematic creator/studio system; black/charcoal base, electric blue/cyan/violet accents, crisp uppercase editorial headings, light working pages, dark feature pages, and video-production language.
- Content direction: wedding, corporate, and commercial videographers; inquiry conversion, package presentation, pre-production questionnaires, delivery emails, review requests, vendor outreach, portfolio/content cadence, and brand polish.
- Added buyer-facing quick-start file:
  - `start-here-videographer-growth-system.html` - 5 pages
- Current Videographer active package inventory:
  - 9 PDF sources
  - 53 customer-facing pages
  - 52 AI prompts
  - 137 templates/scripts/systems
  - 0 spreadsheets
- The 90-day content calendar is split into three monthly files:
  - `02-90day-content-calendar-videographers-month-1.html`
  - `02-90day-content-calendar-videographers-month-2.html`
  - `02-90day-content-calendar-videographers-month-3.html`
- Videographers source-density audit is clean.
- Videographers exact artifact scan is clean across source and packaged HTML: no `Print-ready`, no `undefined`, no `lorem`, no known placeholder fragments, and no old extraction leftovers.
- Updated internal docs:
  - `internal/videographers/bundle-inventory.md`
  - `internal/videographers/payhip-listing-copy.md`
  - `internal/videographers/website-product-copy.md`
  - `internal/videographers/product-workspace.md`
  - `internal/videographers/content-audit-notes.md`
  - `internal/videographers/launch-readiness/videographer-flagship-deep-audit.md`
  - `internal/videographers/launch-readiness/videographer-payhip-upload-packet.md`
- New Videographers export helper:
  - `scripts/run_videographer_flagship_export_outside_codex.command`
- Next launch gate: run the Videographer-only export helper from normal Terminal, review its visual dashboard/contact sheets, then upload the PDF set to Payhip if clean.
