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
        obsidian: "#090d18",
        navy: "#0b1630",
        cream: "#f7efd9",
        muted: "#a8a392",
        gold: "#d8aa48",
        blueglow: "#47a4ff"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Satoshi", "Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      boxShadow: {
        glow: "0 0 80px rgba(216, 170, 72, 0.22)",
        blue: "0 0 80px rgba(71, 164, 255, 0.18)"
      }
    }
  },
  plugins: []
};
