# Website Launch Integrations

Last updated: 2026-05-20

Use this file when setting up or checking the live Content Elevated storefront.

## Kit Newsletter

The website footer posts newsletter signups to:

`/api/newsletter`

Required Vercel environment variables:

```txt
KIT_FORM_ID=
KIT_API_KEY=
KIT_API_VERSION=v4
```

Fallback legacy names are still supported:

```txt
CONVERTKIT_FORM_ID=
CONVERTKIT_API_KEY=
KIT_API_VERSION=v3
```

Recommended setup:

1. In Kit, create a simple newsletter form for Content Elevated.
2. Copy the Kit form ID.
3. Copy a Kit API key from the developer/API settings.
4. Add the variables above in Vercel: Project Settings > Environment Variables.
5. Redeploy the production site.
6. Test the footer form with a personal email before sending traffic.

## Google Search Visibility

Already added in code:

- metadata base: `https://www.contentelevatedhq.com`
- canonical home URL
- `robots.txt`
- `sitemap.xml`
- index/follow metadata

Next setup:

1. Open Google Search Console.
2. Add `https://www.contentelevatedhq.com` as a property.
3. Verify with DNS TXT record or HTML meta verification.
4. If using HTML meta verification, add this Vercel environment variable:

```txt
NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION=
```

5. Redeploy.
6. Submit sitemap:

`https://www.contentelevatedhq.com/sitemap.xml`

## Google Analytics

The website supports Google Analytics 4 through:

```txt
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

Add this in Vercel and redeploy. No code change is needed.

## Current Homepage Change

The repetitive `Inside Every Bundle` section was removed from the homepage because it duplicated the proof/benefit section above it.

## Deploy Check

After any website change:

```zsh
npm run build
```

Then commit and push to GitHub. Vercel should automatically deploy from the connected GitHub repository.
