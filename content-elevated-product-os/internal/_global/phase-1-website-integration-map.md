# Phase 1 Website Integration Map

Last updated: 2026-05-19

This maps the Phase 1 launch batch from the internal product operating system to the current storefront data in `data/site.js`.

## Current Matches

| Internal Product | Website Product Title | Website Slug | Current Payhip Link In Website | Status |
|---|---|---|---|---|
| Wedding Photographers Growth Bundle | Wedding Photographer Growth Bundle | `wedding-photographer-growth-bundle` | `https://payhip.com/b/r5HSz` | matched, title differs slightly |
| Nutritionists Growth Bundle | Nutritionist & Dietitian Growth Bundle | `nutritionist-and-dietitian-growth-bundle` | `https://payhip.com/b/xz0Tr` | matched, title differs |
| HVAC Contractors Growth Bundle | HVAC Contractor Growth Bundle | `hvac-contractor-growth-bundle` | `https://payhip.com/b/r9Jay` | matched, title differs slightly |
| Etsy Sellers Growth Bundle | Etsy Seller Growth Bundle | `etsy-seller-growth-bundle` | `https://payhip.com/b/x7D4I` | matched, title differs slightly |
| Dentists Growth Bundle | Dental Practice Growth Bundle | `dental-practice-growth-bundle` | `https://payhip.com/b/RXUZc` | matched, title differs |
| Med Spas Growth Bundle | Med Spa Aesthetician Growth Bundle | `med-spa-aesthetician-growth-bundle` | `https://payhip.com/b/uRbgW` | likely matched, title differs |
| Accountants & CPAs Growth Bundle | Accountant & CPA Growth Bundle | `accountant-and-cpa-growth-bundle` | `https://payhip.com/b/9zcAT` | matched, title differs slightly |

## Missing From Website Data

| Internal Product | Issue | Needed |
|---|---|---|
| Hair Stylists Growth Bundle | No exact Hair Stylist product exists in `data/site.js`; only Bridal Hair & Makeup Artist and Personal Stylist are present. | Confirm Payhip product URL, cover image, final title, and whether this should be added as its own storefront product. |

## Integration Notes

- The internal copy uses consistent pluralized bundle names, while the website currently uses buyer-facing storefront names from Payhip.
- Do not overwrite Payhip links until the final Payhip URLs are confirmed.
- Website product pages currently use generic `description`, `includes`, `fit`, and `outcome` fields generated from `data/site.js`.
- Next website step: enrich Phase 1 product records with the stronger copy from each `website-product-copy.md`, then add Hair Stylists once its Payhip URL and cover are confirmed.

## Recommended Launch Rule

Before a Phase 1 product is marked live:

1. Confirm product title match between Payhip, website, and internal tracker.
2. Confirm Payhip checkout link.
3. Confirm product cover/mockup image is saved locally.
4. Confirm redesigned buyer files are uploaded to Payhip.
5. Confirm website product page copy uses the finalized listing language.
