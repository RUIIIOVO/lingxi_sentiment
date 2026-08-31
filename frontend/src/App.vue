<template>
  <BaseNav></BaseNav>
  <div class="wrap-main">
    <BaseMain></BaseMain>
  </div>
</template>

<script setup>
import BaseNav from "./components/BaseNav.vue";
import BaseMain from "./components/BaseMain.vue";

// 阻止element报错:ResizeObserver loop completed with undelivered notifications.
const debounce = (callback, delay) => {
  let tid;
  return function (...args) {
    const ctx = this;
    tid && clearTimeout(tid);
    tid = setTimeout(() => {
      callback.apply(ctx, args);
    }, delay);
  };
};
const _ = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ {
  constructor(callback) {
    callback = debounce(callback, 20);
    super(callback);
  }
};

// 引入autofit
import { onMounted } from "vue";
// import autofit from 'autofit.js'
onMounted(() => {
  // tdesign设置暗色模式
  document.documentElement.setAttribute('theme-mode', 'dark');
  // autofit.init({
  //   designHeight: 1080,
  //   designWidth: 1920,
  //   renderDom: "#app",
  //   resize: true,
  // });
});
</script>

<style>
.wrap-main {
  width: calc(100% - 120px);
  height: calc(100% - 40px);
  margin-left: 100px;
  padding-top: 20px;
  color: rgba(255, 255, 255, 0.9);
}
.flex-space-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.flex-space-around {
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.flex-column-space-between{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.flex-align-items-center{
  display: flex;
  align-items: center;
}
.flex-align-items-flex-end{
  display: flex;
  align-items:flex-end;
}
</style>   
