const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  mode: "development",
  entry: {
    ingredient_website: "./ingredients/static/ingredients/js/index.jsx",
  },
  output: {
    path: path.resolve(__dirname, "static/bundles/"),
    filename: "[name].bundle.js",
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", "@babel/preset-react"],
          },
        },
      },
    ],
  },
  plugins: [new BundleTracker({ filename: "./webpack-stats.json" })],
  resolve: {
    alias: {
      react: path.resolve("./node_modules/react"),
    },
  },
};
