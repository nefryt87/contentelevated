#!/bin/zsh
set -e

cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"

OUT="content-elevated-product-os/exports/customer-pdf-phase-2-brandkit-fix-v2"
PY="/Users/tomasz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"

echo "Exporting Phase 2 Brand Kit refresh into: $OUT"
echo ""

python3 scripts/audit_html_source_density.py --batch next --max-cards 4

python3 scripts/export_customer_pdfs_outside_codex.py \
  --batch next \
  --html-pattern "04-brand-kit*.html" \
  --output "$OUT" \
  --slow \
  --timeout 120

python3 scripts/validate_customer_pdf_export.py \
  --batch next \
  --pdf-pattern "04-brand-kit*.pdf" \
  --output "$OUT"

python3 scripts/audit_pdf_layout_risk.py \
  --batch next \
  --pdf-pattern "04-brand-kit*.pdf" \
  --output "$OUT"

"$PY" scripts/create_pdf_contact_sheets.py \
  --root "$OUT" \
  --batch next \
  --pdf-pattern "04-brand-kit*.pdf" \
  --max-pages 45

python3 scripts/build_pdf_visual_review_index.py \
  --root "$OUT" \
  --batch next \
  --title "Phase 2 Brand Kit Visual Review"

echo ""
echo "Phase 2 Brand Kit refresh complete."
echo "Review dashboard:"
echo "$OUT/next-visual-review-index.html"
