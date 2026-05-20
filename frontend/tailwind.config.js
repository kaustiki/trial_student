/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17202a",
        ocean: "#155e75",
        leaf: "#2f855a",
        clay: "#b45309",
        paper: "#f8fafc"
      }
    }
  },
  plugins: []
};
