"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { useEffect, useState } from "react";
import ProductMockup from "./ProductMockup";

function useHoverCapable() {
  const [canHover, setCanHover] = useState(false);

  useEffect(() => {
    const query = window.matchMedia("(hover: hover) and (pointer: fine)");
    const update = () => setCanHover(query.matches);

    update();
    query.addEventListener("change", update);

    return () => query.removeEventListener("change", update);
  }, []);

  return canHover;
}

export default function ProductCard({ product, index }) {
  const canHover = useHoverCapable();

  return (
    <motion.article
      whileHover={canHover ? { y: -5 } : undefined}
      transition={{ duration: 0.42, ease: [0.22, 1, 0.36, 1] }}
      className="premium-edge group relative min-h-[22rem] overflow-hidden rounded-[1.25rem] border border-[#6f7a89]/10 bg-[#0b0f14] p-3 shadow-[0_18px_58px_rgba(0,0,0,0.24)] sm:min-h-[25rem] sm:rounded-[1.75rem] sm:p-4 sm:shadow-[0_24px_80px_rgba(0,0,0,0.28)]"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_0%,rgba(107,124,255,0.12),transparent_36%),radial-gradient(circle_at_85%_18%,rgba(188,245,255,0.035),transparent_30%)] opacity-80 transition duration-500 sm:group-hover:opacity-100" />
      <div className="shine" />
      <div className="relative flex h-full flex-col">
        <Link
          href={`/products/${product.slug}`}
          aria-label={`View ${product.title}`}
          className="relative grid aspect-[1.48] place-items-center overflow-hidden rounded-[1.25rem] border border-[#6f7a89]/8 bg-[radial-gradient(circle_at_50%_18%,rgba(107,124,255,0.08),transparent_18rem),#10141b] outline-none transition hover:border-[#6f7a89]/32 focus-visible:border-[#b8f3ff]/70"
        >
          {product.image ? (
            <>
              <img
                src={product.image}
                alt={`${product.title} product mockup`}
                className="absolute inset-0 h-full w-full object-contain p-2 opacity-95 transition duration-700 sm:group-hover:scale-[1.03]"
                loading="lazy"
              />
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_25%_8%,rgba(188,245,255,0.09),transparent_26%),linear-gradient(180deg,transparent,rgba(5,7,11,0.2))]" />
              <div className="absolute bottom-4 right-4 hidden translate-y-3 rounded-full border border-[#6f7a89]/22 bg-[#05070b]/72 px-4 py-2 text-xs font-semibold uppercase tracking-[0.16em] text-[#b8f3ff] opacity-0 backdrop-blur transition duration-300 sm:block sm:group-hover:translate-y-0 sm:group-hover:opacity-100">
                Open Bundle
              </div>
            </>
          ) : (
            <ProductMockup title={product.title} compact index={index} />
          )}
        </Link>
        <div className="mt-5 flex flex-1 flex-col sm:mt-6">
          <div className="flex items-center justify-between gap-3">
            <p className="text-[0.62rem] uppercase tracking-[0.18em] text-[#8bd7ff] sm:text-xs sm:tracking-[0.24em]">{product.category}</p>
            <p className="rounded-full border border-[#6f7a89]/18 bg-[#6f7a89]/8 px-3 py-1 text-sm font-black text-[#b8f3ff]">
              {product.price}
            </p>
          </div>
          <h3 className="editorial-serif mt-4 text-[1.65rem] leading-tight text-[#f7f8fb] sm:text-3xl">{product.title}</h3>
          <p className="mt-3 flex-1 text-sm leading-6 text-[#8f9baa]">{product.description}</p>
          <Link
            href={`/products/${product.slug}`}
            className="mt-5 inline-flex items-center justify-between border-t border-gradient-soft pt-4 text-[0.72rem] font-semibold uppercase tracking-[0.14em] text-[#b8f3ff] transition hover:text-[#f7f8fb] sm:mt-6 sm:text-sm sm:tracking-[0.16em]"
          >
            View Bundle
            <ArrowRight className="h-4 w-4 text-[#b8f3ff]" />
          </Link>
        </div>
      </div>
    </motion.article>
  );
}
