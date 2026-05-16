/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
    "./data/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#05070f",
        obsidian: "#090d14",
        navy: "#0a1324",
        cream: "#f7f8fb",
        muted: "#9aa6b5",
        gold: "#8bd7ff",
        blueglow: "#6b7cff"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Satoshi", "Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      boxShadow: {
        glow: "0 0 80px rgba(108, 238, 255, 0.18)",
        blue: "0 0 80px rgba(107, 124, 255, 0.18)"
      }
    }
  },
  plugins: []
};
