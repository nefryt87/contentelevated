# Payhip + Website Upload Workflow

Use this every time a product is prepared for sale.

## Before Upload

- Confirm product folder exists in `rebranded-products-sample-direction`.
- Confirm all HTML files open and are readable.
- Confirm spreadsheets are included if the bundle promises spreadsheets.
- Confirm product files do not contain internal production language.
- Confirm price.
- Confirm final Payhip product title.

## Payhip Listing

Store URL: `https://payhip.com/ContentElevated`

The products are already listed on Payhip as bundles, but many current listings use the original/basic PDFs. For redesigned products, update the existing Payhip listing first instead of creating duplicates.

Create or update:

- Product title
- Short description
- Full description
- Preview images/mockups
- Product files
- Price
- Tags/categories
- Refund/digital delivery note
- Cover image/product mockup

After publishing, add the Payhip product URL to:

- `content-elevated-product-os/data/product-master.csv`
- Website product data file

## Website Product Page

Update:

- Product title
- Short description
- Long description
- What's included
- Category
- Product image
- Payhip checkout URL
- SEO title
- SEO description

## Cover Images

- Download/export Payhip cover images and save them locally in `content-elevated-product-os/assets/product-covers/`.
- Use product-slug filenames.
- If a cover is redesigned, replace both the local version and Payhip version.
- Website product images should use the approved local cover whenever possible.

## Future Single Products

When splitting bundle components into individual products:

- Create a row in `data/single-product-roadmap.csv`.
- Create Payhip listing copy.
- Create website product copy.
- Create/export cover image.
- Set Payhip URL after publishing.
- Link the single product from the parent bundle page when useful.

## Final Check

- Product page opens on website.
- "Get the Bundle" opens Payhip checkout.
- Payhip delivery includes the correct files.
- Product tracker status is updated.
- Local cover image exists.
