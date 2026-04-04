import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#111827",
        mist: "#eef2ff",
        paper: "#fffdf8",
        greenFlag: "#1f9d55",
        grayZone: "#d97706",
        redFlag: "#d14343",
      },
      fontFamily: {
        sans: ["var(--font-sans)", "sans-serif"],
      },
      boxShadow: {
        soft: "0 20px 60px rgba(17, 24, 39, 0.12)",
      },
      backgroundImage: {
        aurora:
          "radial-gradient(circle at top left, rgba(16, 185, 129, 0.18), transparent 32%), radial-gradient(circle at top right, rgba(245, 158, 11, 0.18), transparent 24%), linear-gradient(135deg, #fffdf8 0%, #f8fafc 60%, #eef2ff 100%)",
      },
    },
  },
  plugins: [],
};

export default config;
