#!/bin/zsh
set -euo pipefail

cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"

EXPORT="content-elevated-product-os/exports/customer-pdf-med-spa-flagship-v1"

echo "Exporting Med Spa flagship package to: $EXPORT"
node scripts/export_customer_pdfs_playwright.js \
  --batch phase-1 \
  --only med-spas \
  --out "$EXPORT" \
  --timeout 120000

python3 scripts/validate_customer_pdf_export.py \
  --batch phase-1 \
  --root "$EXPORT" \
  --only med-spas

python3 scripts/audit_pdf_layout_risk.py \
  --batch phase-1 \
  --root "$EXPORT" \
  --only med-spas

python3 scripts/create_pdf_contact_sheets.py \
  --root "$EXPORT" \
  --batch phase-1 \
  --only med-spas \
  --max-pages 12 \
  --out "$EXPORT/_visual-audit"

python3 scripts/build_pdf_visual_review_index.py \
  --root "$EXPORT/_visual-audit" \
  --batch "med-spa-flagship-v1" \
  --title "Med Spa Flagship Visual Review"

echo "Done."
echo "Review index: $EXPORT/_visual-audit/med-spa-flagship-v1-visual-review-index.html"
