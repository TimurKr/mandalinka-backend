colors = require("tailwindcss/colors");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          100: "#ffefe7",
          200: "#ffdfcf",
          300: "#ffcfb7",
          400: "#ffbf9f",
          DEFAULT: "#ffaf87",
          600: "#cc8c6c",
          700: "#996951",
          800: "#664636",
          900: "#33231b",
        },
        secondary: {
          100: "#f2f0e6",
          200: "#e6e1cc",
          300: "#d9d3b3",
          400: "#cdc499",
          DEFAULT: "#c0b580",
          600: "#9a9166",
          700: "#736d4d",
          800: "#4d4833",
          900: "#26241a",
        },
        warning: "#ffcc00",
        success: "#339900",
        danger: "#cc0000",
      },
      keyframes: {
        "move-left-right": {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(10px)" },
        },
      },
      animation: {
        "move-left-right": "move-left-right 1s ease-in-out infinite alternate",
      },
    },
  },
  plugins: [require("prettier-plugin-tailwindcss")],
};
