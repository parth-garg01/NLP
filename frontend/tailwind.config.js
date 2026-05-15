/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#111111",
        paper: "#F5F2E9",
        accent: "#D96C06",
        sea: "#0E7490"
      }
    }
  },
  plugins: [],
};
