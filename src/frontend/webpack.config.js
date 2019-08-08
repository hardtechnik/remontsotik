const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

module.exports = {
  entry: {
    'tickets.js': './src/js/tickets/index.js',
    'bundle.js': './src/main.js',
  },
  output: {
    path: path.join(__dirname, 'static'),
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
    ],
  },
};
