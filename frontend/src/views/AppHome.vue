<!-- 热搜监测 -->
<template>
  <div class="main">
    <div style="grid-area: a1; height: 100%" class="wrap-head">
      <div>
        <p class="head-title">灵犀舆情</p>
        <p class="head-des">智能舆情预警分析可视化平台</p>
      </div>
      <div class="wrap-card" style="height: calc(100% - 168px)">
        <div class="title">
          <div class="left-title">
            <div class="icon"><icon-exclamation-circle /></div>
            <p>最新预警</p>
          </div>
          <div class="right-title">
            <p>当前预警：{{ alarm_total_num }}条</p>
          </div>
        </div>
        <el-scrollbar class="wrap-alarm-activities" height="calc(100% - 40px)">
          <a-empty v-if="alarm_flag" style="margin-top: 100px">
            <template #image>
              <icon-safe />
            </template>
            <p style="margin-top: 10px; color: rgb(255, 255, 255, 0.7)">
              安全监测中,暂无预警
            </p>
          </a-empty>
          <el-timeline
            v-if="!alarm_flag"
            style="margin-left: 5px; margin-top: 6px"
          >
            <el-timeline-item
              v-for="(activity, index) in alarm_activities"
              :key="index"
              :icon="activity.icon"
              :type="activity.type"
              :color="activity.color"
              :size="activity.size"
              :hollow="activity.hollow"
              :timestamp="activity.timestamp"
            >
              <t-tag
                theme="primary"
                variant="outline"
                style="margin-right: 8px; margin-bottom: 2px"
                >{{ activity.source }}</t-tag
              >
              <span v-html="highlightKeyword(activity)"></span>
            </el-timeline-item>
          </el-timeline>
        </el-scrollbar>
      </div>
      <!-- <div class="city-choose">
        <p class="city-choose-title">城市选择</p>
        <div class="city-choose-main">
          <a-cascader
            :options="options"
            :style="{
              width: '100%',
              marginRight: '16px',
            }"
            placeholder="请输入监测城市"
            allow-search
          />
          <a-button
            :style="{
              backgroundColor: 'rgba(36,158,255)',
              color: '#fff',
            }"
            >确定</a-button
          >
        </div>
      </div> -->
    </div>
    <div id="china-charts"></div>
    <div class="wrap-card" style="grid-area: a4">
      <div class="title">
        <div class="left-title">
          <div class="icon"><icon-fire /></div>
          <p>热搜榜单</p>
        </div>
        <div class="right-title">
          <!-- <p>热榜数量：{{ hot_search_num }}个</p> -->
          <el-select
            v-model="hot_search_select_value"
            class="m-2"
            placeholder="选择平台"
            size="small"
            style="width: 90px; margin-right: 10px"
          >
            <el-option
              v-for="item in hot_search_select_options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
      </div>
      <div class="wrap-left-box">
        <el-table
          :data="hot_search_list"
          max-height="180px"
          style="margin-top: 40px"
          size="small"
          @cell-click="handleCellClick"
        >
          <el-table-column
            type="index"
            label="排名"
            width="40"
          ></el-table-column>
          <el-table-column prop="title" label="事件"></el-table-column>
          <el-table-column
            prop="hot_value"
            label="热度值"
            width="70"
          ></el-table-column>
        </el-table>
      </div>
    </div>
    <div class="wrap-card" style="grid-area: b4; justify-content: center">
      <div class="title">
        <div class="left-title">
          <div class="icon"><icon-cloud /></div>
          <p>热搜关键词</p>
        </div>
        <div class="right-title">
          <p>热门搜索：词条</p>
        </div>
      </div>
      <!-- <div class="words">
        <span
          class="word-item"
          :style="{ backgroundColor: item.bgcolor }"
          v-for="(item, index) in hotWords"
          :key="index"
          >{{ item.content }}</span
        >
      </div> -->
      <div class="cloud">
        <img src="@/assets/img/word_cloud.png" alt="" />
      </div>
    </div>
    <div class="wrap-card" style="grid-area: c1">
      <div class="title">
        <div class="left-title">
          <div class="icon"><icon-layers /></div>
          <p>舆情分布TOP5</p>
        </div>
        <div class="right-title">
          <p>计量单位：条</p>
        </div>
      </div>
      <div style="width: 100%; margin-top: 18px">
        <div
          class="progress"
          v-for="(item, index) in events_source_list"
          :key="index"
        >
          <img :src="require('@/assets/img/' + item.imgName + '.png')" alt="" />
          <p :style="{ marginRight: item.margin }">{{ item.title }}</p>
          <a-progress
            :percent="item.percent"
            :animation="true"
            :color="item.color"
            trackColor="rgb(84, 84, 84, 0.6)"
            :stroke-width="8"
          >
            <template v-slot:text>
              {{ item.num }}
            </template>
          </a-progress>
        </div>
      </div>
    </div>
    <div class="wrap-card" style="grid-area: c2">
      <div class="title">
        <div class="left-title">
          <div class="icon"><icon-face-smile-fill /></div>
          <p>情感分析</p>
        </div>
        <div class="right-title">
          <p>舆情数量：{{ events_emotion_data.total }}个</p>
        </div>
      </div>
      <div class="wrap-left-box">
        <div style="margin-top: 10px">
          <div class="left-box">
            <p class="text-title">积极舆情数量</p>
            <p class="text-value">{{ events_emotion_data.positive }}</p>
          </div>
          <div class="left-box">
            <p class="text-title">消极舆情数量</p>
            <p class="text-value">{{ events_emotion_data.passive }}</p>
          </div>
        </div>
        <div id="emotion-charts"></div>
      </div>
    </div>
    <div class="wrap-card" style="grid-area: c3">
      <div class="title">
        <div class="left-title">
          <div class="icon"><icon-bar-chart /></div>
          <p>舆情变化趋势</p>
        </div>
        <div class="right-title">
          <el-select
            v-model="time_select_value"
            class="m-2"
            placeholder="选择时间"
            size="small"
            style="width: 90px; margin-right: 10px"
          >
            <el-option
              v-for="item in time_select_options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
      </div>
      <div id="heat-trend-charts"></div>
    </div>
    <div class="wrap-card" style="grid-area: c4">
      <div class="title">
        <div class="left-title">
          <div class="icon"><icon-tags /></div>
          <p>舆情种类</p>
        </div>
        <div class="right-title">
          <p>种类数量：{{ events_kinds_data_length }}个</p>
        </div>
      </div>
      <div id="kinds-charts"></div>
    </div>
    <!-- <BMap></BMap> -->
  </div>
</template>

<script setup>
// import BMap from './BMap.vue'

import * as echarts from "echarts";
import { graphic } from "echarts";
import "echarts/extension/bmap/bmap"; // bmap用来处理百度地图
import {
  ref,
  onMounted,
  onBeforeUnmount,
  reactive,
  nextTick,
  watch,
} from "vue";

// 引入user_id
import { useStore } from "vuex";
const store = useStore();
var user_id = ref(store.state.user_id);

import API from "@/plugins/axiosInstance";
// 预警信息
const alarm_activities = ref([]);
const alarm_total_num = ref(0);
const alarm_flag = ref(false);
function api_get_alarm_msg() {
  API({
    url: "/home/api_get_alarm_msg",
    method: "get",
    params: {
      user_id: user_id.value,
    },
  }).then((res) => {
    alarm_activities.value = [];
    alarm_total_num.value = res.data.length;
    if (res.data.length == 0) {
      alarm_flag.value = true;
      return;
    } else {
      alarm_flag.value = false;
    }
    res.data.forEach((element) => {
      let timestamp = new Date(element[2]);
      console.log(timestamp.getMonth());
      let formattedTimestamp =
        timestamp.getFullYear() +
        "-" +
        (timestamp.getMonth() + 1) +
        "-" +
        timestamp.getDate() +
        " " +
        timestamp.getHours() +
        ":" +
        (timestamp.getMinutes() < 10 ? "0" : "") +
        timestamp.getMinutes();
      let obj = {
        content: element[0],
        source: element[1],
        keyword: element[3],
        emotion: element[4],
        timestamp: formattedTimestamp,
        type: "primary",
        hollow: true,
      };
      alarm_activities.value.unshift(obj);
    });
  });
}

// 将关键词颜色替换为蓝色
function highlightKeyword(activity) {
  const highlightedContent = activity.content.replace(
    new RegExp(activity.keyword, "g"),
    '<span style="color:#a1d3ff;">$&</span>'
  );
  // 返回 HTML 字符串
  return `<span style="font-size: 14px;line-height:24px;">${highlightedContent}</span>`;
}

watch(
  store.state,
  () => {
    user_id.value = store.state.user_id;
    api_get_alarm_msg();
  },
  { deep: true }
);

// 热搜榜单
// var hot_search_num = ref(50);
var hot_search_list = reactive([]);
var hot_search_select_value = ref("weibo");
watch(hot_search_select_value, (newValue) => {
  api_get_hot_search(newValue);
});
var hot_search_select_options = [
  {
    label: "新浪微博",
    value: "weibo",
  },
  {
    label: "百度",
    value: "baidu",
  },
  {
    label: "今日头条",
    value: "toutiao",
  },
  {
    label: "抖音",
    value: "douyin",
  },
  // {
  //   label: "哔哩哔哩",
  //   value: "bili",
  // },
  {
    label: "知乎",
    value: "zhihu",
  },
  {
    label: "微信",
    value: "weixin",
  },
];
function api_get_hot_search(platform = "weibo") {
  API({
    url: "/home/api_get_hot_search",
    method: "get",
    params: {
      platform: platform,
    },
  }).then((res) => {
    hot_search_list.length = 0;
    hot_search_list.push(...res.data);
  });
}
// 点击单元格跳转url
function handleCellClick(row) {
  window.open(row.url, "_blank"); //新建标签页跳转
}

// 舆情分布
var events_source_list = reactive([]);
function api_get_events_source() {
  API({
    url: "/home/api_get_events_source",
    method: "get",
  }).then((res) => {
    let total_match_list = [
      {
        title: "新浪微博",
        imgName: "weibo",
        color: {
          "0%": "rgb(241,125,24)",
          "100%": "rgb(245,193,86)",
        },
      },
      {
        title: "快手",
        imgName: "kuaishou",
        color: {
          "0%": "rgb(241,125,24)",
          "100%": "rgb(245,193,86)",
        },
      },
      {
        title: "抖音",
        imgName: "douyin",
        color: {
          "0%": "rgb(66,35,129)",
          "100%": "rgb(147,23,243)",
        },
      },
      {
        title: "知乎",
        imgName: "zhihu",
        color: {
          "0%": "rgb(83,163,241)",
          "100%": "rgb(83,244,227)",
        },
      },
      {
        title: "百度",
        imgName: "baidu",
        color: {
          "0%": "rgb(83,163,241)",
          "100%": "rgb(83,244,227)",
        },
      },
      {
        title: "今日头条",
        imgName: "toutiao",
        color: {
          "0%": "rgb(214,51,67)",
          "100%": "rgb(247,50,149)",
        },
      },
      {
        title: "微信",
        imgName: "weixin",
        color: {
          "0%": "rgb(110,208,68)",
          "100%": "rgb(90,246,96)",
        },
      },
    ];
    let total_num = 0;
    res.data.forEach((element) => {
      total_match_list.forEach((e) => {
        if (element.title == e.title) {
          element["imgName"] = e.imgName;
          element["color"] = e.color;
          if (element.title.length < 4) {
            element["margin"] = "44px";
          }
        }
      });
      total_num += element.num;
    });
    res.data.forEach((element) => {
      let percent = element.num / total_num;
      element["percent"] = 0.2 + Number(percent.toFixed(2));
    });
    nextTick(() => {
      events_source_list.push(...res.data.slice(0, 5));
    });
  });
}

// 更新词云
// function api_update_word_cloud() {
//   API({
//     url: "/home/api_update_word_cloud",
//     method: "get",
//   }).then((res) => {
//     console.log(res);
//   });
// }

onMounted(() => {
  api_get_alarm_msg();
  api_get_hot_search();
  api_get_events_source();
  // 更新词云图
  // api_update_word_cloud();
});

// 情感分析
var events_emotion_data = ref([]);
function api_get_events_emotion() {
  return new Promise((resolve, reject) => {
    API({
      url: "/home/api_get_events_emotion",
      method: "get",
    })
      .then((res) => {
        resolve(res.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
var emotion_charts;
async function emotionChartsInit() {
  events_emotion_data.value = await api_get_events_emotion();
  emotion_charts = echarts.init(document.getElementById("emotion-charts"));
  let option;
  let isDark = true;
  option = {
    legend: {
      left: "center",
      data: ["积极", "消极"],
      bottom: 0,
      icon: "circle",
      itemWidth: 8,
      textStyle: {
        color: isDark ? "rgba(255, 255, 255, 0.7)" : "#4E5969",
      },
      itemStyle: {
        borderWidth: 0,
      },
    },
    tooltip: {
      show: true,
      trigger: "item",
    },
    graphic: {
      elements: [
        {
          type: "text",
          left: "center",
          top: "42%",
          style: {
            text: "舆情数量",
            textAlign: "center",
            fill: isDark ? "#ffffffb3" : "#4E5969",
            fontSize: 12,
          },
        },
        {
          type: "text",
          left: "center",
          top: "51%",
          style: {
            text: events_emotion_data.value.total,
            textAlign: "center",
            fill: isDark ? "#ffffffb3" : "#1D2129",
            fontSize: 14,
            fontWeight: 500,
          },
        },
      ],
    },
    series: [
      {
        type: "pie",
        radius: ["40%", "75%"],
        center: ["50%", "50%"],
        label: {
          formatter: function (data) {
            return data.percent.toFixed(0) + "%";
          },
          fontSize: 14,
          color: isDark ? "rgba(255, 255, 255, 0.9)" : "#4E5969",
          position: "inner",
        },
        itemStyle: {
          borderColor: isDark ? "#232324" : "#fff",
          borderWidth: 1,
        },
        data: [
          {
            value: events_emotion_data.value.positive,
            name: "积极",
            itemStyle: {
              color: "#71afe5 ",
            },
          },
          {
            value: events_emotion_data.value.passive,
            name: "消极",
            itemStyle: {
              color: "#005a9e",
            },
          },
        ],
      },
    ],
  };

  option && emotion_charts.setOption(option);
}

// 获取近期舆情数量变化
var time_select_value = ref("12");
var time_select_options = [
  {
    label: "12小时内",
    value: "12",
  },
  {
    label: "24小时内",
    value: "24",
  },
  {
    label: "7天内",
    value: "7",
  },
];
watch(time_select_value, (newValue) => {
  heat_trend_charts.dispose();
  heatTrendChartsInit(newValue);
});
function api_get_events_time(range_value = 12) {
  return new Promise((resolve, reject) => {
    API({
      url: "/home/api_get_events_time",
      method: "get",
      params: {
        range_value: range_value,
      },
    })
      .then((res) => {
        resolve(res.data.reverse());
      })
      .catch((error) => {
        reject(error);
      });
  });
}
var heat_trend_charts;
async function heatTrendChartsInit(range_value = 12) {
  let events_time_data = await api_get_events_time(range_value);
  console.log(events_time_data);
  // 修改x轴日期格式
  let xdata = [];
  for (let i = 0; i < events_time_data.length; i++) {
    let date = new Date(events_time_data[i]["select_time"]);
    if (range_value != 7) {
      xdata.push(
        date.toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" })
      );
    } else {
      xdata.push(
        date.toLocaleDateString("zh-CN", { month: "2-digit", day: "2-digit" })
      );
    }
  }
  heat_trend_charts = echarts.init(
    document.getElementById("heat-trend-charts")
  );
  let option;
  window.addEventListener("resize", function () {
    heat_trend_charts.resize();
  });
  option = {
    grid: {
      left: "8%",
      right: "3%",
      top: "15%",
      bottom: "15%",
    },
    xAxis: {
      show: true,
      type: "category",
      offset: 2,
      data: xdata,
      boundaryGap: false,
      axisLabel: {
        color: "#4E5969",
      },
      axisLine: {
        show: true,
      },
      axisTick: {
        show: false,
      },
      splitLine: {
        show: false,
        lineStyle: {
          color: "#E5E8EF",
        },
      },
      axisPointer: {
        show: true,
        lineStyle: {
          color: "#23ADFF",
          width: 2,
        },
      },
    },
    yAxis: {
      type: "value",
      axisLine: {
        show: true,
      },
      minInterval: 1,
      axisLabel: {},
      splitLine: {
        show: false,
        lineStyle: {
          type: "dashed",
          color: "#E5E8EF",
        },
      },
    },
    tooltip: {
      trigger: "axis",
      formatter: function (params) {
        const [firstElement] = params;
        return (
          '<div style="style="width: 140px;height: 72px;background: linear-gradient(303deg, rgba(253,254,255,0.60) -3%, rgba(244,247,252,0.60) 83%);opacity: 1;box-shadow: 0px 10px 20px 0px rgba(167, 200, 255, 0.5),inset 0px -2px 12px 0px rgba(229, 237, 250, 0.5),inset 0px 2px 6px 0px rgba(229, 237, 250, 0.9);">' +
          '<p style="font-size: 13px;line-height: 15px;display: flex;align-items: center;text-align: right;color: #1d2129;font-weight: 700;">' +
          firstElement.axisValueLabel +
          "</p>" +
          '<div style="display: flex;justify-content: space-between;padding: 0 9px;background: rgba(255,255,255,.8);width: 140px;height: 32px;line-height: 32px;box-shadow: 6px 0 20px #2257bc1a;border-radius: 4px;margin: 8px 0;"><span>舆情数量</span><span class="tooltip-value">' +
          firstElement.value +
          "</span></div>" +
          "</div>"
        );
      },
      className: "echarts-tooltip-diy",
    },
    series: [
      {
        data: events_time_data,
        type: "line",
        // smooth: true,
        symbolSize: 12,
        emphasis: {
          focus: "series",
          itemStyle: {
            borderWidth: 2,
          },
        },
        lineStyle: {
          width: 3,
          color: new graphic.LinearGradient(0, 0, 1, 0, [
            {
              offset: 0,
              color: "rgba(30, 231, 255, 1)",
            },
            {
              offset: 0.5,
              color: "rgba(36, 154, 255, 1)",
            },
            {
              offset: 1,
              color: "rgba(111, 66, 251, 1)",
            },
          ]),
        },
        showSymbol: false,
        areaStyle: {
          opacity: 0.8,
          color: new graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: "rgba(17, 126, 255, 0.3)",
            },
            {
              offset: 1,
              color: "rgba(17, 128, 255, 0)",
            },
          ]),
        },
      },
    ],
  };
  option && heat_trend_charts.setOption(option);
}

// 舆情种类
var events_kinds_data = ref([]);
var events_kinds_data_length = ref(0);
function api_get_events_kinds() {
  return new Promise((resolve, reject) => {
    API({
      url: "/home/api_get_events_kinds",
      method: "get",
    })
      .then((res) => {
        // 原始数据
        const originalData = res.data;
        events_kinds_data_length.value = originalData.length;
        // 根据 value 值排序
        originalData.sort((a, b) => b.value - a.value);
        // 取前五项
        const topFive = originalData.slice(0, 5);
        // 计算其他项的 value 总和
        const otherValue = originalData
          .slice(5)
          .reduce((acc, cur) => acc + cur.value, 0);
        // 添加其他项
        topFive.push({ name: "其他", value: otherValue });
        // 返回处理后的数据
        resolve(topFive);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
var kinds_charts;
async function kindsChartsInit() {
  events_kinds_data = await api_get_events_kinds();
  kinds_charts = echarts.init(document.getElementById("kinds-charts"));
  let option;
  option = {
    tooltip: {
      trigger: "item",
    },
    series: [
      {
        name: "舆情种类",
        type: "pie",
        // radius: "80%",
        radius: "65%",
        data: events_kinds_data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
        },
        label: {
          formatter: function (data) {
            return data.data.name + "\n\n" + data.percent.toFixed(0) + "%";
            // return data.percent.toFixed(0) + "%";
          },
          fontSize: 12,
          color: "rgba(255, 255, 255, 0.9)",
          // position: 'inner',
        },
        itemStyle: {
          normal: {
            color: function (colors) {
              var colorList = [
                "#004578",
                "#005a9e",
                "#106ebe",
                "#0078d4",
                "#2b88d8",
                "#71afe5",
              ];
              return colorList[colors.dataIndex];
            },
          },
        },
      },
    ],
  };

  option && kinds_charts.setOption(option);
}

var events_location_data = ref([]);
function api_get_events_location() {
  return new Promise((resolve, reject) => {
    API({
      url: "/home/api_get_events_location",
      method: "get",
    })
      .then((res) => {
        resolve(res.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
var medias_location_data = ref([]);
function api_get_medias_location() {
  return new Promise((resolve, reject) => {
    API({
      url: "/home/api_get_medias_location",
      method: "get",
    })
      .then((res) => {
        resolve(res.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

import locationJson from "@/assets/json/location.json";
var china_charts;
async function chinaChartsInit() {
  events_location_data = await api_get_events_location();
  console.log(events_location_data);
  medias_location_data = await api_get_medias_location();
  console.log(medias_location_data);
  china_charts = echarts.init(document.getElementById("china-charts"));
  let option;
  var geoCoordMap = locationJson;
  var convertData = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
      var geoCoord = geoCoordMap[data[i].name];
      if (geoCoord) {
        res.push({
          name: data[i].name,
          value: geoCoord.concat(data[i].value),
        });
      }
    }
    return res;
  };

  option = {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "item",
    },
    bmap: {
      // 显示中点坐标
      center: [134.2, 28],
      // 缩放比例
      zoom: 5,
      roam: true,
      mapStyle: {
        style: "dark",
      },
    },
    series: [
      // {
      //   name: "媒体账号数量",
      //   type: "scatter",
      //   coordinateSystem: "bmap",
      //   data: convertData(events_location_data),
      //   encode: {
      //     value: 2,
      //   },
      //   symbolSize: function (val) {
      //     return val[2] / 10;
      //   },
      //   label: {
      //     formatter: "{b}",
      //     position: "top",
      //   },
      //   itemStyle: {
      //     color: "#75baff",
      //   },
      //   emphasis: {
      //     label: {
      //       show: true,
      //     },
      //   },
      // },
      {
        name: "舆情数量",
        type: "effectScatter",
        coordinateSystem: "bmap",
        data: convertData(events_location_data),
        //触发事件 不取消全局地图事件
        silent: false,
        encode: {
          value: 2,
        },
        symbolSize: function (val) {
          return val[2] / 1.5;
        },
        // showEffectOn: "emphasis",
        rippleEffect: {
          brushType: "stroke",
        },
        hoverAnimation: true,
        label: {
          formatter: "{b}",
          position: "right",
          // show: true,
        },
        itemSymbol: "circle",
        itemStyle: {
          color: "#0984e3",
          shadowBlur: 10,
          shadowColor: "#333",
        },
        zlevel: 1,
      },
    ],
  };

  option && china_charts.setOption(option);
  //   // 去除百度标志
  // let element = document.querySelector('div.BMap_cpyCtrl');
  // element.remove();
}
onMounted(() => {
  emotionChartsInit();
  heatTrendChartsInit();
  kindsChartsInit();
  chinaChartsInit();
});
onBeforeUnmount(() => {
  // 销毁echarts实例
  emotion_charts.dispose();
  heat_trend_charts.dispose();
  kinds_charts.dispose();
  china_charts.dispose();
});
// const hotWords = [
//   {
//     content: "高校",
//     bgcolor: "#3498db",
//   },
//   {
//     content: "哈尔滨",
//     bgcolor: "#1abc9c",
//   },
//   {
//     content: "寒假",
//     bgcolor: "#2ecc71",
//   },
//   {
//     content: "过年",
//     bgcolor: "#f1c40f",
//   },
//   {
//     content: "期末",
//     bgcolor: "#e74c3c",
//   },
//   {
//     content: "考试周",
//     bgcolor: "#ffa502",
//   },
//   {
//     content: "重庆文旅",
//     bgcolor: "#ff6348",
//   },
//   {
//     content: "互联网",
//     bgcolor: "#1e90ff",
//   },
//   {
//     content: "人工智能",
//     bgcolor: "#686de0",
//   },
//   {
//     content: "新能源",
//     bgcolor: "#8395a7",
//   },
// ];

// const options = [
//   {
//     value: "beijing",
//     label: "Beijing",
//     children: [
//       {
//         value: "chaoyang",
//         label: "ChaoYang",
//         children: [
//           {
//             value: "datunli",
//             label: "Datunli",
//           },
//         ],
//       },
//       {
//         value: "haidian",
//         label: "Haidian",
//       },
//       {
//         value: "dongcheng",
//         label: "Dongcheng",
//       },
//       {
//         value: "xicheng",
//         label: "Xicheng",
//         children: [
//           {
//             value: "jinrongjie",
//             label: "Jinrongjie",
//           },
//           {
//             value: "tianqiao",
//             label: "Tianqiao",
//           },
//         ],
//       },
//     ],
//   },
//   {
//     value: "shanghai",
//     label: "Shanghai",
//     children: [
//       {
//         value: "huangpu",
//         label: "Huangpu",
//       },
//     ],
//   },
// ];
</script>

<style scoped>
.main {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.3fr) minmax(0, 1.3fr) minmax(
      0,
      1fr
    );
  grid-template-rows: repeat(3, minmax(0, 1fr));
  gap: 20px;
  grid-template-areas:
    "a1 a2 a2 a4"
    "a1 a2 a2 b4"
    "c1 c2 c3 c4";
}
/* 头部 */
.wrap-head {
  display: flex;
  flex-direction: column;
}
.head-title {
  font-family: "黑体";
  font-size: 36px;
  font-weight: 600;
  margin-top: 20px;
  margin-bottom: 16px;
}
.head-des {
  font-family: "黑体";
  font-size: 18px;
  color: rgb(255, 255, 255, 0.6);
  margin-bottom: 30px;
}
.city-choose {
  width: 100%;
}
.city-choose-title {
  font-size: 30px;
  font-weight: 600;
  margin-bottom: 20px;
}
.city-choose-main {
  display: flex;
  justify-content: space-around;
  align-items: center;
}
/* 卡片 */
.wrap-card {
  border-radius: 20px;
  backdrop-filter: blur(20px);
  /* background-color: rgba(52, 52, 52, 0.55); */
  background-color: #212121;
  border: 1px solid #2d2e2f;
  box-shadow: 0px 0px 4px rgba(10, 11, 23, 0.5);
  padding: 20px;
  position: relative;
  display: flex;
  align-items: center;
  color: rgb(255, 255, 255, 0.86);
}
/* 卡片标题 */
.wrap-card .title {
  width: 90%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  position: absolute;
  top: 14px;
  z-index: 20;
}
.wrap-card .left-title {
  display: flex;
  align-items: center;
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
  align-items: center;
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
  font-size: 12px;
  color: rgba(232, 232, 232, 0.5);
}
.left-box .text-value {
  font-size: 20px;
  font-weight: 600;
  margin-top: 5px;
}
.nodata-title {
  text-align: center;
  margin-top: 5px;
}
/* 透明卡片 */
/* .opacity-card {
  background-color: rgba(19, 21, 46);
  box-shadow: 0px 0px 4px rgba(10, 11, 23, 0.5);
} */
#emotion-charts {
  width: 220px;
  height: 220px;
}
#china-charts {
  grid-area: a2;
  width: 100%;
  height: 100%;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid #2d2e2f;
}
.baidu-tag {
  /* position: absolute; */
  bottom: 0;
  right: 0;
}
#heat-trend-charts {
  width: 110%;
  height: 220px;
  margin-top: 10px;
}
#kinds-charts {
  width: 110%;
  height: 220px;
  margin-top: 10px;
  margin-bottom: -20px;
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
/* 告警时间 */
.wrap-alarm-activities {
  margin-top: 40px;
  width: 100%;
  align-self: baseline;
}
.wrap-alarm-activities p {
  color: #fff;
}
/* 关键词 */
.words {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
  margin-top: 20px;
}
.word-item {
  padding: 10px;
  margin: 8px;
  border-radius: 6px;
  /* background-color: rgb(97, 97, 97); */
  color: #fff;
}
.cloud {
  display: flex;
  justify-content: center;
  align-items: center;
}
.cloud img {
  width: 100%;
  height: 180px;
  margin: 30px auto 0 auto;
  object-fit: cover;
}
/* 时间选择下拉框 */
.time-select {
  cursor: pointer;
}
.arco-dropdown-open .arco-icon-down {
  transform: rotate(180deg);
}
:deep(.el-table__row:hover){
  cursor: pointer;
}
</style>