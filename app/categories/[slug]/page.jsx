import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, Sparkles } from "lucide-react";
import BrandMark from "@/components/BrandMark";
import ProductCard from "@/components/ProductCard";
import { categories, categorySlug, products } from "@/data/site";

export function generateStaticParams() {
  return categories.map((category) => ({ slug: category.slug }));
}

export function generateMetadata({ params }) {
  const category = categories.find((item) => item.slug === params.slug);

  if (!category) {
    return {};
  }

  return {
    title: `${category.title} Growth Bundles | Content Elevated`,
    description: category.text
  };
}

export default function CategoryPage({ params }) {
  const category = categories.find((item) => item.slug === params.slug);

  if (!category) {
    notFound();
  }

  const categoryProducts = products.filter(
    (product) => categorySlug(product.category) === category.slug
  );

  return (
    <main className="min-h-screen overflow-hidden px-5 pb-20 pt-6 sm:px-8">
      <div className="mx-auto max-w-7xl">
        <nav className="flex items-center justify-between py-4">
          <Link href="/" className="flex items-center">
            <BrandMark className="h-12 w-44 sm:w-52" />
          </Link>
          <Link
            href="/#categories"
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm font-semibold text-cream/72 transition hover:border-gold/40 hover:text-gold"
          >
            <ArrowLeft className="h-4 w-4" />
            Categories
          </Link>
        </nav>

        <section className="relative py-16">
          <div className="absolute left-[-12rem] top-0 h-[28rem] w-[28rem] rounded-full bg-blueglow/14 blur-[110px]" />
          <div className="absolute right-[-10rem] top-16 h-[30rem] w-[30rem] rounded-full bg-gold/16 blur-[120px]" />
          <div className="relative max-w-4xl">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
              <Sparkles className="h-4 w-4" />
              {category.count} curated bundles
            </div>
            <h1 className="text-5xl font-black leading-[0.96] tracking-[-0.03em] text-cream sm:text-7xl">
              {category.title} Growth Bundles
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-cream/68">
              {category.text} Browse every Content Elevated system built for this niche and open the bundle details before checkout.
            </p>
          </div>
        </section>

        <section className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {categoryProducts.map((product, index) => (
            <ProductCard key={product.slug} product={product} index={index} />
          ))}
        </section>
      </div>
    </main>
  );
}
