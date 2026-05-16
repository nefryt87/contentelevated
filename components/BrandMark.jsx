export default function BrandMark({ className = "h-12 w-52" }) {
  return (
    <svg
      viewBox="0 0 360 92"
      fill="none"
      aria-label="Content Elevated"
      className={className}
      role="img"
    >
      <defs>
        <linearGradient id="ceMarkGold" x1="24" y1="8" x2="82" y2="78" gradientUnits="userSpaceOnUse">
          <stop stopColor="#fff2c6" />
          <stop offset="0.45" stopColor="#c9a65e" />
          <stop offset="1" stopColor="#7d6229" />
        </linearGradient>
        <linearGradient id="ceMarkCream" x1="70" y1="17" x2="106" y2="74" gradientUnits="userSpaceOnUse">
          <stop stopColor="#ffffff" />
          <stop offset="0.72" stopColor="#f4f0e7" />
          <stop offset="1" stopColor="#b9b2a5" />
        </linearGradient>
      </defs>
      <path
        d="M62 18H53.5C38 18 27.5 29.6 27.5 46C27.5 62.4 38 74 53.5 74H62"
        stroke="url(#ceMarkGold)"
        strokeWidth="10"
        strokeLinecap="round"
      />
      <path
        d="M80 20H113M80 46H106M80 72H113"
        stroke="url(#ceMarkCream)"
        strokeWidth="9"
        strokeLinecap="square"
      />
      <text
        x="142"
        y="42"
        fill="#f7efd9"
        fontFamily="Inter, Arial, sans-serif"
        fontSize="18"
        fontWeight="700"
        letterSpacing="8"
      >
        CONTENT
      </text>
      <text
        x="142"
        y="68"
        fill="#c9a65e"
        fontFamily="Inter, Arial, sans-serif"
        fontSize="18"
        fontWeight="800"
        letterSpacing="8"
      >
        ELEVATED
      </text>
    </svg>
  );
}
