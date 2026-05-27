# Phase 1 Upload Safety Audit

Last updated: 2026-05-19

## Scope

Products scanned:

- Hair Stylists
- Med Spas
- Dentists
- Nutritionists
- HVAC Contractors
- Accountants & CPAs
- Wedding Photographers
- Etsy Sellers

## Automated Checks Completed

Scanned buyer-facing files for:

- broken replacement characters
- old `90 Day` title formatting
- `print-ready` language
- marketplace/admin references such as Gumroad, Stan Store, ConvertKit, launch price, sales channels
- obvious placeholder/internal language
- aggressive quantified claims in Phase 1 buyer-facing files

## Fixes Made

- Replaced broken bullet characters in the Dentists lead magnet.
- Rebuilt the Dentists lead magnet into a clean 4-page mini-guide.
- Standardized visible `90 Day` wording to `90-Day` across Phase 1 calendar files.
- Softened aggressive quantified claims in the Dentists AI Playbook.
- Softened an aggressive lead-recovery claim in the Wedding Photographers AI Playbook.
- Softened aggressive revenue, no-show, review, ROI, booking, and conversion claims across the Phase 1 buyer-facing files.
- Standardized obvious UK spellings in Etsy-facing copy to US-facing wording.
- Confirmed the current Phase 1 high-risk scan is clean for buyer-facing files.
- Rebuilt bundle inventory after the Dentists lead magnet cleanup.
- Updated Dentists listing/website copy counts from 55 to 58 detected templates/scripts/systems.
- Built a validated Phase 1 source package at `exports/phase-1-payhip-source-package/`.
- Created a zipped source package at `exports/phase-1-payhip-source-package.zip`.
- Confirmed packaged file counts and spreadsheet counts match bundle inventory for all 8 Phase 1 products.

## Intentional Exclusions

Hair Stylists contains two internal/reference files that should not be uploaded as buyer-facing files:

- `hairstylist-bundle-launch-kit.html`
- `hairstylist-complete-growth-bundle-master-reference.html`

These files contain marketplace strategy, launch pricing, Gumroad/Etsy/Stan Store references, ConvertKit notes, and internal sales-channel planning. They are useful internally but should stay out of the buyer upload package unless rewritten.

Hair Stylists also contains a `v2/` draft folder with corrupted imported glyphs. The current Hair Stylists buyer-facing inventory uses the approved root-level files, not the `v2/` draft files.

## Remaining Before Upload

- Human proofread of every final buyer-facing file.
- Final PDF export from the validated HTML source package.
- Visual review of generated PDFs.
- Confirm final Payhip product URLs.
- Confirm current price and launch price.
- Save final cover/mockup images locally.
- Confirm spreadsheets are included where inventory says they exist.

## Export Blocker

Automated local PDF export was attempted on 2026-05-19. Chrome aborted in headless mode, bundled Playwright is installed without its browser binary, and the local Swift/WebKit toolchain is mismatched. The source package is still clean and ready; final PDF generation should happen in a working Chrome print-to-PDF/Playwright environment or a dedicated export tool.
