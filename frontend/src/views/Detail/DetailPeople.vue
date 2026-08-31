<!-- 人物画像 -->
<template>
  <div style="height: 100%">
    <div class="wrap-top">
      <div id="china">
      </div>
              <p class="china-tip">© 2024 Baidu - GS(2023)3206号 - 甲测资字11111342 - 京ICP证030173号 - Data © 百度智图 & OpenStreetMap HERE</p>

      <div class="wrap-card" style="width: 32%">
        <div class="title">
          <div class="left-title">
            <p>省份分布</p>
          </div>
          <div class="right-title">
            <p>评论用户数量：{{mapData.length}}个</p>
          </div>
        </div>
        <div style="width: 100%; margin-top: 18px">
          <div
            class="progress"
            v-for="(item, index) in capital_list"
            :key="index"
          >
            <p>{{ item.name }}</p>
            <a-progress
              :percent="item.percent"
              :animation="true"
              :color="{ '0%': 'rgb(58, 144, 232)', '100%': '#baeeff' }"
              trackColor="rgb(84, 84, 84, 0.6)"
              :stroke-width="8"
            >
              <template v-slot:text>
                {{ item.value }}
              </template>
            </a-progress>
          </div>
        </div>
      </div>
    </div>
    <div
      style="display: flex; justify-content: space-between; margin: 20px 0 0px 0"
    >
      <div class="wrap-card">
        <div class="title">
          <div class="left-title">
            <div class="icon"></div>
            <p>年龄分布</p>
          </div>
        </div>
        <div id="age-charts"></div>
      </div>
      <div class="wrap-card" style="width: 50%">
        <div class="title" style="margin-bottom: 30px">
          <div class="left-title">
            <div class="icon"></div>
            <p>性别分布</p>
          </div>
          <div class="right-title"></div>
        </div>
        <div class="wrap-left-box">
          <div id="sex-charts"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import * as echarts from "echarts";
import API from "@/plugins/axiosInstance";

// 获取title
import { useStore } from "vuex";
const store = useStore();

import chinaMap from "@/assets/json/china.json";
var china_charts;
// var mapData = [
//   { name: "北京", value: 1 },
//   { name: "天津", value: 2 },
//   { name: "上海", value: 3 },
//   { name: "重庆", value: 4 },
//   { name: "河北", value: 5 },
//   { name: "河南", value: 6 },
//   { name: "云南", value: 7 },
//   { name: "辽宁", value: 8 },
//   { name: "黑龙江", value: 9 },
//   { name: "湖南", value: 10 },
//   { name: "安徽", value: 11 },
//   { name: "山东", value: 12 },
//   { name: "新疆", value: 13 },
//   { name: "江苏", value: 14 },
//   { name: "浙江", value: 15 },
//   { name: "江西", value: 16 },
//   { name: "湖北", value: 17 },
//   { name: "广西", value: 18 },
//   { name: "甘肃", value: 19 },
//   { name: "山西", value: 20 },
//   { name: "内蒙古", value: 21 },
//   { name: "陕西", value: 22 },
//   { name: "吉林", value: 23 },
//   { name: "福建", value: 24 },
//   { name: "贵州", value: 25 },
//   { name: "广东", value: 26 },
//   { name: "青海", value: 27 },
//   { name: "西藏", value: 28 },
//   { name: "四川", value: 29 },
//   { name: "宁夏", value: 30 },
//   { name: "海南", value: 31 },
//   { name: "台湾", value: 32 },
//   { name: "香港", value: 33 },
//   { name: "澳门", value: 34 },
// ];
var mapData = ref([])
function api_get_people_ip(){
  return new Promise((resolve, reject) => {
    API({
      url: "/database/api_get_people_ip",
      method: "get",
      params: {
        title: store.state.title,
      },
    })
      .then((res) => {
        resolve(res.data);
      })
      .catch((error) => {
        reject(error);
      });
  });  
}
async function chinaChartsInit() {
  mapData.value = await api_get_people_ip();
  // console.log(mapData);
  echarts.registerMap("china", { geoJSON: chinaMap });
  china_charts = echarts.init(document.getElementById("china"));
  let option;
  window.addEventListener("resize", function () {
    china_charts.resize();
  });

  china_charts.setOption({
    backgroundColor: "transparent",
    title: {
      text: "地域分布",
      subtext: "",
      x: "left",
      textStyle: {
        color: "rgba(256, 256, 256, 0.8)",
      },
    },
    tooltip: {
      trigger: "item",
    },
    geo: {
      // 地理坐标系组件用于地图的绘制
      map: "china", // 表示中国地图
      roam: true, // 是否开启鼠标缩放和平移漫游
      zoom: 1.75, // 当前视角的缩放比例（地图的放大比例）
      center: [100, 36],
      label: {
        normal: {
          show: false, //省份名称----你可以选择true，展示每个省份的名称
        },
        emphasis: {
          show: true,
          textStyle: {
            color: "rgba(256, 256, 256, 0.8)",
          },
        },
      },
      itemStyle: {
        // 地图区域的多边形 图形样式。
        borderColor: "rgba(0, 0, 0, 0.2)",
        // areaColor: "#d0ebff",
        emphasis: {
          // 高亮状态下的多边形和标签样式
          shadowBlur: 20,
          shadowColor: "rgba(0, 0, 0, 0.5)",
          areaColor: "#3375b9",
          color: "#fff",
        },
      },
    },
    select: {
      // 地图选中区域样式
      label: {
        // 选中区域的label(文字)样式
        color: "#fff",
      },
      itemStyle: {
        // 选中区域的默认样式
        areaColor: "#3375b9",
      },
    },
    visualMap: {
      //左下角的渐变颜色条
      min: 0,
      max: 10,
      left: "left",
      top: "bottom",
      text: ["高", "低"],
      textStyle: {
        color: "rgba(256, 256, 256, 0.8)",
      },
      inRange: {
        color: ["#e0ffff", "#006edd"],
      },
      show: true,
    },
    //配置属性
    series: [
      {
        name: "用户数量",
        type: "map",
        mapType: "china",
        geoIndex: 0, //理解就是多个组件都能用option里配置的geo地图，类似于坐标轴里的yAxisIndex:numder,也就是说你可以配置多个geo，也可以多个组件共用geo
        data: mapData.value,
      },
    ],
  });
  option && china_charts.setOption(option);
}

// 省会排名
var capital_list = ref([]);
async function api_get_capital_list() {
  let res = await await api_get_people_ip();
  capital_list.value = res.sort((a, b) => b.value - a.value).slice(0, 8);
  let mapTotalValue = res.reduce((acc, curr) => acc + curr.value, 0);
  capital_list.value = res
    .sort((a, b) => b.value - a.value)
    .slice(0, 8)
    .map((item) => {
      item.percent = (item.value / mapTotalValue).toFixed(2);
      return item;
    });
}

// 年龄分布
function api_get_people_age(){
  return new Promise((resolve, reject) => {
    API({
      url: "/database/api_get_people_age",
      method: "get",
      params: {
        title: store.state.title,
      },
    })
      .then((res) => {
        resolve(res.data);
      })
      .catch((error) => {
        reject(error);
      });
  });  
}
var age_charts;
async function ageChartsInit() {
  let age_data = await api_get_people_age();
  console.log(age_data);
  age_charts = echarts.init(document.getElementById("age-charts"));
  let option;
  window.addEventListener("resize", function () {
    age_charts.resize();
  });
  option = {
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
    },
    grid: {
      top: "12%",
      left: "3%",
      right: "4%",
      bottom: "5%",
      containLabel: true,
    },
    xAxis: [
      {
        type: "category",
        data: ["≤19", "20~29", "30~39", "40~49", "≥50"],
        axisTick: {
          alignWithLabel: true,
        },
        // 刻度线文字颜色
        axisLabel: {
          show: true,
          textStyle: {
            color: "rgb(256, 256, 256, 0.75)",
          },
        },
      },
    ],
    yAxis: [
      {
        type: "value",
        // 水平分割线颜色
        splitLine: {
          show: true,
          lineStyle: {
            type: "dashed",
            color: "rgb(102, 102, 102)",
          },
        },
        // 刻度线文字颜色
        axisLabel: {
          show: true,
          textStyle: {
            color: "rgb(256, 256, 256, 0.75)",
          },
        },
      },
    ],
    series: [
      {
        name: "用户数量",
        type: "bar",
        barWidth: "28%",
        // data: [200, 334, 390, 330, 220],
        data:age_data,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#83bff6" },
            { offset: 0.5, color: "#188df0" },
            { offset: 1, color: "#188df0" },
          ]),
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "#2378f7" },
              { offset: 0.7, color: "#2378f7" },
              { offset: 1, color: "#83bff6" },
            ]),
          },
        },
      },
    ],
  };
  option && age_charts.setOption(option);
}

// 性别分布
function api_get_people_sex(){
  return new Promise((resolve, reject) => {
    API({
      url: "/database/api_get_people_sex",
      method: "get",
      params: {
        title: store.state.title,
      },
    })
      .then((res) => {
        resolve(res.data);
      })
      .catch((error) => {
        reject(error);
      });
  });  
}
var sex_charts;
async function sexChartsInit() {
  let sex_data = await api_get_people_sex();
  sex_charts = echarts.init(document.getElementById("sex-charts"));
  let option;
  option = {
    tooltip: {
      trigger: "item",
    },
    legend: {
      left: "center",
      bottom: 50,
      icon: "circle",
      orient: "horizontal",
      textStyle: {
        color: "rgba(256,256,256,0.8)",
      },
    },
    series: [
      {
        name: "用户数量",
        type: "pie",
        radius: ["35%", "65%"],
        center: ["50%", "35%"],
        itemStyle: {
          borderRadius: 5,
          borderColor: "#242424",
          borderWidth: 3,
          color: function (colors) {
            var colorList = [
              "#1f7ed1",
              "#71afe5",
            ];
            return colorList[colors.dataIndex];
          },
        },
        data: sex_data,
        label: {
          formatter: function (data) {
            return data.name + "\n" + data.percent.toFixed(0) + "%";
          },
          fontSize: 14,
          fontWeight: "bold",
          lineHeight: 20,
          color: "rgba(255, 255, 255, 0.9)",
          position: "inner",
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: "bold",
          },
        },
      },
    ],
  };
  option && sex_charts.setOption(option);
}

onMounted(() => {
  api_get_capital_list();
  chinaChartsInit();
  ageChartsInit();
  sexChartsInit();
});
onBeforeUnmount(() => {
  sex_charts.dispose();
  age_charts.dispose();
  china_charts.dispose();
});
</script>

<style scoped>
#china {
  width: 50%;
  height: 380px;
  
}
.wrap-top {
  width: calc(100% - 50px);
  height: 380px;
  margin: 30px auto 40px auto;
  display: flex;
  justify-content: space-between;
  position: relative;
}
/* 卡片 */
.wrap-card {
  width: 100%;
  padding: 0 20px;
  color: rgb(255, 255, 255, 0.86);
}
/* 卡片标题 */
.wrap-card .title {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  z-index: 20;
}
.wrap-card .left-title {
  display: flex;
  align-items: center;
  font-weight: 600;
}
.wrap-card .right-title {
  font-size: 12px;
  color: rgba(214, 214, 214, 0.5);
}
.wrap-card .icon {
  font-size: 18px;
  color: rgb(164, 164, 164);
  margin-right: 8px;
}
/* 卡片左侧文字 */
.wrap-left-box {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.left-box {
  margin-bottom: 30%;
  margin-left: 20px;
}
.left-box:last-child {
  margin-bottom: 0px;
}
.left-box .text-title {
  font-size: 14px;
  color: rgba(232, 232, 232, 0.5);
  width: 90px;
}
.left-box .text-value {
  font-size: 22px;
  font-weight: 600;
  margin-top: 15px;
}
#sex-charts {
  width: 100%;
  height: 300px;
}
#age-charts {
  width: 100%;
  height: 300px;
}
/* 舆情分布TOP5 */
.progress {
  display: flex;
  align-items: center;
  margin-top: 20px;
  width: 100%;
  white-space: nowrap;
}
.progress img {
  width: 20px;
  height: 20px;
  border-radius: 20px;
}
.progress p {
  margin: 0 20px 0 8px;
  font-size: 12px;
}
:deep(.arco-progress-line-text) {
  color: rgb(255, 255, 255);
  font-size: 16px;
}
.china-tip{
  position:absolute;
  bottom: -30px;
  left: 0;
  font-size: 10px;
}
</style>