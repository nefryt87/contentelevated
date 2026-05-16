"use client";

import { motion } from "framer-motion";

export default function AnimatedSection({ children, className = "", delay = 0, ...props }) {
  return (
    <motion.section
      {...props}
      initial={{ opacity: 0, y: 34 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.8, delay, ease: [0.22, 1, 0.36, 1] }}
      className={className}
    >
      {children}
    </motion.section>
  );
}
