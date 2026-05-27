# Content Elevated Product OS

This folder is the operating system for the Content Elevated product library. Use it to avoid re-reading the whole chat and to keep product development, copy, Payhip uploads, website updates, and marketing organized.

## Core Outputs

- `data/product-master.csv`: master tracker for all product bundles.
- `data/product-master.json`: same tracker in structured format for scripts and website import.
- `data/bundle-inventory.csv`: concrete product inventory for listing copy, including customer-facing file count, page count, spreadsheet count, prompt count, and template estimates.
- `data/bundle-inventory.json`: detailed inventory with per-file page/prompt/template counts and internal-file flags.
- `data/single-product-roadmap.csv`: future individual products split out from each bundle.
- `internal/[product-slug]/`: internal product workspace for Payhip copy, website copy, launch copy, upload checklists, audit notes, Payhip URLs, prices, and strategy notes.
- `copy-templates/payhip-product-copy-template.md`: copy structure for Payhip listings.
- `copy-templates/website-product-copy-template.md`: copy structure for website product pages.
- `marketing/content-elevated-launch-plan.md`: phased launch plan for selling soon.
- `skills/content-elevated-product-os/SKILL.md`: reusable local skill/instructions for future Codex work.

## Live Store Memory

- Payhip store: `https://payhip.com/ContentElevated`
- Products are already listed on Payhip as bundles.
- Current Payhip listings use the original/basic PDF files.
- As products are redesigned and proofread, the Payhip files need to be re-uploaded/replaced.
- Payhip remains the checkout and digital delivery platform.
- The Content Elevated website is the premium storefront and should link product CTAs to the matching Payhip checkout.

## Asset Memory

- Product cover photos/mockups currently exist on Payhip.
- We should also save every cover image locally inside `content-elevated-product-os/assets/product-covers/`.
- Local cover file naming should match product slugs, for example `hair-stylists-cover.png`.
- Product cover assets should be used consistently across Payhip, the website, and launch marketing.

## Future Product Expansion

The current store focuses on bundles. Down the line, split strong bundle components into individual products:

- 90-day content calendars
- Brand kits
- AI playbooks
- Prompt libraries
- Client intake/onboarding systems
- Email/communication templates
- Retention/rebooking systems
- Lead magnets/freebie products

Each individual product should get its own Payhip listing, website product page, cover image, price, description, and launch copy.

## Product Status Stages

1. `needs proofread`: source content has not had a deep editorial pass.
2. `proofread complete`: grammar, extraction, clarity, and niche fit reviewed.
3. `copy ready`: Payhip and website copy created.
4. `uploaded`: product is live on Payhip.
5. `website connected`: website product page points to the correct Payhip checkout.
6. `marketing active`: included in launch content, email, or ad plan.

## Efficient Batch Workflow

Work in batches by category:

1. Choose one category, such as Beauty or Health & Wellness.
2. Create or update one niche research brief.
3. Proofread the product documents for that niche.
4. Generate Payhip and website copy from the approved product.
5. Add/update Payhip URL and price in `product-master.csv`.
6. Add the website product data.
7. Add the niche to the current marketing campaign.
8. Save/update cover images in `assets/product-covers`.

Do not deeply research the same niche repeatedly. Reuse the approved research brief and product tracker.

## Active Batch

Current batch: Phase 1 launch set.

Created:

- Launch board: `internal/_global/phase-1-launch-board.md`
- Copy status: `internal/_global/phase-1-copy-status.md`
- Upload safety audit: `internal/_global/phase-1-upload-safety-audit.md`
- Payhip upload manifest: `internal/_global/phase-1-payhip-upload-manifest.md`
- Website integration map: `internal/_global/phase-1-website-integration-map.md`
- Source package for final PDF export: `exports/phase-1-payhip-source-package/`
- Source package archive: `exports/phase-1-payhip-source-package.zip`
- Phase 1 listing copy CSV: `exports/phase-1-listing-copy-export.csv`
- Source package validation: `internal/_global/phase-1-package-validation.md`
- Payhip action board: `internal/_global/phase-1-payhip-action-board.md`
- Cover asset map: `internal/_global/phase-1-cover-map.md`
- Website copy handoff: `internal/_global/phase-1-website-copy-handoff.md` and `internal/_global/phase-1-website-copy-handoff.json`
- PDF export and Payhip upload SOP: `internal/_global/pdf-export-and-payhip-upload-sop.md`
- Design approval memory: `internal/_global/design-approval-memory.md`
- Next phase board: `internal/_global/next-phase-work-board.md`
- Phase 1 launch campaign: `marketing/phase-1-launch-campaign.md`
- Next batch readiness audit: `internal/_global/next-batch-readiness-audit.md`
- Next batch Payhip action board: `internal/_global/next-batch-payhip-action-board.md`
- Next batch cover map: `internal/_global/next-batch-cover-map.md`
- Next batch website copy handoff: `internal/_global/next-batch-website-copy-handoff.md` and `internal/_global/next-batch-website-copy-handoff.json`
- Work session checkpoint: `internal/_global/work-session-checkpoint.md`
- Catalog operations coverage report: `internal/_global/catalog-operations-coverage.md`
- Catalog cover map: `internal/_global/catalog-cover-map.md`
- User approval parking lot: `internal/_global/user-approval-parking-lot.md`
- Next batch source package: `exports/next-batch-source-package/`
- Next batch source package archive: `exports/next-batch-source-package.zip`
- Next batch listing copy CSV: `exports/next-batch-listing-copy-export.csv`
- Standard queue action board: `internal/_global/standard-queue-action-board.md` and `internal/_global/standard-queue-action-board.csv`
- Individual product/proofing system: `internal/_global/individual-product-and-proofing-system.md`
- User review sample index: `../rebranded-products-sample-direction/approval-samples.html`
- Payhip listing copy: `internal/[phase-1-product]/payhip-listing-copy.md`
- Website product copy: `internal/[phase-1-product]/website-product-copy.md`
- Content audit notes: `internal/[phase-1-product]/content-audit-notes.md`

Inventory system:

- Bundle inventory script: `scripts/build_bundle_inventory.py`
- Product tracker JSON sync script: `scripts/sync_product_master_json.py`
- Product tracker Payhip URL sync script: `scripts/update_product_master_from_site.py`
- Next batch action board script: `scripts/build_next_batch_action_board.py`
- Next batch website handoff script: `scripts/build_next_batch_website_copy_handoff.py`
- Catalog coverage report script: `scripts/build_catalog_coverage_report.py`
- Catalog cover map script: `scripts/build_catalog_cover_map.py`
- Listing copy CSV export script: `scripts/export_listing_copy_csv.py`
- Standalone product map script: `scripts/build_standalone_product_maps.py`
- Standard queue action board script: `scripts/build_standard_queue_action_board.py`
- Inventory output: `data/bundle-inventory.csv` and `data/bundle-inventory.json`
- Per-product inventory: `internal/[product-slug]/bundle-inventory.md`
- Standalone planning maps: `internal/[product-slug]/standalone-products.md`

Current export status:

- Phase 1 buyer-facing HTML source package is built and validated clean.
- Next approved batch buyer-facing HTML source package is built.
- Spreadsheets are included for Hair Stylists and Etsy Sellers.
- Payhip listing copy, website product copy, upload checklists, and standalone-product planning maps exist for all 38 product folders.
- Dog Walkers & Pet Sitters, Personal Stylists, and Life & Business Coaches have approved directions applied across the full bundles and included in the next approved batch package.
- Full catalog automated readiness scan is clean for broken glyphs, production wording, old admin/platform references, obvious placeholder/internal wording, aggressive guarantee language, and common UK spellings.
- Automated local PDF export is blocked by this desktop environment because Chrome aborts in headless mode, Playwright has no installed browser binary, and the local Swift/WebKit toolchain is mismatched. Keep the HTML package as the source of truth for final PDF export.

Next:

- Export final PDFs from the validated HTML source package, then visually proof the PDFs.
- Confirm Payhip URL, price, and local cover image for each Phase 1 product.
- Add Hair Stylists to the website once its Payhip URL and cover image are confirmed.
- Update website product data with final copy and checkout links.
- Continue the remaining standard queue and final export/proofing work.
