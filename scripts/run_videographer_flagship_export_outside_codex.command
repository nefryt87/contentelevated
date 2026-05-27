#!/bin/zsh
set -euo pipefail

cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"

EXPORT="content-elevated-product-os/exports/customer-pdf-videographer-flagship-v1"

echo "Exporting Videographer flagship package to: $EXPORT"
node scripts/export_customer_pdfs_playwright.js \
  --batch next \
  --only videographers \
  --out "$EXPORT" \
  --timeout 120000

python3 scripts/validate_customer_pdf_export.py \
  --batch next \
  --root "$EXPORT" \
  --only videographers

python3 scripts/audit_pdf_layout_risk.py \
  --batch next \
  --root "$EXPORT" \
  --only videographers

python3 scripts/create_pdf_contact_sheets.py \
  --root "$EXPORT" \
  --batch next \
  --only videographers \
  --max-pages 14 \
  --out "$EXPORT/_visual-audit"

python3 scripts/build_pdf_visual_review_index.py \
  --root "$EXPORT/_visual-audit" \
  --batch "videographer-flagship-v1" \
  --title "Videographer Flagship Visual Review"

echo "Done."
echo "Review index: $EXPORT/_visual-audit/videographer-flagship-v1-visual-review-index.html"
