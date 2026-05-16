import Link from "next/link";
import { notFound } from "next/navigation";
import {
  ArrowLeft,
  ArrowRight,
  BadgeCheck,
  CheckCircle2,
  Download,
  ShieldCheck,
  Sparkles,
  Star
} from "lucide-react";
import BrandMark from "@/components/BrandMark";
import { products } from "@/data/site";

export function generateStaticParams() {
  return products.map((product) => ({ slug: product.slug }));
}

export function generateMetadata({ params }) {
  const product = products.find((item) => item.slug === params.slug);

  if (!product) {
    return {};
  }

  return {
    title: `${product.title} | Content Elevated`,
    description: product.description,
    openGraph: {
      title: `${product.title} | Content Elevated`,
      description: product.description,
      images: [product.image]
    }
  };
}

export default function ProductPage({ params }) {
  const product = products.find((item) => item.slug === params.slug);

  if (!product) {
    notFound();
  }

  const related = products
    .filter((item) => item.category === product.category && item.slug !== product.slug)
    .slice(0, 3);

  return (
    <main className="min-h-screen overflow-hidden px-5 pb-16 pt-6 sm:px-8">
      <div className="mx-auto max-w-7xl">
        <nav className="flex items-center justify-between py-4">
          <Link href="/" className="flex items-center">
            <BrandMark className="h-12 w-44 sm:w-52" />
          </Link>
          <Link
            href="/#collections"
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm font-semibold text-cream/72 transition hover:border-gold/40 hover:text-gold"
          >
            <ArrowLeft className="h-4 w-4" />
            Bundles
          </Link>
        </nav>

        <section className="grid gap-10 py-14 lg:grid-cols-[0.96fr_1.04fr] lg:items-center">
          <div className="relative">
            <div className="absolute inset-0 rounded-[3rem] bg-gold/20 blur-[90px]" />
            <div className="glass relative overflow-hidden rounded-[2.4rem] p-4">
              <div className="relative aspect-[1.42] overflow-hidden rounded-[1.7rem] border border-white/10 bg-ink">
                <img
                  src={product.image}
                  alt={`${product.title} product preview`}
                  className="h-full w-full object-contain p-3"
                />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_10%,rgba(255,255,255,0.18),transparent_26%),linear-gradient(180deg,transparent,rgba(5,7,15,0.12))]" />
              </div>
            </div>
          </div>

          <div>
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
              <Sparkles className="h-4 w-4" />
              {product.category}
            </div>
            <h1 className="text-5xl font-black leading-[0.96] tracking-[-0.03em] text-cream sm:text-6xl">
              {product.title}
            </h1>
            <p className="mt-6 text-lg leading-8 text-cream/68">
              {product.description}
            </p>

            <div className="mt-8 grid gap-3 sm:grid-cols-3">
              {[
                ["Price", product.price],
                ["Total value", product.value],
                ["Delivery", "Instant"]
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border border-white/10 bg-white/[0.04] p-4">
                  <p className="text-xs uppercase tracking-[0.22em] text-cream/42">{label}</p>
                  <p className="mt-2 text-xl font-black text-cream">{value}</p>
                </div>
              ))}
            </div>

            <PurchasePanel product={product} />
          </div>
        </section>

        <section className="grid gap-5 py-10 lg:grid-cols-[0.85fr_1.15fr]">
          <div className="glass rounded-[2rem] p-7 sm:p-9">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Bundle details</p>
            <h2 className="mt-4 text-3xl font-black tracking-[-0.02em] text-cream">Built as a complete growth system.</h2>
            <p className="mt-5 leading-7 text-cream/62">
              A focused business kit with strategy, prompts, templates, and implementation assets designed to move from idea to execution fast.
            </p>
            <div className="mt-7 rounded-[24px] border border-gold/15 bg-gold/[0.07] p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Outcome</p>
              <p className="mt-3 leading-7 text-cream/72">{product.outcome}</p>
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {product.includes.map((item) => (
              <div key={item} className="rounded-[24px] border border-white/10 bg-white/[0.045] p-5">
                <CheckCircle2 className="mb-4 h-5 w-5 text-gold" />
                <p className="font-semibold leading-7 text-cream">{item}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="grid gap-5 py-10 lg:grid-cols-3">
          <div className="rounded-[28px] border border-white/10 bg-white/[0.04] p-7 lg:col-span-2">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Who this is for</p>
            <h2 className="mt-4 text-3xl font-black tracking-[-0.02em] text-cream">
              Built for operators who want a premium system, not another folder of random templates.
            </h2>
            <div className="mt-7 grid gap-4 sm:grid-cols-3">
              {product.fit.map((item) => (
                <div key={item} className="rounded-[22px] border border-white/10 bg-black/16 p-5">
                  <BadgeCheck className="mb-4 h-5 w-5 text-gold" />
                  <p className="text-sm font-semibold leading-6 text-cream/76">{item}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="glass rounded-[28px] p-7">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">After purchase</p>
            <div className="mt-6 space-y-5">
              {[
                ["1", "Checkout securely through Payhip."],
                ["2", "Get instant access to your digital files."],
                ["3", "Open the playbook and start implementing the system."]
              ].map(([step, text]) => (
                <div key={step} className="flex gap-4">
                  <span className="grid h-8 w-8 flex-none place-items-center rounded-full border border-gold/25 bg-gold/10 text-xs font-black text-gold">
                    {step}
                  </span>
                  <p className="pt-1 text-sm leading-6 text-cream/68">{text}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="py-12">
          <div className="mb-6 flex items-end justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Related bundles</p>
              <h2 className="mt-3 text-3xl font-black text-cream">More in {product.category}</h2>
            </div>
            <Link href="/#collections" className="hidden text-sm font-semibold text-gold sm:inline">
              View catalog
            </Link>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            {related.map((item) => (
              <Link
                key={item.slug}
                href={`/products/${item.slug}`}
                className="group rounded-[24px] border border-white/10 bg-white/[0.04] p-4 transition hover:border-gold/35 hover:bg-white/[0.07]"
              >
                <div className="aspect-[1.55] overflow-hidden rounded-[18px] bg-ink">
                  <img src={item.image} alt="" className="h-full w-full object-contain p-2 transition group-hover:scale-[1.03]" />
                </div>
                <p className="mt-4 text-xs uppercase tracking-[0.22em] text-gold/80">{item.price}</p>
                <h3 className="mt-2 text-lg font-bold leading-tight text-cream">{item.title}</h3>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}

function PurchasePanel({ product }) {
  return (
    <div className="mt-8 rounded-[28px] border border-gold/20 bg-[linear-gradient(145deg,rgba(216,170,72,0.12),rgba(255,255,255,0.035))] p-5 shadow-glow backdrop-blur-xl">
      <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-center">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Instant access</p>
          <p className="mt-2 text-3xl font-black text-cream">{product.price}</p>
        </div>
        <a
          href={product.checkoutUrl}
          target="_blank"
          rel="noreferrer"
          className="premium-button inline-flex items-center justify-center gap-2 rounded-full px-7 py-4 text-sm font-black text-ink shadow-glow transition hover:scale-[1.02]"
        >
          Get the Bundle
          <ArrowRight className="h-4 w-4" />
        </a>
      </div>
      <div className="mt-5 grid gap-3 border-t border-white/10 pt-5 sm:grid-cols-3">
        {[
          [ShieldCheck, "Secure Payhip checkout"],
          [Download, "Instant digital delivery"],
          [BadgeCheck, "No physical item shipped"]
        ].map(([Icon, label]) => (
          <div key={label} className="inline-flex items-center gap-2 text-sm text-cream/58">
            <Icon className="h-4 w-4 text-gold" />
            {label}
          </div>
        ))}
      </div>
    </div>
  );
}
