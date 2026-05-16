"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import ProductMockup from "./ProductMockup";

export default function ProductCard({ product, index }) {
  return (
    <motion.article
      whileHover={{ y: -8 }}
      transition={{ duration: 0.42, ease: [0.22, 1, 0.36, 1] }}
      className="group relative min-h-[25rem] overflow-hidden rounded-[1.75rem] border border-gold/14 bg-[#05070f] p-4 shadow-[0_24px_80px_rgba(0,0,0,0.28)]"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_0%,rgba(216,170,72,0.16),transparent_36%),radial-gradient(circle_at_85%_18%,rgba(71,164,255,0.08),transparent_30%)] opacity-80 transition duration-500 group-hover:opacity-100" />
      <div className="shine" />
      <div className="relative flex h-full flex-col">
        <Link
          href={`/products/${product.slug}`}
          aria-label={`View ${product.title}`}
          className="relative grid aspect-[1.48] place-items-center overflow-hidden rounded-[1.25rem] border border-white/10 bg-black/28 outline-none transition hover:border-gold/40 focus-visible:border-gold/70"
        >
          {product.image ? (
            <>
              <img
                src={product.image}
                alt={`${product.title} product mockup`}
                className="absolute inset-0 h-full w-full object-contain p-2 opacity-95 transition duration-700 group-hover:scale-[1.03]"
                loading="lazy"
              />
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_25%_8%,rgba(255,255,255,0.14),transparent_26%),linear-gradient(180deg,transparent,rgba(5,7,15,0.2))]" />
              <div className="absolute bottom-4 right-4 translate-y-3 rounded-full border border-gold/30 bg-ink/72 px-4 py-2 text-xs font-semibold uppercase tracking-[0.16em] text-gold opacity-0 backdrop-blur transition duration-300 group-hover:translate-y-0 group-hover:opacity-100">
                Open Bundle
              </div>
            </>
          ) : (
            <ProductMockup title={product.title} compact index={index} />
          )}
        </Link>
        <div className="mt-6 flex flex-1 flex-col">
          <div className="flex items-center justify-between gap-3">
            <p className="text-xs uppercase tracking-[0.24em] text-gold/80">{product.category}</p>
            <p className="rounded-full border border-gold/25 bg-gold/10 px-3 py-1 text-sm font-black text-gold">
              {product.price}
            </p>
          </div>
          <h3 className="editorial-serif mt-4 text-3xl leading-tight text-cream">{product.title}</h3>
          <p className="mt-3 flex-1 text-sm leading-6 text-cream/66">{product.description}</p>
          <Link
            href={`/products/${product.slug}`}
            className="mt-6 inline-flex items-center justify-between border-t border-gold/16 pt-4 text-sm font-semibold uppercase tracking-[0.16em] text-gold transition hover:text-cream"
          >
            View Bundle
            <ArrowRight className="h-4 w-4 text-gold" />
          </Link>
        </div>
      </div>
    </motion.article>
  );
}
