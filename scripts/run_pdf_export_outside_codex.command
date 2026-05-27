#!/bin/zsh
set -e

cd "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for"

echo "Content Elevated PDF Export"
echo "Choose a batch:"
echo "1) Phase 1 launch batch"
echo "2) Next approved batch"
echo "3) Standard queue"
echo "4) All batches"
echo ""
read "choice?Enter 1, 2, 3, or 4: "

case "$choice" in
  1) batch="phase-1" ;;
  2) batch="next" ;;
  3) batch="standard" ;;
  4) batch="all" ;;
  *) echo "Invalid choice."; exit 1 ;;
esac

/usr/bin/python3 scripts/export_customer_pdfs_outside_codex.py --batch "$batch" --slow --timeout 45

echo ""
echo "Done. Open this folder:"
echo "/Users/tomasz/Documents/Codex/2026-05-15/can-you-build-a-website-for/content-elevated-product-os/exports/customer-pdf-export"
