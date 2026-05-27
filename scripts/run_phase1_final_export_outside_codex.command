#!/bin/zsh
set -e

cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"

OUT="content-elevated-product-os/exports/customer-pdf-phase-1-final-v3"
PY="/Users/tomasz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"

echo "Exporting full Phase 1 final candidate into: $OUT"
echo ""

python3 scripts/audit_html_source_density.py --batch phase-1 --max-cards 4

python3 scripts/export_customer_pdfs_outside_codex.py \
  --batch phase-1 \
  --output "$OUT" \
  --slow \
  --timeout 120

python3 scripts/validate_customer_pdf_export.py \
  --batch phase-1 \
  --output "$OUT"

python3 scripts/audit_pdf_layout_risk.py \
  --batch phase-1 \
  --output "$OUT"

"$PY" scripts/create_pdf_contact_sheets.py \
  --root "$OUT" \
  --batch phase-1 \
  --max-pages 45

python3 scripts/build_pdf_visual_review_index.py \
  --root "$OUT" \
  --batch phase-1 \
  --title "Phase 1 Final V3 Visual Review"

echo ""
echo "Phase 1 final candidate export complete."
echo "Review dashboard:"
echo "$OUT/phase-1-visual-review-index.html"
