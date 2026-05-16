import "./globals.css";

export const metadata = {
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
    type: "website"
  }
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
