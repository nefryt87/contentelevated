#!/bin/zsh
set -e

cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"

OUT="content-elevated-product-os/exports/customer-pdf-phase-1-risk-test-v1"
PY="/Users/tomasz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"

echo "Exporting Phase 1 risk files into: $OUT"
echo ""

python3 scripts/export_customer_pdfs_outside_codex.py \
  --batch phase-1 \
  --only etsy-sellers \
  --html-pattern "01-ai-playbook-etsy-sellers.html" \
  --output "$OUT" \
  --slow \
  --timeout 120

python3 scripts/export_customer_pdfs_outside_codex.py \
  --batch phase-1 \
  --only hvac-contractors \
  --html-pattern "*.html" \
  --output "$OUT" \
  --slow \
  --timeout 120

python3 scripts/validate_customer_pdf_export.py \
  --batch phase-1 \
  --only etsy-sellers hvac-contractors \
  --pdf-pattern "01-ai-playbook-etsy-sellers.pdf" "01-ai-playbook-hvac-contractors.pdf" "02-90day-content-calendar-hvac-month-*.pdf" "03-email-templates-hvac.pdf" "04-brand-kit-hvac.pdf" "05-phone-scripts-hvac.pdf" "lm-hvac-contractors.pdf" \
  --output "$OUT"

python3 scripts/audit_pdf_layout_risk.py \
  --batch phase-1 \
  --only etsy-sellers hvac-contractors \
  --pdf-pattern "01-ai-playbook-etsy-sellers.pdf" "01-ai-playbook-hvac-contractors.pdf" "02-90day-content-calendar-hvac-month-*.pdf" "03-email-templates-hvac.pdf" "04-brand-kit-hvac.pdf" "05-phone-scripts-hvac.pdf" "lm-hvac-contractors.pdf" \
  --output "$OUT"

"$PY" scripts/create_pdf_contact_sheets.py \
  --root "$OUT" \
  --batch phase-1 \
  --only etsy-sellers hvac-contractors \
  --pdf-pattern "01-ai-playbook-etsy-sellers.pdf" "01-ai-playbook-hvac-contractors.pdf" "02-90day-content-calendar-hvac-month-*.pdf" "03-email-templates-hvac.pdf" "04-brand-kit-hvac.pdf" "05-phone-scripts-hvac.pdf" "lm-hvac-contractors.pdf" \
  --max-pages 45

python3 scripts/build_pdf_visual_review_index.py \
  --root "$OUT" \
  --batch phase-1 \
  --title "Phase 1 Risk Export Visual Review"

echo ""
echo "Risk export complete."
echo "Review contact sheets here:"
echo "$OUT/_visual-audit/phase-1"
echo ""
echo "Review dashboard:"
echo "$OUT/phase-1-visual-review-index.html"
