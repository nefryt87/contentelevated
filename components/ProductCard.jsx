"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import ProductMockup from "./ProductMockup";

export default function ProductCard({ product, index }) {
  return (
    <motion.article
      whileHover={{ y: -5 }}
      transition={{ duration: 0.42, ease: [0.22, 1, 0.36, 1] }}
      className="premium-edge group relative min-h-[22rem] overflow-hidden rounded-[1.25rem] border border-[#c9a65e]/10 bg-[#0b0a08] p-3 shadow-[0_18px_58px_rgba(0,0,0,0.24)] sm:min-h-[25rem] sm:rounded-[1.75rem] sm:p-4 sm:shadow-[0_24px_80px_rgba(0,0,0,0.28)]"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_0%,rgba(201,166,94,0.12),transparent_36%),radial-gradient(circle_at_85%_18%,rgba(245,227,167,0.035),transparent_30%)] opacity-80 transition duration-500 group-hover:opacity-100" />
      <div className="shine" />
      <div className="relative flex h-full flex-col">
        <Link
          href={`/products/${product.slug}`}
          aria-label={`View ${product.title}`}
          className="relative grid aspect-[1.48] place-items-center overflow-hidden rounded-[1.25rem] border border-[#c9a65e]/8 bg-[radial-gradient(circle_at_50%_18%,rgba(201,166,94,0.08),transparent_18rem),#11100b] outline-none transition hover:border-[#c9a65e]/32 focus-visible:border-[#dcc27b]/70"
        >
          {product.image ? (
            <>
              <img
                src={product.image}
                alt={`${product.title} product mockup`}
                className="absolute inset-0 h-full w-full object-contain p-2 opacity-95 transition duration-700 group-hover:scale-[1.01] sm:group-hover:scale-[1.03]"
                loading="lazy"
              />
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_25%_8%,rgba(245,227,167,0.09),transparent_26%),linear-gradient(180deg,transparent,rgba(5,5,3,0.2))]" />
              <div className="absolute bottom-4 right-4 translate-y-3 rounded-full border border-[#c9a65e]/22 bg-[#050503]/72 px-4 py-2 text-xs font-semibold uppercase tracking-[0.16em] text-[#dcc27b] opacity-0 backdrop-blur transition duration-300 group-hover:translate-y-0 group-hover:opacity-100">
                Open Bundle
              </div>
            </>
          ) : (
            <ProductMockup title={product.title} compact index={index} />
          )}
        </Link>
        <div className="mt-5 flex flex-1 flex-col sm:mt-6">
          <div className="flex items-center justify-between gap-3">
            <p className="text-[0.62rem] uppercase tracking-[0.18em] text-[#b99b63] sm:text-xs sm:tracking-[0.24em]">{product.category}</p>
            <p className="rounded-full border border-[#c9a65e]/18 bg-[#c9a65e]/8 px-3 py-1 text-sm font-black text-[#dcc27b]">
              {product.price}
            </p>
          </div>
          <h3 className="editorial-serif mt-4 text-[1.65rem] leading-tight text-[#f4eee2] sm:text-3xl">{product.title}</h3>
          <p className="mt-3 flex-1 text-sm leading-6 text-[#9e9688]">{product.description}</p>
          <Link
            href={`/products/${product.slug}`}
            className="mt-5 inline-flex items-center justify-between border-t border-gradient-soft pt-4 text-[0.72rem] font-semibold uppercase tracking-[0.14em] text-[#dcc27b] transition hover:text-[#f4eee2] sm:mt-6 sm:text-sm sm:tracking-[0.16em]"
          >
            View Bundle
            <ArrowRight className="h-4 w-4 text-[#dcc27b]" />
          </Link>
        </div>
      </div>
    </motion.article>
  );
}
