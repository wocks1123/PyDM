const path = require("path");

module.exports = {
    transpileDependencies: [
        'vuetify'
    ],
    configureWebpack: {
        devtool: 'source-map'
    },
    devServer: {
        port: 53010,
        disableHostCheck: true,
        overlay: false
    },
    outputDir: path.resolve("../templates"),
    //assetsDir: "../static",
}

