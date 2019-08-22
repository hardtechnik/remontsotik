const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

const DIST_DIR = path.join(__dirname, 'dist');

module.exports = {
  entry: {
    'tickets.js': './src/js/tickets/index.js',
    'bundle.js': './src/main.js',
    'phone.js': './src/js/react/PhoneField.jsx',
  },
  output: {
    path: DIST_DIR,
    filename: '[name]',
  },
  optimization: {
    minimizer: [new TerserPlugin({}), new OptimizeCSSAssetsPlugin({})],
  },
  module: {
    rules: [
      {
         test: /\.scss$/,
         use: [
           'style-loader',
           'css-loader',
           'postcss-loader',
           'sass-loader'
         ],
      },
      {
        test: /\.jsx$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        },
      },
    ],
  },
};
