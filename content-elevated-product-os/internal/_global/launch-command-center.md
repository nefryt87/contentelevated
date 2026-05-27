# Content Elevated Launch Command Center

Last updated: 2026-05-26

This is the highest-level operating board. Use it first when resuming work so we do not burn time or credits rediscovering the project.

## North Star

Get redesigned bundles into Payhip and connected to `contentelevatedhq.com` as quickly as possible, while keeping enough quality control to avoid uploading messy or off-brand files.

## Current Reality

- Total bundle products tracked: 38
- Customer-facing HTML/PDF source files tracked: 293
- Customer-facing pages tracked: 1930
- Spreadsheets tracked: 7
- Products with Payhip URLs recorded: 33 / 38
- Products missing Payhip URLs: 5
- Automated catalog scan: clean across all buyer-facing files.
- Source-density audit: clean across Phase 1, Next Approved Batch, and Standard Queue. No active source page has more than 4 stacked `asset-card`/`data-card` blocks.
- Main blocker: external PDF export/proofing. Codex cannot reliably launch Chrome/Playwright for PDF printing inside this sandbox, so final PDF export must be run from normal Terminal.
- Current sales-first pivot: Hair Stylists is the first flagship proof product. Med Spas is the second flagship product. Videographers is the third flagship product and has been rebuilt as a cinematic creator/studio package.

## Sales-First Priority Order

1. **Launch Hair Stylists first**: export the flagship bundle, proof it, upload to Payhip, connect/update the website listing.
2. **Launch Med Spas second**: export the rebuilt Med Spa flagship, proof it, upload to Payhip, connect/update the website listing.
3. **Launch Videographers third**: export the rebuilt Videographer flagship, proof it, upload to Payhip, connect/update the website listing.
4. **Launch Phase 1 / Next Approved Batch by exception**: use the flagship workflow as the QC standard before broad uploads.
5. **Launch Standard Queue**: products are packaged and mechanically clean, but some need URL/cover confirmation and later visual proofing.
6. **Only then expand into standalone products**: content calendar, brand kit, prompt library, client templates, etc.

## Flagship Niche Protocol

When the user names the next flagship niche:

1. Confirm it exists in the master tracker and source folders before opening a broad set of files.
2. If it exists, build a focused lane: inventory, audit, source upgrade, package validation, export helper, upload packet.
3. If it does not exist, do not fake it. Recommend the closest existing product or treat it as a new-product build.
4. Keep the design niche-specific. Flagship products should not look like cloned templates.
5. Do not call it upload-ready until export validation, layout-risk audit, contact sheets, and human visual proof are clean.

Current note: no dedicated Real Estate Agents Growth Bundle exists in the tracked catalog. Mortgage Brokers is the closest existing real-estate-adjacent bundle.

## Do Not Spend Credits On Yet

- Redesigning approved bundles unless the user spots a real issue.
- Re-reading every source PDF or every HTML file without a specific question.
- Deep research/proofreading all products before the first sales-ready upload batch exists.
- Standalone product buildout before bundles are live with the upgraded files.
- More design concepts for categories already approved.

## Credit-Efficient Operating Rules

- Use the generated inventory, handoff JSON, and action boards before opening individual product files.
- Batch work by launch group: Phase 1, Next Approved Batch, Standard Queue.
- Run automated scans after edits, not before every small thought.
- Treat HTML packages as source of truth until PDF export works.
- When visual QA is needed, review 1 representative file first, then spot-check the rest by exception.
- Keep approvals parked in `user-approval-parking-lot.md` instead of stopping the workstream.

## Active Workstreams

| Workstream | Status | Next Action | Source |
|---|---|---|---|
| Hair Stylists flagship | Active priority; clean source promoted; Start Here guide added; artifact scan clean | Run Hair Stylist flagship export helper from normal Terminal and review contact sheets | `exports/phase-1-payhip-source-package/hair-stylists/` |
| Med Spas flagship | Active second priority; premium clinical/aesthetic rebuild complete; source validation clean | Run Med Spa flagship export helper from normal Terminal and review contact sheets | `exports/phase-1-payhip-source-package/med-spas/` |
| Videographers flagship | Active third priority; cinematic creator/studio rebuild complete; source validation clean | Run Videographer flagship export helper from normal Terminal and review contact sheets | `exports/next-batch-source-package/videographers/` |
| Phase 1 upload | Patched source ready, old final-v2 export is superseded | Resume broad Phase 1 after Hair Stylists is clean and uploaded | `exports/phase-1-payhip-source-package/` |
| Next approved batch | Patched source ready; Phase 2 full-v1 automation passed but Brand Kits need refresh | Run Phase 2 Brand Kit helper after Phase 1 is stable | `exports/next-batch-source-package/` |
| Standard queue | Packaged, mechanically clean, and source-density hardened | Confirm missing URLs/covers, then export/proof later | `exports/standard-queue-source-package/` |
| Website copy | Handoffs generated | Use JSON/CSV when updating storefront data | `exports/*listing-copy-export.csv` |
| Standalone products | Planned only | Start after bundles are uploaded | `internal/{slug}/standalone-products.md` |

## Missing Payhip URL Confirmations

| Product | Batch | Note |
|---|---|---|
| Aestheticians Growth Bundle | Standard queue | Confirm directly in Payhip before website linking. |
| Attorneys Growth Bundle | Standard queue | Website data suggests an Attorney URL exists; confirm before updating tracker. |
| Hair Stylists Growth Bundle | Phase 1 | Confirm directly in Payhip before website linking. |
| Insurance Agents Growth Bundle | Standard queue | Confirm directly in Payhip before website linking. |
| Lash Technicians Growth Bundle | Standard queue | Confirm directly in Payhip before website linking. |

## Resume Checklist

When starting a new session, do this in order:

1. Open this command center.
2. Open `work-session-checkpoint.md` only if more detail is needed.
3. Check `pdf-final-qa-command-center.md`.
4. Work on the highest-priority active blocker: Hair Stylists flagship export/review.
5. Then work on Med Spas flagship export/review.
6. Rebuild affected boards/packages only after changes.
7. Sync to `/Users/tomasz/Documents/Codex/Content-Elevated` before ending.

## Key Files

- Operating brief: `internal/_global/content-elevated-operating-brief.md`
- Resume point: `internal/_global/work-session-checkpoint.md`
- Project queue: `internal/_global/next-phase-work-board.md`
- PDF/export SOP: `internal/_global/pdf-export-and-payhip-upload-sop.md`
- PDF terminal runbook: `internal/_global/pdf-export-terminal-runbook.md`
- PDF final QA command center: `internal/_global/pdf-final-qa-command-center.md`
- Hair Stylist flagship audit: `internal/hair-stylists/launch-readiness/hair-stylist-flagship-deep-audit.md`
- Med Spa flagship audit: `internal/med-spas/launch-readiness/med-spa-flagship-deep-audit.md`
- Med Spa upload packet: `internal/med-spas/launch-readiness/med-spa-payhip-upload-packet.md`
- Videographer flagship audit: `internal/videographers/launch-readiness/videographer-flagship-deep-audit.md`
- Videographer upload packet: `internal/videographers/launch-readiness/videographer-payhip-upload-packet.md`
- Upload command sheet: `internal/_global/upload-execution-command-sheet.md`
- Phase 1 launch upload checklist: `internal/_global/phase-1-launch-upload-checklist.md`
- Phase 1 action board: `internal/_global/phase-1-payhip-action-board.md`
- Next batch action board: `internal/_global/next-batch-payhip-action-board.md`
- Standard queue action board: `internal/_global/standard-queue-action-board.md`
- Catalog coverage: `internal/_global/catalog-operations-coverage.md`
