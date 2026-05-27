import Script from "next/script";
import "./globals.css";

const siteUrl = "https://www.contentelevatedhq.com";

export const metadata = {
  metadataBase: new URL(siteUrl),
  title: "Content Elevated | Premium AI Growth Bundles",
  description:
    "Premium AI-powered growth bundles, templates, prompts, content calendars, and business systems for service businesses and creators.",
  keywords: [
    "AI growth bundles",
    "business templates",
    "content calendar",
    "service business marketing",
    "digital products"
  ],
  openGraph: {
    title: "Content Elevated",
    description:
      "High-end AI-powered growth systems for modern businesses and creators.",
    url: siteUrl,
    siteName: "Content Elevated",
    type: "website"
  },
  alternates: {
    canonical: "/"
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1
    }
  },
  icons: {
    icon: "/icon.svg",
    shortcut: "/icon.svg",
    apple: "/icon.svg"
  },
  verification: {
    google: process.env.NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION
  }
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <GoogleAnalytics />
      </body>
    </html>
  );
}

function GoogleAnalytics() {
  const measurementId = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID;

  if (!measurementId) {
    return null;
  }

  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`}
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${measurementId}');
        `}
      </Script>
    </>
  );
}
