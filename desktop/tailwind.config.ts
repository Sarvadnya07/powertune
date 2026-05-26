import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "Segoe UI", "Aptos", "sans-serif"],
        mono: ["JetBrains Mono", "Cascadia Code", "Consolas", "monospace"]
      },
      colors: {
        graphite: "#0a0d12",
        panel: "#101820",
        panel2: "#0c1722",
        line: "rgba(148, 163, 184, 0.18)",
        telemetry: "#8ee7ff",
        cobalt: "#4f7dff",
        healthy: "#5ee6a7",
        warn: "#ffc857",
        critical: "#ff6b6b"
      },
      boxShadow: {
        panel: "0 18px 45px rgba(0, 0, 0, 0.35)",
        glow: "0 0 26px rgba(142, 231, 255, 0.18)"
      }
    }
  },
  plugins: []
} satisfies Config;
