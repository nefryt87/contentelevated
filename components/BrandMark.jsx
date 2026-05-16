export default function BrandMark({ className = "h-12 w-52" }) {
  return (
    <img
      src="/brand/ce-logo-main.png"
      alt="Content Elevated"
      className={`brand-logo object-contain ${className}`}
    />
  );
}
