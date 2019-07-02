const path = require("path");
const PerspectivePlugin = require("@finos/perspective-webpack-plugin");
const webpack = require("webpack");

module.exports = {
    entry: './build/index.js',
    output: {
        path: __dirname + '/dashboard/assets/static/js/',
        filename: 'bundle.js',
        publicPath: './static/js/'
    },
    plugins: [new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /(en|es|fr)$/), new PerspectivePlugin()],
    module: {
        rules: [
            {test: /\.css$/, use: [{loader: 'style-loader', }, {loader: 'css-loader', }, ], },
            {test: /\.ts?$/, loader: "ts-loader"}
        ]
    },
    mode: "development",
    devtool: "source-map"
};
