import { createApp } from 'vue'
import App from './App.vue'
const app = createApp(App)

// 引入elementplus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 开启深色模式
import 'element-plus/theme-chalk/dark/css-vars.css'
// 引入elementplus icon
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
app.use(ElementPlus)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

// 引入路由
import router from './router/index'
app.use(router)

// 引入vuex
import store from './store/index.js'
app.use(store)

// 配置全局变量baseUrl
app.provide('baseUrl', 'http://localhost:8080/'); 

// 配置axios
import axios from '@/plugins/axiosInstance.js'
app.config.globalProperties.$axios=axios;  //配置axios的全局引用

// 配置AntV G2
import * as G2 from '@antv/g2'//注,需要写成 * as G2 而不是 G2
app.config.globalProperties.$G2 = G2

// main.js文件中引入并全局注册
import * as echarts from 'echarts';//引入echarts
app.config.globalProperties.$echarts = echarts  //绑定实例

// 引入 ArcoVue
import ArcoVue from '@arco-design/web-vue';
import '@arco-design/web-vue/dist/arco.css';
app.use(ArcoVue);
// 图标库
import ArcoVueIcon from '@arco-design/web-vue/es/icon';
app.use(ArcoVueIcon);

// 引入tdesign
import TDesign from 'tdesign-vue-next';
// 引入组件库的少量全局样式变量
import 'tdesign-vue-next/es/style/index.css';
app.use(TDesign);

// Vue3 BaiduMap GL
import Vue3BaiduMapGL from 'vue3-baidu-map-gl'
app.use(Vue3BaiduMapGL)
import baiduMap from 'vue3-baidu-map-gl'
app.use(baiduMap, {
    ak: 'b574yOXrrOP81sWqXs4ZZ8019vhDZgth',
    plugins: ['TrackAnimation']
})

app.mount('#app')