# Work Session Checkpoint

Last updated: 2026-05-26

Use this file as the fast resume point for the Content Elevated product library.

## Current Business Setup

- Brand: Content Elevated
- Storefront domain: `contentelevatedhq.com`
- Payhip store: `https://payhip.com/ContentElevated`
- Payhip handles checkout and digital delivery.
- The website is the premium storefront and should route product CTAs to the matching Payhip checkout.
- Current Payhip products are live as bundles, but many still use the older/basic PDFs and need updated files uploaded after final export/proof.

## Current Source Of Truth

- Product OS: `content-elevated-product-os/`
- Redesigned HTML product files: `rebranded-products-sample-direction/`
- Executive command center: `content-elevated-product-os/internal/_global/launch-command-center.md`
- Operating role brief: `content-elevated-product-os/internal/_global/content-elevated-operating-brief.md`
- Credit-efficient SOP: `content-elevated-product-os/internal/_global/credit-efficient-production-sop.md`
- Sales launch roadmap: `content-elevated-product-os/internal/_global/sales-launch-roadmap.md`
- Product master tracker: `content-elevated-product-os/data/product-master.csv`
- Structured tracker: `content-elevated-product-os/data/product-master.json`
- Bundle inventory: `content-elevated-product-os/data/bundle-inventory.csv`
- Design decisions: `content-elevated-product-os/internal/_global/design-approval-memory.md`
- Work queue: `content-elevated-product-os/internal/_global/next-phase-work-board.md`
- PDF/export SOP: `content-elevated-product-os/internal/_global/pdf-export-and-payhip-upload-sop.md`
- Terminal PDF export runbook: `content-elevated-product-os/internal/_global/pdf-export-terminal-runbook.md`
- Upload execution command sheet: `content-elevated-product-os/internal/_global/upload-execution-command-sheet.md`
- Phase 1 launch upload checklist: `content-elevated-product-os/internal/_global/phase-1-launch-upload-checklist.md`
- Catalog operations coverage: `content-elevated-product-os/internal/_global/catalog-operations-coverage.md`
- Catalog cover map: `content-elevated-product-os/internal/_global/catalog-cover-map.md`
- User approval parking lot: `content-elevated-product-os/internal/_global/user-approval-parking-lot.md`
- Parked design review brief: `content-elevated-product-os/internal/_global/parked-design-review-brief.md`
- Individual product/proofing system: `content-elevated-product-os/internal/_global/individual-product-and-proofing-system.md`
- Website launch integrations: `content-elevated-product-os/internal/_global/website-launch-integrations.md`

## Flagship Workflow Memory

When Tomasz picks a flagship niche, first confirm the product exists in the trackers and folders. Then run a focused flagship lane:

- inventory the current bundle
- audit buyer value, grammar, design, niche accuracy, compliance/claims risk, and missing assets
- rebuild source only where needed
- update internal niche docs
- package and validate source
- add a focused external Terminal export helper
- require PDF export, validation, layout-risk audit, contact sheets, and human visual proof before Payhip upload

Products already moved into flagship treatment:

- Hair Stylists
- Med Spas
- Videographers

Catalog note:

- A dedicated Real Estate Agents Growth Bundle is not currently present in `product-master.csv`, `bundle-inventory.csv`, source folders, or internal workspaces.
- Closest existing product: Mortgage Brokers Growth Bundle.
- Real-estate-adjacent content also appears inside Interior Designers, HVAC Contractors, Plumbers, Personal Chefs, and Attorneys.

## Phase 1 Launch Batch

Phase 1 products:

- Hair Stylists
- Med Spas
- Dentists
- Nutritionists
- HVAC Contractors
- Accountants & CPAs
- Wedding Photographers
- Etsy Sellers

Status:

- Buyer-facing HTML source package is built.
- Source package validation is clean.
- Website copy handoff exists in Markdown and JSON.
- Payhip action board exists in Markdown and CSV.
- Full catalog automated readiness audit is clean.
- Final customer PDF export `customer-pdf-phase-1-final-v2` passed automated checks.
- Human review found a visual issue in Nutritionists Brand Kit; the PDF was quarantined, the source was fixed from 7 pages to 9 pages with lighter export effects, the fixed version was re-exported into `customer-pdf-phase-1-nutritionists-fix-v1`, contact-sheet checked, and restored into final-v2.
- Med Spas has been rebuilt as the second flagship product. Active source is now a fresh premium clinical/aesthetic design with cleaned grammar, safer compliance language, and a 9-file/54-page buyer package. The old final-v2 Med Spa PDFs are superseded until the Med Spa flagship export helper is run and visually approved.

Source package:

- `content-elevated-product-os/exports/phase-1-payhip-source-package/`
- `content-elevated-product-os/exports/phase-1-payhip-source-package.zip`
- `content-elevated-product-os/exports/phase-1-listing-copy-export.csv`

Final customer PDF export:

- `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/phase-1/`
- Final human review hub: `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/phase-1-final-review-index.html`
- Visual audit contact sheets: `content-elevated-product-os/exports/customer-pdf-phase-1-final-v2/_visual-audit/phase-1/`
- Final CEO launch gate report: `content-elevated-product-os/internal/_global/phase-1-final-launch-gate-report.md`
- Final upload handoff: `content-elevated-product-os/internal/_global/phase-1-final-v2-upload-handoff.md`

Known Phase 1 Payhip URLs:

- Med Spas: `https://payhip.com/b/uRbgW`
- Dentists: `https://payhip.com/b/RXUZc`
- Nutritionists: `https://payhip.com/b/xz0Tr`
- HVAC Contractors: `https://payhip.com/b/r9Jay`
- Accountants & CPAs: `https://payhip.com/b/9zcAT`
- Wedding Photographers: `https://payhip.com/b/r5HSz`
- Etsy Sellers: `https://payhip.com/b/x7D4I`
- Hair Stylists: missing; confirm in Payhip before website connection.

Phase 1 blockers:

- Final human skim of review hub/contact sheets.
- Confirm prices in Payhip.
- Save product cover images locally.
- Confirm Hair Stylists Payhip URL.
- Re-upload redesigned files to Payhip.
- Run focused flagship exports for Hair Stylists and Med Spas from normal Terminal before broad Phase 1 upload.

Med Spa flagship:

- Active source: `rebranded-products-sample-direction/med-spas/`
- Packaged source: `content-elevated-product-os/exports/phase-1-payhip-source-package/med-spas/`
- Deep audit: `content-elevated-product-os/internal/med-spas/launch-readiness/med-spa-flagship-deep-audit.md`
- Upload packet: `content-elevated-product-os/internal/med-spas/launch-readiness/med-spa-payhip-upload-packet.md`
- Export helper: `scripts/run_med_spa_flagship_export_outside_codex.command`
- Expected output: `content-elevated-product-os/exports/customer-pdf-med-spa-flagship-v1/`
- Status: source validation clean; PDF export and human visual proof still needed.

## Videographers Flagship

- Product exists and Payhip URL is recorded: `https://payhip.com/b/hofPG`.
- Active source has been rebuilt as a cinematic creator/studio package for wedding, corporate, and commercial videographers.
- Inventory: 9 PDF sources, 53 customer-facing pages, 52 AI prompts, 137 templates/scripts/systems, 0 spreadsheets.
- Source package has been refreshed in `content-elevated-product-os/exports/next-batch-source-package/videographers/`.
- Artifact scan is clean across source and packaged HTML.
- Source-density audit is clean for Videographers.
- Deep audit: `content-elevated-product-os/internal/videographers/launch-readiness/videographer-flagship-deep-audit.md`
- Upload packet: `content-elevated-product-os/internal/videographers/launch-readiness/videographer-payhip-upload-packet.md`
- Export helper: `scripts/run_videographer_flagship_export_outside_codex.command`
- Expected output: `content-elevated-product-os/exports/customer-pdf-videographer-flagship-v1/`
- Status: source validation clean; PDF export and human visual proof still needed.

## Next Approved Batch

These are approved/directionally approved and packaged as source files:

- Barbers
- Dog Walkers & Pet Sitters
- Personal Trainers
- Personal Chefs
- Nannies & Childcare Professionals
- Florists
- Event Planners
- Videographers
- Public Speakers
- Personal Stylists
- Life & Business Coaches

Source package:

- `content-elevated-product-os/exports/next-batch-source-package/`
- Review hub: `content-elevated-product-os/exports/next-batch-source-package/review-index.html`
- `content-elevated-product-os/exports/next-batch-source-package.zip`
- `content-elevated-product-os/exports/next-batch-listing-copy-export.csv`

PDF export:

- Full export completed at `content-elevated-product-os/exports/customer-pdf-phase-2-full-v1/`.
- Automated checks: 84 PDFs, validation errors 0, layout-risk attention 0, 84 contact sheets.
- Human visual QA found bottom-edge crowding in several long Brand Kit contact sheets, especially checklist/template pages.
- Source has been patched to split dense Brand Kit/card stacks into safer groups. Current active rule: no Phase 1 or Phase 2 source page should have more than 4 stacked `asset-card`/`data-card` blocks.
- Phase 2 is not upload-ready until targeted Brand Kit re-export is run from normal Terminal, then validated and contact-sheet reviewed.
- Videographers in this batch has been superseded by the fresh flagship rebuild above; use the Videographer-only helper before uploading that product.
- Targeted command pattern is now supported:
  - Export: `python3 scripts/export_customer_pdfs_outside_codex.py --batch next --html-pattern '04-brand-kit*.html' --output content-elevated-product-os/exports/customer-pdf-phase-2-brandkit-fix-v2 --slow --timeout 90`
  - Validate: `python3 scripts/validate_customer_pdf_export.py --batch next --pdf-pattern '04-brand-kit*.pdf' --output content-elevated-product-os/exports/customer-pdf-phase-2-brandkit-fix-v2`
  - Audit: `python3 scripts/audit_pdf_layout_risk.py --batch next --pdf-pattern '04-brand-kit*.pdf' --output content-elevated-product-os/exports/customer-pdf-phase-2-brandkit-fix-v2`
  - Contact sheets: `/Users/tomasz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/create_pdf_contact_sheets.py --batch next --root content-elevated-product-os/exports/customer-pdf-phase-2-brandkit-fix-v2 --pdf-pattern '04-brand-kit*.pdf'`
- Phase 1 source was patched after human review found two systemic failures:
  - `etsy-sellers/01-ai-playbook-etsy-sellers.pdf`: visual breakdown starting around page 16.
  - `hvac-contractors/05-phone-scripts-hvac.pdf`: page 04/05 crowding plus laggy PDF behavior.
- Root cause: overloaded fixed-height page stacks. Etsy used `asset-card`; HVAC used `data-card`, so the first splitter missed HVAC until `scripts/split_dense_pdf_cards.py` was updated to handle both card systems.
- New one-click external risk test helper: `scripts/run_phase1_risk_export_outside_codex.command`. Run it from Finder/Terminal to export the known-risk Phase 1 files, validate, layout-audit, and generate contact sheets before any full re-export.
- Standard queue was proactively hardened with the same density rule for Car Wash, Electricians, and Plumbers.
- Source-density audit: `python3 scripts/audit_html_source_density.py --batch all --max-cards 4` now reports 0 pages needing attention across active Phase 1, Phase 2, and standard queue source packages.

Operational boards:

- `content-elevated-product-os/internal/_global/next-batch-payhip-action-board.md`
- `content-elevated-product-os/internal/_global/next-batch-payhip-action-board.csv`
- `content-elevated-product-os/internal/_global/next-batch-cover-map.md`
- `content-elevated-product-os/internal/_global/next-batch-website-copy-handoff.md`
- `content-elevated-product-os/internal/_global/next-batch-website-copy-handoff.json`

## Design Items Parked For User Review

No products are currently parked for design review.

Approved and rolled across full bundle:

- Dog Walkers & Pet Sitters: sample approved by user at `rebranded-products-sample-direction/dog-walkers-and-pet-sitters/dog-walkers-redesign-sample.html`; direction applied across the full bundle and included in the next approved batch package.
- Personal Stylists: sample approved by user at `rebranded-products-sample-direction/personal-stylists/personal-stylists-redesign-sample.html`; page 4 badge/footer spacing refined, direction applied across the full bundle, and included in the next approved batch package.
- Life & Business Coaches: sample approved by user at `rebranded-products-sample-direction/life-and-business-coaches/life-business-coaches-redesign-sample.html`; direction applied across the full bundle and included in the next approved batch package.

## Automation Status

Working scripts:

- `scripts/build_bundle_inventory.py`
- `scripts/package_phase1_payhip_sources.py`
- `scripts/validate_phase1_package.py`
- `scripts/package_next_batch_sources.py`
- `scripts/audit_next_batch_readiness.py`
- `scripts/audit_full_catalog_readiness.py`
- `scripts/build_phase1_payhip_action_board.py`
- `scripts/build_phase1_cover_map.py`
- `scripts/build_phase1_website_copy_handoff.py`
- `scripts/build_next_batch_action_board.py`
- `scripts/build_next_batch_website_copy_handoff.py`
- `scripts/update_phase1_payhip_tracker.py`
- `scripts/update_product_master_from_site.py`
- `scripts/sync_product_master_json.py`
- `scripts/build_catalog_coverage_report.py`
- `scripts/build_standalone_product_maps.py`
- `scripts/build_standard_queue_action_board.py`
- `scripts/package_standard_queue_sources.py`
- `scripts/audit_standard_queue_readiness.py`
- `scripts/build_standard_queue_website_copy_handoff.py`
- `scripts/build_standard_queue_cover_map.py`
- `scripts/standard_queue.py`
- `scripts/build_catalog_cover_map.py`
- `scripts/export_listing_copy_csv.py`
- `scripts/build_launch_command_center.py`
- `scripts/export_customer_pdfs_outside_codex.py`
- `scripts/run_pdf_export_outside_codex.command`
- `scripts/validate_customer_pdf_export.py`
- `scripts/audit_pdf_layout_risk.py`
- `scripts/create_pdf_contact_sheets.py`
- `scripts/build_upload_execution_command_sheet.py`

PDF export automation is currently blocked inside Codex:

- Direct Google Chrome headless export did not produce PDFs; old headless exited with code 134.
- Chrome/Crashpad keeps reaching into protected `~/Library` paths even with temp profiles and crash reporter flags.
- Swift/WebKit with the default SDK fails because `MacOSX26.2.sdk` expects Swift 6.2 while installed Swift is 6.1.2.
- Swift/WebKit with `MacOSX15.5.sdk` gets past compilation but still times out because WebKit needs sandbox-blocked Apple services/Library paths.
- `cupsfilter` has no `text/html` to `application/pdf` filter.
- Bundled Playwright/Core exists but no browser binary is available for PDF export.
- Browser plugin can render/inspect pages but does not expose raw `page.pdf()`.
- Retest after macOS permissions on 2026-05-20: Codex could list protected Library paths, but Chrome headless still exited code 134 and Swift/WebKit still failed creating WebKit/cache support folders. Use external Terminal exporter unless Codex is restarted and retested.

Do not keep retrying these from inside Codex. Keep HTML packages as source of truth and run the external Terminal exporter:

- `scripts/export_customer_pdfs_outside_codex.py`
- `scripts/run_pdf_export_outside_codex.command`
- Output: `content-elevated-product-os/exports/customer-pdf-export/`

Latest proofing finding:

- The original full Phase 1 export at `customer-pdf-export` was not upload-ready and is no longer active.
- A mechanical print hardening pass changed source `.page` rules from `min-height:11in` to `height:11in` across print source directories.
- Hair Stylist corrupted/binary HTML sources were replaced with clean working source files before final export.
- The clean export is `customer-pdf-phase-1-final-v2`.
- Final-v2 validation: 65 PDFs checked, errors 0.
- Final-v2 layout-risk audit: 65 PDFs checked, files needing attention 0.
- Final-v2 visual contact sheets: 65 generated successfully.
- Old export attempts were moved to `content-elevated-product-os/exports/_archive-old-runs-2026-05-21/` so the active export folder stays focused.
- New rule remains: run a small demo export and contact-sheet audit before every full batch export.

Website update status:

- Homepage repetitive `Inside Every Bundle` section was removed.
- Kit newsletter route is wired through `/api/newsletter`.
- SEO indexing assets were added: metadata base, canonical, robots.txt, sitemap.xml.
- Google Analytics can be enabled with `NEXT_PUBLIC_GA_MEASUREMENT_ID`.
- Google Search Console verification can be enabled with `NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION`.
- Build passed after these changes.

## Standalone Product Planning

- Internal standalone product maps have been generated for all 38 products.
- Each map lives at `content-elevated-product-os/internal/{slug}/standalone-products.md`.
- These are internal planning files for future single-product Payhip listings and website cards.
- They use the current bundle inventory counts for pages, prompts, templates, upload files, and suggested price ranges.

## Standard Queue

- Standard queue action board exists at `content-elevated-product-os/internal/_global/standard-queue-action-board.md`.
- CSV version exists at `content-elevated-product-os/internal/_global/standard-queue-action-board.csv`.
- Source package exists at `content-elevated-product-os/exports/standard-queue-source-package/`.
- Source package archive exists at `content-elevated-product-os/exports/standard-queue-source-package.zip`.
- Website copy handoff exists at `content-elevated-product-os/internal/_global/standard-queue-website-copy-handoff.md`.
- Listing copy CSV exists at `content-elevated-product-os/exports/standard-queue-listing-copy-export.csv`.
- Combined upload execution command sheet exists at `content-elevated-product-os/internal/_global/upload-execution-command-sheet.md`.
- Readiness audit exists at `content-elevated-product-os/internal/_global/standard-queue-readiness-audit.md`.
- The standard queue includes 19 product folders. Automated pass is clean; final visual proofing and PDF export are still needed.
- Aestheticians, Attorneys, Insurance Agents, and Lash Technicians still need Payhip URL confirmation in the master tracker. Attorneys has a probable website match in the standard cover map, but still confirm before upload.

## Next Practical Steps

1. Start every session from `internal/_global/launch-command-center.md`.
2. Current priority: perfect Hair Stylists as the flagship first product.
3. Run `scripts/run_hair_stylist_flagship_export_outside_codex.command` from normal Terminal/Finder and review the generated dashboard/contact sheets.
4. If Hair Stylist visual export is clean, improve/review the two spreadsheets and package the final Payhip upload folder.
5. Confirm Hair Stylists Payhip URL and price.
6. Update Payhip with redesigned Hair Stylist PDFs/spreadsheets first.
7. Update the website Hair Stylists product page copy from `internal/hair-stylists/website-product-copy.md`.
8. After Hair Stylists is live and sellable, return to Phase 1/next-batch exports.
9. Save cover images into `content-elevated-product-os/assets/product-covers/`.
10. After Phase 1 is live, move into the next approved batch package, then the standard queue package.
