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
    <main className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_12%_4%,rgba(201,166,94,0.08),transparent_30rem),radial-gradient(circle_at_86%_8%,rgba(130,92,31,0.07),transparent_36rem),linear-gradient(180deg,#050503,#070604_42%,#050503)] px-5 pb-16 pt-6 text-[#f4eee2] sm:px-8">
      <div className="mx-auto max-w-[94rem]">
        <nav className="flex items-center justify-between py-4">
          <Link href="/" className="flex items-center">
            <BrandMark className="h-12 w-52 sm:h-14 sm:w-60" />
          </Link>
          <Link
            href="/#bundles"
            className="inline-flex items-center gap-2 rounded-full border border-[#c9a65e]/10 bg-white/[0.025] px-3.5 py-2 text-xs font-semibold text-[#d8d0c2]/72 transition hover:border-[#c9a65e]/32 hover:text-[#dcc27b] sm:px-4 sm:py-2.5 sm:text-sm"
          >
            <ArrowLeft className="h-4 w-4" />
            Bundles
          </Link>
        </nav>

        <section className="grid gap-9 py-10 sm:py-14 lg:grid-cols-[0.94fr_1.06fr] lg:items-center lg:gap-12">
          <div className="relative">
            <div className="absolute inset-0 rounded-[3rem] bg-[radial-gradient(circle_at_50%_32%,rgba(201,166,94,0.12),transparent_28rem)] blur-[70px] sm:blur-[90px]" />
            <div className="luxe-card premium-edge relative overflow-hidden rounded-[1.35rem] border border-[#c9a65e]/10 bg-[#0b0a08] p-2 shadow-[0_24px_80px_rgba(0,0,0,0.4)] sm:rounded-[2rem] sm:p-3 sm:shadow-[0_50px_140px_rgba(0,0,0,0.5)]">
              <div className="relative aspect-[1.28] overflow-hidden rounded-[1rem] border border-[#c9a65e]/8 bg-[radial-gradient(circle_at_50%_18%,rgba(201,166,94,0.11),transparent_22rem),linear-gradient(180deg,#11100b,#070604)] sm:aspect-[1.42] sm:rounded-[1.45rem]">
                <img
                  src={product.image}
                  alt={`${product.title} product preview`}
                  className="h-full w-full object-contain p-3"
                />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_22%_8%,rgba(245,227,167,0.12),transparent_25%),linear-gradient(180deg,transparent,rgba(5,5,3,0.18))]" />
              </div>
            </div>
          </div>

          <div>
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-[#c9a65e]/16 bg-[#c9a65e]/8 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-[#dcc27b]">
              <Sparkles className="h-4 w-4" />
              {product.category}
            </div>
            <h1 className="editorial-serif max-w-4xl text-[clamp(2.4rem,12vw,3.8rem)] font-normal leading-[0.98] tracking-normal text-[#f4eee2] sm:text-[clamp(2.8rem,4.7vw,5.8rem)] sm:leading-[0.95]">
              {product.title}
            </h1>
            <p className="mt-6 max-w-3xl text-base leading-7 text-[#aaa295] sm:text-lg sm:leading-8">
              {product.description}
            </p>

            <div className="mt-8 grid gap-3 sm:grid-cols-3">
              {[
                ["Price", product.price],
                ["Total value", product.value],
                ["Delivery", "Instant"]
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border border-[#c9a65e]/10 bg-white/[0.018] p-4">
                  <p className="text-xs uppercase tracking-[0.22em] text-[#8f887b]">{label}</p>
                  <p className="editorial-serif mt-2 text-2xl text-[#f4eee2]">{value}</p>
                </div>
              ))}
            </div>

            <PurchasePanel product={product} />
          </div>
        </section>

        <section className="grid gap-4 py-8 sm:gap-5 sm:py-10 lg:grid-cols-[0.85fr_1.15fr]">
          <div className="rounded-[1.35rem] border border-[#c9a65e]/10 bg-[#0b0a08]/70 p-5 shadow-[0_18px_60px_rgba(0,0,0,0.2)] sm:rounded-[2rem] sm:p-9 sm:shadow-[0_24px_90px_rgba(0,0,0,0.22)]">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#b99b63]">Bundle details</p>
            <h2 className="editorial-serif mt-4 text-[1.7rem] leading-tight text-[#f4eee2] sm:text-[2.1rem]">Built as a complete growth system.</h2>
            <p className="mt-5 leading-7 text-[#9e9688]">
              A focused business kit with strategy, prompts, templates, and implementation assets designed to move from idea to execution fast.
            </p>
            <div className="mt-7 rounded-[24px] border border-[#c9a65e]/12 bg-[#c9a65e]/[0.045] p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#b99b63]">Outcome</p>
              <p className="mt-3 leading-7 text-[#d8d0c2]/78">{product.outcome}</p>
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {product.includes.map((item) => (
              <div key={item} className="premium-edge rounded-[1.2rem] border border-[#c9a65e]/10 bg-white/[0.018] p-4 sm:rounded-[24px] sm:p-5">
                <CheckCircle2 className="mb-4 h-5 w-5 text-[#dcc27b]" />
                <p className="font-semibold leading-7 text-[#d8d0c2]">{item}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="grid gap-4 py-8 sm:gap-5 sm:py-10 lg:grid-cols-3">
          <div className="rounded-[1.35rem] border border-[#c9a65e]/10 bg-white/[0.018] p-5 sm:rounded-[28px] sm:p-7 lg:col-span-2">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#b99b63]">Who this is for</p>
            <h2 className="editorial-serif mt-4 text-[1.65rem] leading-tight text-[#f4eee2] sm:text-[2.05rem]">
              Built for operators who want a premium system, not another folder of random templates.
            </h2>
            <div className="mt-7 grid gap-4 sm:grid-cols-3">
              {product.fit.map((item) => (
                <div key={item} className="rounded-[22px] border border-[#c9a65e]/8 bg-black/15 p-5">
                  <BadgeCheck className="mb-4 h-5 w-5 text-[#dcc27b]" />
                  <p className="text-sm font-semibold leading-6 text-[#d8d0c2]/78">{item}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-[1.35rem] border border-[#c9a65e]/10 bg-[#0b0a08]/70 p-5 sm:rounded-[28px] sm:p-7">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#b99b63]">After purchase</p>
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
                  <p className="pt-1 text-sm leading-6 text-[#aaa295]">{text}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="py-12">
          <div className="mb-6 flex items-end justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#b99b63]">Related bundles</p>
              <h2 className="editorial-serif mt-3 text-[1.75rem] leading-tight text-[#f4eee2] sm:text-[2.3rem]">More in {product.category}</h2>
            </div>
            <Link href="/#bundles" className="hidden text-sm font-semibold text-[#dcc27b] sm:inline">
              View catalog
            </Link>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {related.map((item) => (
              <Link
                key={item.slug}
                href={`/products/${item.slug}`}
                className="group rounded-[24px] border border-[#c9a65e]/10 bg-white/[0.018] p-4 transition hover:border-[#c9a65e]/28 hover:bg-white/[0.035]"
              >
                <div className="aspect-[1.55] overflow-hidden rounded-[18px] bg-[radial-gradient(circle_at_50%_20%,rgba(201,166,94,0.08),transparent_18rem),#0b0a08]">
                  <img src={item.image} alt="" className="h-full w-full object-contain p-2 transition group-hover:scale-[1.03]" />
                </div>
                <p className="mt-4 text-xs uppercase tracking-[0.22em] text-[#b99b63]">{item.price}</p>
                <h3 className="editorial-serif mt-2 text-xl leading-tight text-[#f4eee2]">{item.title}</h3>
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
    <div className="mt-8 rounded-[1.35rem] border border-[#c9a65e]/16 bg-[linear-gradient(145deg,rgba(201,166,94,0.12),rgba(255,255,255,0.025))] p-5 shadow-[0_18px_60px_rgba(0,0,0,0.24)] backdrop-blur-xl sm:rounded-[28px] sm:shadow-[0_24px_90px_rgba(0,0,0,0.28)]">
      <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-center">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#b99b63]">Instant access</p>
          <p className="editorial-serif mt-2 text-3xl text-[#f4eee2] sm:text-4xl">{product.price}</p>
        </div>
        <a
          href={product.checkoutUrl}
          target="_blank"
          rel="noreferrer"
          className="gold-button inline-flex items-center justify-center gap-2 rounded-full px-7 py-4 text-sm font-black text-[#080704] transition hover:scale-[1.02]"
        >
          Get the Bundle
          <ArrowRight className="h-4 w-4" />
        </a>
      </div>
      <div className="mt-5 grid gap-3 border-t border-gradient-soft pt-5 sm:grid-cols-3">
        {[
          [ShieldCheck, "Secure Payhip checkout"],
          [Download, "Instant digital delivery"],
          [BadgeCheck, "No physical item shipped"]
        ].map(([Icon, label]) => (
          <div key={label} className="inline-flex items-center gap-2 text-sm text-[#aaa295]">
            <Icon className="h-4 w-4 text-[#dcc27b]" />
            {label}
          </div>
        ))}
      </div>
    </div>
  );
}
