"use client";

import { motion } from "framer-motion";

export default function ProductMockup({ title = "Growth Bundle", compact = false, index = 0 }) {
  const label = title.replace(" Growth Bundle", "");

  return (
    <motion.div
      initial={{ opacity: 0, y: 12, rotate: -0.8 }}
      whileInView={{ opacity: 1, y: 0, rotate: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.58, delay: Math.min(index * 0.035, 0.18), ease: [0.22, 1, 0.36, 1] }}
      className={`product-box relative mx-auto ${compact ? "h-28 w-28" : "h-44 w-44 sm:h-56 sm:w-56"}`}
    >
      <div className="absolute inset-0 rounded-[18px] border border-[#6f7a89]/35 bg-[linear-gradient(145deg,rgba(188,245,255,0.18),rgba(11,15,20,0.94)_34%,rgba(107,124,255,0.16))] p-4 shadow-[0_0_70px_rgba(107,124,255,0.16)]">
        <div className="shine rounded-[18px]" />
        <div className="h-full rounded-[12px] border border-[#6f7a89]/10 bg-[radial-gradient(circle_at_30%_20%,rgba(107,124,255,0.26),transparent_35%),linear-gradient(160deg,rgba(11,15,20,0.92),rgba(5,7,11,0.96))] p-3">
          <div className="mb-3 h-1.5 w-12 rounded-full bg-[#b8f3ff]" />
          <div className="space-y-1.5">
            <div className="h-1.5 w-4/5 rounded-full bg-[#f7f8fb]/65" />
            <div className="h-1.5 w-3/5 rounded-full bg-[#f7f8fb]/26" />
            <div className="h-1.5 w-2/3 rounded-full bg-[#6f7a89]/32" />
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
