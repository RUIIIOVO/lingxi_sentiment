import { createRouter ,createWebHashHistory } from 'vue-router';
// 引入基本主体页
import BaseMain from "../components/BaseMain.vue"
// 引入首页
import AppHome from "../views/AppHome.vue"
// 引入事件库
import AppDatabase from "../views/AppDatabase.vue"
// 引入事件库详情页
import AppDetail from "../views/AppDetail.vue"
// 引入热搜监测
import AppMonitor from "../views/AppMonitor.vue"


// 创建路由管理器对象，并配置路由表
const router = createRouter({
  history: createWebHashHistory (),
  routes: [
    { 
      path: '/', 
      component: BaseMain,
      children:[
        {
          path:'/',
          component:AppHome,
        },
        {
          path:'/AppHome',
          component:AppHome,
        },
        {
          path:'/AppDatabase',
          component:AppDatabase,
        },
        {
          path:'/AppDetail',
          component:AppDetail,
        },
        {
          path:'/AppMonitor',
          component:AppMonitor,
        },
      ]
    },
  ],
});

// 导出路由
export default router;
