const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // django路径，上线部署用
  assetsDir: "static",
  devServer: {
    hot: true,
  },
})
