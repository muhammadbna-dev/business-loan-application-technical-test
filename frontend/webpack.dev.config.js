const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");

const PORT = process.env.PORT;
const NODE_MODULES_DIR = path.resolve(__dirname, "node_modules");

module.exports = {
  mode: "development",
  context: __dirname,
  entry: "./src",
  output: {
    path: path.resolve(__dirname, "dist"),
    publicPath: `http://localhost:${PORT}/`,
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(?:js|jsx)$/,
        exclude: NODE_MODULES_DIR,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", "@babel/preset-react"],
          },
        },
      },
    ],
  },
  plugins: [
    new BundleTracker({
      filename: "webpack-stats.json",
      path: path.join(__dirname, "../"),
    }),
  ],
  resolve: {
    modules: ["node_modules", path.resolve(__dirname, "src")],
    extensions: [".js", ".jsx"],
  },
  devServer: {
    port: PORT,
    historyApiFallback: true,
    watchFiles: ["src"],
  },
  watchOptions: {
    aggregateTimeout: 200,
    poll: 1000,
  },
};
