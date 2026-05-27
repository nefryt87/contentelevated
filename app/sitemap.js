import { categories, products } from "@/data/site";

const siteUrl = "https://www.contentelevatedhq.com";

export default function sitemap() {
  const now = new Date();

  const staticRoutes = [
    {
      url: siteUrl,
      lastModified: now,
      changeFrequency: "weekly",
      priority: 1
    }
  ];

  const productRoutes = products.map((product) => ({
    url: `${siteUrl}/products/${product.slug}`,
    lastModified: now,
    changeFrequency: "weekly",
    priority: 0.8
  }));

  const categoryRoutes = categories.map((category) => ({
    url: `${siteUrl}/categories/${category.slug}`,
    lastModified: now,
    changeFrequency: "monthly",
    priority: 0.6
  }));

  return [...staticRoutes, ...productRoutes, ...categoryRoutes];
}
