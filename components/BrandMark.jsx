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
        <linearGradient id="ceMarkSignal" x1="24" y1="8" x2="82" y2="78" gradientUnits="userSpaceOnUse">
          <stop stopColor="#ffffff" />
          <stop offset="0.48" stopColor="#b8f3ff" />
          <stop offset="1" stopColor="#7c8cff" />
        </linearGradient>
        <linearGradient id="ceMarkWhite" x1="70" y1="17" x2="106" y2="74" gradientUnits="userSpaceOnUse">
          <stop stopColor="#ffffff" />
          <stop offset="0.72" stopColor="#edf4fb" />
          <stop offset="1" stopColor="#9aa7b7" />
        </linearGradient>
      </defs>
      <path
        d="M62 18H53.5C38 18 27.5 29.6 27.5 46C27.5 62.4 38 74 53.5 74H62"
        stroke="url(#ceMarkSignal)"
        strokeWidth="10"
        strokeLinecap="round"
      />
      <path
        d="M80 20H113M80 46H106M80 72H113"
        stroke="url(#ceMarkWhite)"
        strokeWidth="9"
        strokeLinecap="square"
      />
      <text
        x="142"
        y="42"
        fill="#f7f8fb"
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
        fill="#b8f3ff"
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
