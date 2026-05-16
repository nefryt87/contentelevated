"use client";

import { motion } from "framer-motion";
import { BarChart3, Layers3, PenTool, Sparkles, Workflow } from "lucide-react";
import BrandMark from "./BrandMark";

const systemRows = [
  ["Market position", "96%"],
  ["Content engine", "90 days"],
  ["Client journey", "Mapped"],
  ["Launch assets", "Ready"]
];

const studioCards = [
  [PenTool, "Offer clarity"],
  [Layers3, "Template suite"],
  [Workflow, "Automation map"],
  [BarChart3, "Growth rhythm"]
];

export default function AboutVisual() {
  return (
    <div className="relative min-h-[32rem] overflow-hidden bg-[radial-gradient(circle_at_24%_18%,rgba(216,170,72,0.24),transparent_30%),radial-gradient(circle_at_78%_28%,rgba(71,164,255,0.18),transparent_30%),linear-gradient(145deg,#101827,#05070f)]">
      <div className="absolute inset-0 opacity-35 [background-image:linear-gradient(rgba(255,255,255,0.045)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.045)_1px,transparent_1px)] [background-size:44px_44px]" />
      <motion.div
        aria-hidden="true"
        animate={{ rotate: 360 }}
        transition={{ duration: 44, repeat: Infinity, ease: "linear" }}
        className="absolute left-1/2 top-1/2 h-[28rem] w-[28rem] -translate-x-1/2 -translate-y-1/2 rounded-full border border-gold/16"
      />
      <div className="absolute inset-8 rounded-[2rem] border border-gold/20 bg-white/[0.035] backdrop-blur" />

      <motion.div
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        className="absolute left-8 right-8 top-9 z-20 rounded-[2rem] border border-white/12 bg-black/28 p-5 shadow-glow backdrop-blur-xl"
      >
        <div className="mb-5 flex items-center justify-between gap-4">
          <BrandMark className="h-14 w-52" />
          <Sparkles className="h-5 w-5 text-gold" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          {studioCards.map(([Icon, label], index) => (
            <motion.div
              key={label}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.55, delay: index * 0.06 }}
              className="rounded-2xl border border-white/10 bg-white/[0.045] p-4"
            >
              <Icon className="mb-3 h-5 w-5 text-gold" />
              <p className="text-sm font-bold text-cream">{label}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      <div className="absolute bottom-10 left-10 right-10 z-30 rounded-[1.8rem] border border-white/10 bg-black/34 p-5 backdrop-blur-xl">
        <p className="mb-4 text-xs font-semibold uppercase tracking-[0.24em] text-gold">Studio framework</p>
        <div className="space-y-3">
          {systemRows.map(([label, value], index) => (
            <motion.div
              key={label}
              initial={{ opacity: 0, x: -14 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.55, delay: index * 0.07 }}
              className="flex items-center gap-4"
            >
              <span className="w-32 text-sm font-semibold text-cream/70">{label}</span>
              <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/10">
                <motion.div
                  initial={{ width: 0 }}
                  whileInView={{ width: `${82 - index * 9}%` }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.9, delay: 0.25 + index * 0.08, ease: [0.22, 1, 0.36, 1] }}
                  className="h-full rounded-full bg-gradient-to-r from-gold to-[#b8f3ff]"
                />
              </div>
              <span className="w-16 text-right text-xs font-bold uppercase tracking-[0.14em] text-gold">{value}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
