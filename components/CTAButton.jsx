import { ArrowRight } from "lucide-react";

export default function CTAButton({ children, href = "#bundles", variant = "primary", external = false }) {
  const base =
    "inline-flex items-center justify-center gap-3 rounded-full px-7 py-4 text-xs font-black uppercase tracking-[0.22em] transition duration-300 sm:px-8";

  if (variant === "secondary") {
    return (
      <a
        href={href}
        target={external ? "_blank" : undefined}
        rel={external ? "noreferrer" : undefined}
        className={`${base} border border-cream/15 bg-white/[0.04] text-cream backdrop-blur hover:border-gold/50 hover:bg-white/[0.08]`}
      >
        {children}
        <ArrowRight className="h-4 w-4" />
      </a>
    );
  }

  return (
    <a
      href={href}
      target={external ? "_blank" : undefined}
      rel={external ? "noreferrer" : undefined}
      className={`${base} premium-button text-ink shadow-glow hover:scale-[1.02]`}
    >
      {children}
      <ArrowRight className="h-4 w-4" />
    </a>
  );
}
