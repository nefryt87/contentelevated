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
    <main className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_12%_4%,rgba(201,166,94,0.08),transparent_30rem),radial-gradient(circle_at_86%_8%,rgba(130,92,31,0.07),transparent_36rem),linear-gradient(180deg,#050503,#070604_42%,#050503)] px-5 pb-16 pt-5 text-[#f4eee2] sm:px-8 sm:pb-20 sm:pt-6">
      <div className="mx-auto max-w-[94rem]">
        <nav className="flex items-center justify-between py-4">
          <Link href="/" className="flex items-center">
            <BrandMark className="h-12 w-52 sm:h-14 sm:w-60" />
          </Link>
          <Link
            href="/#categories"
            className="inline-flex items-center gap-2 rounded-full border border-[#c9a65e]/10 bg-white/[0.025] px-3.5 py-2 text-xs font-semibold text-[#d8d0c2]/72 transition hover:border-[#c9a65e]/32 hover:text-[#dcc27b] sm:px-4 sm:py-2.5 sm:text-sm"
          >
            <ArrowLeft className="h-4 w-4" />
            Categories
          </Link>
        </nav>

        <section className="relative py-11 sm:py-16">
          <div className="absolute left-[-12rem] top-0 hidden h-[28rem] w-[28rem] rounded-full bg-[#c9a65e]/8 blur-[110px] sm:block" />
          <div className="absolute right-[-10rem] top-16 hidden h-[30rem] w-[30rem] rounded-full bg-[#5a3e16]/16 blur-[120px] sm:block" />
          <div className="relative max-w-4xl">
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-[#c9a65e]/16 bg-[#c9a65e]/8 px-3.5 py-2 text-[0.62rem] font-semibold uppercase tracking-[0.16em] text-[#dcc27b] sm:mb-6 sm:px-4 sm:text-xs sm:tracking-[0.2em]">
              <Sparkles className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
              {category.count} curated bundles
            </div>
            <h1 className="editorial-serif text-[clamp(2.35rem,12vw,3.75rem)] font-normal leading-[0.96] tracking-normal text-[#f4eee2] sm:text-[clamp(3rem,5.2vw,6rem)] sm:leading-[0.95]">
              {category.title} Growth Bundles
            </h1>
            <p className="mt-5 max-w-2xl text-sm leading-6 text-[#aaa295] sm:mt-6 sm:text-lg sm:leading-8">
              {category.text} Browse every Content Elevated system built for this niche and open the bundle details before checkout.
            </p>
          </div>
        </section>

        <section className="grid gap-4 sm:grid-cols-2 sm:gap-5 xl:grid-cols-4">
          {categoryProducts.map((product, index) => (
            <ProductCard key={product.slug} product={product} index={index} />
          ))}
        </section>
      </div>
    </main>
  );
}
