"use client";

import { motion } from "framer-motion";

export default function ProductMockup({ title = "Growth Bundle", compact = false, index = 0 }) {
  const label = title.replace(" Growth Bundle", "");

  return (
    <motion.div
      animate={{ y: [0, -10, 0], rotate: [0, 1.5, 0] }}
      transition={{ duration: 5 + (index % 4), repeat: Infinity, ease: "easeInOut" }}
      className={`product-box relative mx-auto ${compact ? "h-28 w-28" : "h-44 w-44 sm:h-56 sm:w-56"}`}
    >
      <div className="absolute inset-0 rounded-[18px] border border-gold/50 bg-[linear-gradient(145deg,rgba(255,255,255,0.24),rgba(7,12,25,0.92)_34%,rgba(216,170,72,0.2))] p-4 shadow-glow">
        <div className="shine rounded-[18px]" />
        <div className="h-full rounded-[12px] border border-white/10 bg-[radial-gradient(circle_at_30%_20%,rgba(216,170,72,0.38),transparent_35%),linear-gradient(160deg,rgba(11,22,48,0.9),rgba(5,7,15,0.95))] p-3">
          <div className="mb-3 h-1.5 w-12 rounded-full bg-gold" />
          <div className="space-y-1.5">
            <div className="h-1.5 w-4/5 rounded-full bg-cream/70" />
            <div className="h-1.5 w-3/5 rounded-full bg-cream/30" />
            <div className="h-1.5 w-2/3 rounded-full bg-blueglow/40" />
          </div>
          <div className="absolute bottom-5 left-4 right-4">
            <p className="text-[9px] uppercase tracking-[0.28em] text-gold/80">Content Elevated</p>
            <p className={`${compact ? "text-[10px]" : "text-xs"} mt-1 max-w-[9rem] font-semibold leading-tight text-cream`}>
              {label}
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
