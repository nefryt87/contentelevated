"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import {
  ArrowRight,
  BrainCircuit,
  CalendarDays,
  Menu,
  Minus,
  Palette,
  Plus,
  Star,
  Users
} from "lucide-react";
import BrandMark from "@/components/BrandMark";
import { categories, products } from "@/data/site";

const byTitle = (name) => products.find((product) => product.title === name);

const heroProduct =
  byTitle("Bridal Hair & Makeup Artist Growth Bundle") ||
  byTitle("Makeup Artist Growth Bundle") ||
  products[0];

const showcaseProducts = [
  byTitle("Bridal Hair & Makeup Artist Growth Bundle"),
  byTitle("Makeup Artist Growth Bundle"),
  byTitle("Med Spa Aesthetician Growth Bundle"),
  byTitle("Nail Technician Growth Bundle"),
  byTitle("Personal Trainer Growth Bundle"),
  byTitle("Barber Growth Bundle")
].filter(Boolean);

const insideItems = [
  [CalendarDays, "90-day calendar", "A full season of posts, hooks, themes, and weekly campaign direction."],
  [BrainCircuit, "AI playbook + prompts", "Niche-ready prompts for captions, scripts, emails, offers, ads, and client experience."],
  [Users, "Client systems", "Onboarding, follow-up, retention, review, and referral assets that compound."],
  [Palette, "Brand kit + Canva", "Editable templates, visual direction, and positioning assets built to look premium fast."]
];

const processSteps = [
  ["01", "Choose your bundle", "Pick the niche that matches your craft and open a system built for the way that business actually grows."],
  ["02", "Plug in & brand", "Swap in your colors, paste prompts into your AI tool of choice, and use the templates as your operating plan."],
  ["03", "Launch & book", "Post your 90-day calendar, send the rebooking emails, follow up better, and move with polish."]
];

const testimonials = [
  ["Brielle Tanaka", "Nail studio owner · Austin", "I went from 6 fills a week to a 3-week waitlist. The 90-day calendar alone is worth ten times what I paid.", "bg-[#9a7b3c]"],
  ["Marisol Vega", "Bridal MUA · Miami", "It is a brand-in-a-box. The Canva files alone made my Instagram look like I hired an agency.", "bg-[#a15a67]"],
  ["Devon Marsh", "Personal trainer · Brooklyn", "The AI playbook is the unfair advantage. I write a week of content in 30 minutes, and it actually sounds like me.", "bg-[#3d765b]"],
  ["Sasha Renaud", "Med spa founder · Scottsdale", "Two weekends with Content Elevated and the consult-to-client rate jumped to 78%.", "bg-[#d8d3bf]"],
  ["Jordan Pak", "Stylist · Los Angeles", "The retention kit helped me stop losing clients quietly. Within a month, rebooking felt automatic.", "bg-[#b58a32]"]
];

const faqs = [
  ["Do I need any tech or design experience?", "No. The bundles are built to be edited and used by busy operators. You can customize the included templates, prompts, and systems without being a designer."],
  ["How fast do I get access?", "Immediately after checkout through Payhip. You will be redirected to secure delivery and can start downloading the files right away."],
  ["Can I use this for multiple businesses or locations?", "Each purchase is intended for one business brand. If you want to use assets across multiple locations or client brands, contact us for a broader license."],
  ["What is inside a bundle?", "Each niche bundle includes a 90-day content calendar, AI prompt library, client communication templates, brand direction, Canva-ready guidance, and growth systems for that business type."],
  ["Is there a refund policy?", "Because these are instant digital downloads, purchases are generally final. If there is a file access issue, we will help get it resolved."],
  ["Do you offer custom or done-with-you work?", "Custom work is limited, but the storefront will continue expanding with more niches, vault options, and premium growth systems."]
];

const statItems = [
  ["34+", "niche systems"],
  ["AI", "playbook + prompts"],
  ["Brand", "kit included"],
  ["90 day", "content calendar"],
  ["Instant", "download access"]
];

const heroImage = "/brand/hero-4.png";

const heroReveal = {
  hidden: { opacity: 0, y: 18, filter: "blur(10px)" },
  visible: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: { duration: 0.72, ease: [0.22, 1, 0.36, 1] }
  }
};

const heroImageReveal = {
  hidden: { opacity: 0, y: 18, scale: 0.975, filter: "blur(12px)" },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    filter: "blur(0px)",
    transition: { duration: 0.95, delay: 0.28, ease: [0.22, 1, 0.36, 1] }
  }
};

export default function Home() {
  return (
    <main className="relative overflow-hidden bg-[radial-gradient(circle_at_10%_16%,rgba(107,124,255,0.045),transparent_34rem),radial-gradient(circle_at_88%_8%,rgba(26,48,88,0.16),transparent_38rem),linear-gradient(180deg,rgba(5,7,11,0.76),rgba(5,7,11,0.94)_38%,rgba(5,7,11,0.98))] text-[#f7f8fb]">
      <Navbar />
      <Hero />
      <Method />
      <InsideBundle />
      <BundleShowcase />
      <Process />
      <CategoryShowcase />
      <Results />
      <FAQ />
      <FinalCTA />
      <Footer />
    </main>
  );
}

function Navbar() {
  const [open, setOpen] = useState(false);
  const links = [
    ["Bundles", "#bundles"],
    ["How it works", "#process"],
    ["Results", "#results"],
    ["FAQ", "#faq"]
  ];

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-[#6f7a89]/10 bg-[#05070b]/78 backdrop-blur-2xl">
      <nav className="mx-auto flex max-w-[94rem] items-center justify-between px-5 py-4 sm:px-8">
        <a href="#" className="flex items-center">
          <BrandMark className="h-12 w-52 sm:h-14 sm:w-60" />
        </a>
        <div className="hidden items-center gap-10 text-xs font-bold uppercase tracking-[0.18em] text-[#c9d0da]/64 lg:flex">
          {links.map(([label, href]) => (
            <a key={href} href={href} className="transition duration-300 hover:text-[#b8f3ff]">{label}</a>
          ))}
        </div>
        <a href="#bundles" className="gold-button hidden rounded-full px-8 py-3 text-xs font-black uppercase tracking-[0.22em] text-[#06101a] transition duration-300 hover:scale-[1.02] sm:inline-flex">
          Shop Bundles
        </a>
        <button
          aria-label="Open navigation"
          onClick={() => setOpen((value) => !value)}
          className="grid h-11 w-11 place-items-center rounded-full border border-[#6f7a89]/10 bg-white/[0.03] lg:hidden"
        >
          <Menu className="h-5 w-5" />
        </button>
      </nav>
      {open ? (
        <div className="mx-5 mb-4 rounded-3xl border border-[#6f7a89]/8 bg-[#080b10] p-3 lg:hidden">
          {links.map(([label, href]) => (
            <a key={href} href={href} onClick={() => setOpen(false)} className="block rounded-2xl px-4 py-3 text-sm font-semibold text-[#c9d0da]/72">
              {label}
            </a>
          ))}
        </div>
      ) : null}
    </header>
  );
}

function Eyebrow({ children, centered = false }) {
  return (
    <p className={`mb-5 flex items-center gap-3 text-[0.58rem] font-bold uppercase tracking-[0.24em] text-[#8bd7ff] sm:mb-6 sm:gap-4 sm:text-[0.68rem] sm:tracking-[0.36em] ${centered ? "justify-center" : ""}`}>
      <span className="h-px w-7 bg-[#8bd7ff] sm:w-10" />
      {children}
      {centered ? <span className="h-px w-7 bg-[#8bd7ff] sm:w-10" /> : null}
    </p>
  );
}

function Hero() {
  return (
    <section className="relative px-5 pb-6 pt-24 sm:min-h-[88vh] sm:px-8 sm:pt-28 lg:pb-8 lg:pt-32">
      <motion.div
        aria-hidden="true"
        animate={{ opacity: [0.52, 0.78, 0.52], scale: [1, 1.06, 1] }}
        transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
        className="absolute inset-0 hidden bg-[radial-gradient(circle_at_15%_28%,rgba(107,124,255,0.12),transparent_27rem),radial-gradient(circle_at_78%_32%,rgba(108,238,255,0.08),transparent_34rem)] sm:block"
      />
      <motion.div
        className="relative mx-auto grid max-w-[92rem] items-center gap-9 lg:grid-cols-[0.96fr_1.04fr] xl:gap-16"
        initial="hidden"
        animate="visible"
        variants={{ visible: { transition: { staggerChildren: 0.12, delayChildren: 0.08 } } }}
      >
        <div>
          <motion.div variants={heroReveal}>
            <Eyebrow>Premium · AI-Powered · Done-For-You</Eyebrow>
          </motion.div>
          <motion.h1 variants={heroReveal} className="editorial-serif max-w-4xl text-[clamp(2.55rem,14vw,4.25rem)] font-normal leading-[0.94] tracking-normal sm:text-[clamp(3.05rem,5.7vw,6.35rem)] sm:leading-[0.92]">
            Elevate your brand. <span className="gold-text">Elevate</span> your income.
          </motion.h1>
          <motion.p variants={heroReveal} className="mt-6 max-w-2xl text-base leading-7 text-[#aeb7c3] sm:mt-7 sm:text-xl sm:leading-9">
            Premium growth bundles for service businesses and creators, engineered like a studio-grade growth system and delivered like an instant download.
          </motion.p>
          <motion.div variants={heroReveal} className="mt-8 flex flex-col gap-3 sm:mt-9 sm:flex-row sm:gap-4">
            <a href="#bundles" className="gold-button inline-flex items-center justify-center gap-4 rounded-full px-7 py-4 text-[0.68rem] font-black uppercase tracking-[0.18em] text-[#06101a] transition duration-300 hover:scale-[1.02] sm:px-8 sm:text-xs sm:tracking-[0.22em]">
              Explore the bundles <ArrowRight className="h-4 w-4" />
            </a>
            <a href="#process" className="inline-flex items-center justify-center rounded-full border border-white/8 px-7 py-4 text-[0.68rem] font-black uppercase tracking-[0.18em] text-[#f4f7fb] transition duration-300 hover:border-[#6f7a89]/50 hover:bg-white/[0.03] sm:px-8 sm:text-xs sm:tracking-[0.22em]">
              How it works
            </a>
          </motion.div>
          <motion.div variants={heroReveal} className="mt-8 flex items-center gap-4 sm:mt-10 sm:gap-5">
            <div className="flex -space-x-3">
              {["bg-[#a78b4c]", "bg-[#c6929f]", "bg-[#d8d3bf]", "bg-[#3d765b]"].map((color) => (
                <span key={color} className={`h-10 w-10 rounded-full border-2 border-[#05070b] ${color}`} />
              ))}
            </div>
            <div>
              <div className="mb-1 flex text-[#b8f3ff]">
                {Array.from({ length: 5 }).map((_, index) => <Star key={index} className="h-4 w-4 fill-current" />)}
              </div>
              <p className="text-sm text-[#aeb7c3]">Trusted by modern service brands</p>
            </div>
          </motion.div>
        </div>

        <motion.div variants={heroImageReveal} className="relative">
          <motion.div
            aria-hidden="true"
            animate={{ opacity: [0.35, 0.62, 0.35], y: [0, -10, 0] }}
            transition={{ duration: 9, repeat: Infinity, ease: "easeInOut" }}
            className="hidden absolute -inset-8 rounded-[2.8rem] bg-[radial-gradient(circle_at_50%_30%,rgba(108,238,255,0.14),transparent_34rem)] blur-xl sm:block"
          />
          <motion.a
            href="#bundles"
            whileHover={{ y: -4, rotateX: 0.6, rotateY: -0.6 }}
            transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
            className="luxe-card group relative block overflow-hidden rounded-[1.35rem] border border-[#6f7a89]/10 bg-[#10141b] shadow-[0_26px_80px_rgba(0,0,0,0.42)] sm:rounded-[2rem] sm:shadow-[0_50px_140px_rgba(0,0,0,0.55)]"
          >
            <div className="luxe-sheen z-20" />
            <div className="absolute -inset-10 rounded-[3rem] border border-[#6f7a89]/10" />
            <img src={heroImage} alt="" className="relative aspect-[1.04] w-full object-cover transition duration-700 group-hover:scale-[1.012] sm:group-hover:scale-[1.025]" />
            <div className="absolute left-4 top-4 rounded-full border border-[#6f7a89]/8 bg-[#090d12]/78 px-3 py-2 text-xs text-[#f7f8fb] backdrop-blur-xl sm:left-5 sm:top-8 sm:px-4 sm:py-3 sm:text-sm">
              <span className="mr-2 text-[#b8f3ff]">★</span> Designed for growth
            </div>
            <div className="absolute bottom-4 right-4 rounded-full border border-[#6f7a89]/10 bg-[#090d12]/84 px-4 py-2 text-xs text-[#c9d0da] backdrop-blur-xl sm:bottom-6 sm:right-6 sm:px-5 sm:py-3 sm:text-sm">
              Secure checkout · Instant delivery
            </div>
          </motion.a>
          <div className="mx-auto mt-4 grid max-w-2xl grid-cols-2 overflow-hidden rounded-[1rem] border border-[#6f7a89]/8 bg-[#080b10]/40 sm:mt-5 sm:rounded-[1.25rem] md:grid-cols-5">
            {statItems.map(([value, label]) => (
              <div key={label} className="border-l border-t border-[#6f7a89]/8 px-3 py-4 first:border-l-0 md:border-t-0 md:first:border-l-0">
                <p className="editorial-serif gold-text text-[1.08rem] leading-none sm:text-[1.65rem]">{value}</p>
                <p className="mt-2 text-[0.5rem] font-bold uppercase tracking-[0.16em] text-[#737f8f] sm:text-[0.55rem] sm:tracking-[0.2em]">{label}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
}

function Method() {
  return (
    <Section id="method" compactTop>
      <div className="grid gap-14 lg:grid-cols-[0.92fr_1.08fr] lg:items-end">
        <div>
          <Eyebrow>The Method</Eyebrow>
          <h2 className="editorial-serif text-[clamp(2.55rem,4.15vw,4.75rem)] leading-[0.98]">
            Built like a <span className="gold-text">studio-grade</span> growth system. Ready on download.
          </h2>
        </div>
        <p className="max-w-3xl text-base leading-7 text-[#9aa6b5] xl:text-[1.05rem] xl:leading-8">
          Every bundle is a complete operating system: calendar, content, scripts, brand kit, AI prompts, and client systems engineered to make a one-person business look and earn like a full studio.
        </p>
      </div>
      <div className="mt-14 overflow-hidden rounded-[1.6rem] border border-[#6f7a89]/10 bg-[#070a0f]/50">
        <div className="grid lg:grid-cols-4">
          {insideItems.map(([Icon, title, text], index) => (
            <motion.article
              key={title}
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-90px" }}
              transition={{ duration: 0.52, delay: index * 0.06, ease: [0.22, 1, 0.36, 1] }}
              className="transition duration-500 border-b border-[#6f7a89]/8 p-6 hover:bg-white/[0.025] lg:border-b-0 lg:border-l lg:first:border-l-0"
            >
              <div className="mb-7 grid h-11 w-11 place-items-center rounded-full border border-[#6f7a89]/10 text-[#b8f3ff]">
                <Icon className="h-5 w-5" />
              </div>
              <h3 className="editorial-serif text-[1.45rem]">{title}</h3>
              <p className="mt-3 text-sm leading-6 text-[#8f9baa]">{text}</p>
            </motion.article>
          ))}
        </div>
      </div>
    </Section>
  );
}

function InsideBundle() {
  const list = [
    ["01", "90-day content calendar", "Daily prompts, themes, captions, and hooks tuned to your niche."],
    ["02", "AI playbook + prompts", "Niche-trained prompts for captions, scripts, emails, offers, and ads."],
    ["03", "Client systems pack", "Intake forms, consult scripts, follow-ups, rebooking sequences."],
    ["04", "Editable brand kit + Canva", "Palette, type direction, post templates, story templates, and business cards."],
    ["05", "Profit & pricing calculators", "Plug-in spreadsheets to price services and project monthly revenue."]
  ];

  return (
    <Section id="inside">
      <div className="grid items-center gap-10 lg:grid-cols-[0.92fr_1.08fr] lg:gap-16">
        <div>
          <Eyebrow>Inside Every Bundle</Eyebrow>
          <h2 className="editorial-serif text-[clamp(2.2rem,12vw,3.3rem)] leading-[1] sm:text-[clamp(2.55rem,4.35vw,5rem)] sm:leading-[0.98]">
            A complete <span className="gold-text">operating system</span> for your business.
          </h2>
          <div className="mt-10 space-y-6">
            {list.map(([number, title, text]) => (
              <div key={title} className="group flex gap-5 rounded-2xl p-2 transition duration-300 hover:bg-white/[0.025]">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full border border-[#6f7a89]/10 text-sm text-[#b8f3ff]">{number}</span>
                <div>
                  <h3 className="text-xl font-bold">{title}</h3>
                  <p className="mt-1 text-base leading-7 text-[#8f9baa]">{text}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 sm:gap-6">
          {showcaseProducts.slice(1, 5).map((product, index) => (
            <a key={product.slug} href={`/products/${product.slug}`} className={`luxe-card premium-edge group relative block overflow-hidden rounded-[1.25rem] border border-[#6f7a89]/8 bg-[#10141b] shadow-[0_20px_60px_rgba(0,0,0,0.3)] transition duration-500 hover:-translate-y-1 sm:rounded-[1.5rem] sm:hover:-translate-y-2 ${index % 2 ? "sm:mt-10" : ""}`}>
              <div className="luxe-sheen z-10" />
              <img src={product.image} alt="" className="aspect-[1.18] w-full object-contain p-2 transition duration-700 group-hover:scale-[1.035]" />
            </a>
          ))}
        </div>
      </div>
    </Section>
  );
}

function BundleShowcase() {
  const [activeCategory, setActiveCategory] = useState("Featured");
  const categoryOptions = ["Featured", ...categories.map((category) => category.title)];
  const visibleProducts =
    activeCategory === "Featured"
      ? showcaseProducts
      : products.filter((product) => product.category === activeCategory).slice(0, 6);

  return (
    <Section id="bundles">
      <div className="mb-8 grid gap-6 lg:mb-10 lg:grid-cols-[1fr_0.72fr] lg:items-end lg:gap-8">
        <div>
          <Eyebrow>The Bundles · 34 Niches</Eyebrow>
          <h2 className="editorial-serif text-[clamp(2.1rem,11vw,3.2rem)] leading-[1] sm:text-[clamp(2.25rem,3.6vw,4.15rem)]">
            Pick your <span className="gold-text">craft.</span> We built the rest.
          </h2>
        </div>
        <p className="text-base leading-7 text-[#9aa6b5] lg:pb-2 lg:text-right">
          Every bundle ships as instant-download files: PDFs, editable Canva templates, prompt libraries, and ready-to-use forms.
        </p>
      </div>
      <div className="mb-8 flex gap-2 overflow-x-auto pb-3 scrollbar-hidden sm:mb-10">
        {categoryOptions.map((option) => {
          const selected = activeCategory === option;

          return (
            <button
              key={option}
              type="button"
              onClick={() => setActiveCategory(option)}
              className={`shrink-0 rounded-full border px-3.5 py-2 text-[0.6rem] font-bold uppercase tracking-[0.14em] transition duration-300 sm:px-4 sm:text-[0.66rem] sm:tracking-[0.18em] ${
                selected
                  ? "border-[#b8f3ff]/50 bg-[linear-gradient(135deg,#dcecff,#8bd7ff_44%,#19314a)] text-[#06101a] shadow-[0_16px_36px_rgba(255,106,61,0.14)]"
                  : "border-[#6f7a89]/10 bg-white/[0.012] text-[#9aa6b5] hover:border-[#6f7a89]/28 hover:text-[#f7f8fb]"
              }`}
            >
              {option}
            </button>
          );
        })}
      </div>
      <motion.div
        key={activeCategory}
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
        className="grid gap-4 md:grid-cols-2 xl:grid-cols-4 xl:gap-5"
      >
        {visibleProducts.map((product, index) => <BundleCard key={product.slug} product={product} index={index} />)}
      </motion.div>
    </Section>
  );
}

function BundleCard({ product, index = 0 }) {
  const niche = product.title.replace(" Growth Bundle", "").replace("Complete ", "");
  return (
    <motion.a
      href={`/products/${product.slug}`}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5, rotateX: 0.7, rotateY: -0.7 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.48, delay: index * 0.035, ease: [0.22, 1, 0.36, 1] }}
      className="luxe-card premium-edge group relative overflow-hidden rounded-[1.25rem] border border-[#6f7a89]/10 bg-[#0b0f14] shadow-[0_18px_58px_rgba(0,0,0,0.22)] sm:rounded-[1.5rem] sm:shadow-[0_22px_80px_rgba(0,0,0,0.24)]"
    >
      <div className="luxe-sheen z-20" />
      <div className="relative overflow-hidden bg-[#10141b]">
        <img src={product.image} alt="" className="aspect-[1.18] w-full object-contain p-2 transition duration-700 group-hover:scale-[1.015] sm:group-hover:scale-[1.045]" />
        <div className="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-[#0b0f14] to-transparent opacity-70" />
      </div>
      <div className="p-5 sm:p-6">
        <div className="mb-6 flex items-center justify-between">
          <p className="text-[0.58rem] font-bold uppercase tracking-[0.28em] text-[#8bd7ff]">For {niche}s</p>
          <p className="editorial-serif text-xl text-[#f7f8fb]">{product.price.replace(".00", "")}</p>
        </div>
        <h3 className="editorial-serif text-[1.4rem] leading-[1.13] sm:text-[1.55rem]">{product.title.replace(" Growth Bundle", " Growth Bundle")}</h3>
        <p className="mt-4 text-sm leading-6 text-[#8f9baa]">{product.description}</p>
        <div className="mt-7 flex items-center justify-between border-t border-gradient-soft pt-5 text-[0.68rem] font-bold uppercase tracking-[0.18em] text-[#b8f3ff] sm:mt-8 sm:text-xs sm:tracking-[0.24em]">
          View Bundle <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
        </div>
      </div>
    </motion.a>
  );
}

function Process() {
  return (
    <Section id="process">
      <div className="mx-auto max-w-5xl text-center">
        <Eyebrow centered>The Process</Eyebrow>
        <h2 className="editorial-serif text-[clamp(2.55rem,4.15vw,4.85rem)] leading-[0.98]">
          Launch your new brand <span className="gold-text">this weekend.</span>
        </h2>
        <p className="mx-auto mt-7 max-w-3xl text-lg leading-8 text-[#9aa6b5] xl:text-xl xl:leading-9">
          No agency calls. No course to finish. No blank page. Just plug in, swap your colors, and start booking.
        </p>
      </div>
      <div className="relative mt-14 grid gap-10 lg:mt-20 lg:grid-cols-3 lg:gap-12">
        <div className="absolute left-0 right-0 top-9 hidden border-t border-dashed border-[#6f7a89]/8 lg:block" />
        {processSteps.map(([number, title, text]) => (
          <article key={title} className="relative text-center">
            <div className="mx-auto grid h-14 w-14 place-items-center rounded-full border border-[#6f7a89]/10 bg-[#05070b] editorial-serif text-xl text-[#b8f3ff] sm:h-[4.5rem] sm:w-[4.5rem] sm:text-2xl">{number}</div>
            <h3 className="editorial-serif mt-6 text-[1.55rem] sm:mt-9 sm:text-[1.75rem]">{title}</h3>
            <p className="mx-auto mt-4 max-w-sm text-sm leading-6 text-[#8f9baa] sm:mt-5 sm:text-base sm:leading-7">{text}</p>
          </article>
        ))}
      </div>
    </Section>
  );
}

function CategoryShowcase() {
  return (
    <Section id="categories">
      <div className="mb-14 grid gap-8 lg:grid-cols-[0.9fr_1fr] lg:items-end">
        <div>
          <Eyebrow>Choose Your World</Eyebrow>
          <h2 className="editorial-serif text-[clamp(2.2rem,12vw,3.3rem)] leading-[1] sm:text-[clamp(2.55rem,4.15vw,4.75rem)] sm:leading-[0.98]">
            Find the system built for your market.
          </h2>
        </div>
        <p className="text-base leading-7 text-[#9aa6b5] lg:text-right lg:text-lg lg:leading-8">
          Skip the generic advice and go straight to the bundles that match how your customers buy.
        </p>
      </div>
      <div className="grid gap-px overflow-hidden rounded-[1.25rem] border border-[#6f7a89]/10 bg-[#6f7a89]/10 md:grid-cols-2 lg:grid-cols-4 lg:rounded-[1.6rem]">
        {categories.map((category, index) => (
          <motion.a
            key={category.slug}
            href={`/categories/${category.slug}`}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            whileHover={{ y: -2 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.44, delay: index * 0.035, ease: [0.22, 1, 0.36, 1] }}
            className="group min-h-[12rem] bg-[#05070b] p-5 transition duration-500 hover:bg-[#10141b] sm:p-7 lg:min-h-[14rem]"
          >
            <div className="mb-8 flex items-center justify-between">
              <span className="editorial-serif text-[1.45rem] text-[#8bd7ff] sm:text-[1.75rem]">0{index + 1}</span>
              <span className="text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#8bd7ff] sm:text-xs sm:tracking-[0.22em]">{category.count} bundles</span>
            </div>
            <h3 className="editorial-serif text-[1.5rem] sm:text-[1.75rem]">{category.title}</h3>
            <p className="mt-4 text-sm leading-6 text-[#8f9baa]">{category.text}</p>
            <ArrowRight className="mt-8 h-4 w-4 text-[#b8f3ff] transition group-hover:translate-x-1" />
          </motion.a>
        ))}
      </div>
    </Section>
  );
}

function Results() {
  return (
    <Section id="results">
      <div className="mb-14 flex flex-col justify-between gap-8 lg:flex-row lg:items-end">
        <div>
          <Eyebrow>The Results</Eyebrow>
          <h2 className="editorial-serif text-[clamp(2.1rem,11vw,3.2rem)] leading-[1] sm:text-[clamp(2.25rem,3.6vw,4.15rem)]">
            Pros are <span className="gold-text">obsessed.</span>
          </h2>
        </div>
        <div className="flex items-center gap-4 text-[#9aa6b5]">
          <span className="flex text-[#b8f3ff]">{Array.from({ length: 5 }).map((_, i) => <Star key={i} className="h-5 w-5 fill-current" />)}</span>
          <span>4.9 avg · verified buyers</span>
        </div>
      </div>
      <div className="grid gap-4 lg:grid-cols-3 lg:gap-6">
        {testimonials.map(([name, role, quote, color], index) => (
          <motion.article
            key={name}
            initial={{ opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            whileHover={{ y: -3 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.44, delay: index * 0.05, ease: [0.22, 1, 0.36, 1] }}
            className={index === 3 ? "premium-edge rounded-[1.25rem] border border-[#6f7a89]/10 bg-[#0b0f14] p-5 transition-colors hover:bg-[#111722] sm:rounded-[1.5rem] sm:p-6 lg:col-span-2" : "premium-edge rounded-[1.25rem] border border-[#6f7a89]/10 bg-[#0b0f14] p-5 transition-colors hover:bg-[#111722] sm:rounded-[1.5rem] sm:p-6"}
          >
            <p className="editorial-serif text-[2rem] leading-none text-[#b8f3ff]">"</p>
            <p className="mt-4 text-base leading-7 text-[#c9d0da]">{quote}</p>
            <div className="mt-8 border-t border-gradient-soft pt-6 flex items-center gap-4">
              <span className={`h-10 w-10 rounded-full ${color}`} />
              <div>
                <p className="text-sm font-semibold">{name}</p>
                <p className="text-xs text-[#737f8f]">{role}</p>
              </div>
            </div>
          </motion.article>
        ))}
      </div>
    </Section>
  );
}

function FAQ() {
  const [open, setOpen] = useState(0);

  return (
    <Section id="faq">
      <div className="mx-auto max-w-5xl text-center">
        <Eyebrow centered>Frequently Asked</Eyebrow>
        <h2 className="editorial-serif text-[clamp(2.1rem,11vw,3.2rem)] leading-[1] sm:text-[clamp(2.25rem,3.6vw,4.15rem)]">
          Questions? <span className="gold-text">Answers.</span>
        </h2>
      </div>
      <div className="mx-auto mt-9 max-w-7xl border-t border-gradient-soft">
        {faqs.map(([question, answer], index) => (
          <button
            key={question}
            onClick={() => setOpen(open === index ? -1 : index)}
            className="w-full border-b border-gradient-soft py-5 text-left transition hover:bg-white/[0.018]"
          >
            <span className="flex items-center justify-between gap-6">
              <span className="editorial-serif text-[clamp(1.04rem,1.3vw,1.3rem)] text-[#f7f8fb]">{question}</span>
              {open === index ? <Minus className="h-5 w-5 text-[#b8f3ff]" /> : <Plus className="h-5 w-5 text-[#b8f3ff]" />}
            </span>
            {open === index ? <span className="mt-4 block max-w-3xl text-sm leading-6 text-[#8f9baa]">{answer}</span> : null}
          </button>
        ))}
      </div>
    </Section>
  );
}

function FinalCTA() {
  return (
    <section className="relative border-y border-[#6f7a89]/8 px-5 py-16 text-center sm:px-8 sm:py-24">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(107,124,255,0.12),transparent_34rem)]" />
      <div className="relative mx-auto max-w-5xl">
        <Eyebrow centered>Your Move</Eyebrow>
        <h2 className="editorial-serif text-[clamp(2.35rem,12vw,3.65rem)] leading-[1] sm:text-[clamp(2.7rem,4.5vw,5.2rem)] sm:leading-[0.98]">
          The next <span className="gold-text">90 days</span> could change everything.
        </h2>
        <p className="mx-auto mt-6 max-w-3xl text-base leading-7 text-[#9aa6b5] sm:mt-7 sm:text-lg sm:leading-8 xl:text-xl xl:leading-9">
          Stop trading hours for tutorials. Plug in a premium system and put your craft back at the center of your business.
        </p>
        <div className="mt-10 flex flex-col justify-center gap-4 sm:flex-row">
          <a href="#bundles" className="gold-button inline-flex items-center justify-center gap-4 rounded-full px-9 py-4 text-xs font-black uppercase tracking-[0.24em] text-[#06101a] transition hover:scale-[1.02]">
            Shop Bundles <ArrowRight className="h-4 w-4" />
          </a>
          <a href="#faq" className="inline-flex items-center justify-center rounded-full border border-white/8 px-9 py-4 text-xs font-black uppercase tracking-[0.24em] text-[#f4f7fb] transition hover:border-[#6f7a89]/50 hover:bg-white/[0.03]">
            Read FAQ
          </a>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="px-5 py-16 sm:px-8">
      <div className="mx-auto grid max-w-[94rem] gap-12 lg:grid-cols-[1.2fr_0.7fr_0.7fr_1fr]">
        <div>
          <BrandMark className="h-14 w-60" />
          <p className="mt-7 max-w-md text-sm leading-6 text-[#8f9baa]">
            Premium digital marketing bundles for service entrepreneurs. Built like a studio-grade growth system. Priced like a download.
          </p>
        </div>
        <FooterList title="Shop" items={["Beauty", "Creatives", "Health & Wellness", "Home Services"]} />
        <FooterList title="Company" items={["About", "FAQ", "Contact", "Terms"]} />
        <NewsletterForm />
      </div>
    </footer>
  );
}

function NewsletterForm() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState("idle");
  const [message, setMessage] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus("loading");
    setMessage("");

    try {
      const response = await fetch("/api/newsletter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
      });
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Signup failed. Please try again.");
      }

      setEmail("");
      setStatus("success");
      setMessage("You are on the list.");
    } catch (error) {
      setStatus("error");
      setMessage(error.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <p className="mb-6 text-xs font-bold uppercase tracking-[0.34em] text-[#8bd7ff]">Newsletter</p>
      <p className="mb-5 text-sm leading-6 text-[#8f9baa]">Monthly drops, new prompts, and free templates.</p>
      <div className="flex flex-col gap-2 sm:flex-row">
        <input
          className="min-w-0 flex-1 rounded-full border border-[#6f7a89]/10 bg-[#0b0f14] px-5 py-3 text-sm outline-none placeholder:text-[#667282] focus:border-[#8bd7ff]/35"
          placeholder="you@studio.com"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
        <button
          className="gold-button rounded-full px-6 py-3 text-xs font-black uppercase tracking-[0.18em] text-[#06101a] disabled:cursor-not-allowed disabled:opacity-60 sm:py-0"
          disabled={status === "loading"}
        >
          {status === "loading" ? "..." : "Join"}
        </button>
      </div>
      {message ? (
        <p className={`mt-3 text-xs ${status === "success" ? "text-[#b8f3ff]" : "text-[#ff9a88]"}`}>
          {message}
        </p>
      ) : null}
    </form>
  );
}

function FooterList({ title, items }) {
  return (
    <div>
      <p className="mb-6 text-xs font-bold uppercase tracking-[0.34em] text-[#8bd7ff]">{title}</p>
      <div className="space-y-4">
        {items.map((item) => (
          <a key={item} href={item === "FAQ" ? "#faq" : "#categories"} className="block text-sm text-[#8f9baa] transition hover:text-[#b8f3ff]">
            {item}
          </a>
        ))}
      </div>
    </div>
  );
}

function Section({ id, children, compactTop = false }) {
  return (
    <motion.section
      id={id}
      initial={{ opacity: 0, y: 22 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-120px" }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      className={`section-fade relative px-5 sm:px-8 ${compactTop ? "pb-16 pt-8 sm:pb-20 sm:pt-10 lg:pb-24 lg:pt-12" : "py-16 sm:py-20 lg:py-24"}`}
    >
      <div className="mx-auto max-w-[94rem]">{children}</div>
    </motion.section>
  );
}
