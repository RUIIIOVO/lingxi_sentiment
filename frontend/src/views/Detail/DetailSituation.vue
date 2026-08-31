<!-- 事件概况 -->
<template>
  <div style="display: flex;flex-direction: column;">
    <div class="wrap-msg">
      <t-descriptions
        title="事件详情"
        :label-style="{ width: '60px', textAlign: 'left' }"
      >
        <t-descriptions-item label="事件标题">{{
          events.title
        }}</t-descriptions-item>
        <t-descriptions-item label="标签">
          <el-tag
            style="margin-right: 16px"
            v-for="(tag, index) in events.tags"
            :key="index"
            >{{ tag }}</el-tag
          >
        </t-descriptions-item>
        <t-descriptions-item label="报道时间">{{
          events.time
        }}</t-descriptions-item>
        <t-descriptions-item label="报道地点">{{
          events.location
        }}</t-descriptions-item>
        <t-descriptions-item label="事件来源">{{
          events.source
        }}</t-descriptions-item>
        <t-descriptions-item label="报道媒体">{{
          events.media
        }}</t-descriptions-item>
        <t-descriptions-item label="事件简介">{{
          events.text
        }}</t-descriptions-item>
      </t-descriptions>
    </div>
    <div style="display: flex; justify-content: space-between">
      <div class="wrap-card">
        <div class="title">
          <div class="left-title">
            <div class="icon"></div>
            <p>热度变化趋势</p>
          </div>
          <div class="right-title">
            <el-select
              v-model="time_select_value"
              class="m-2"
              placeholder="选择时间"
              size="small"
              style="width: 90px"
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
        <el-empty description="暂无数据" v-show="dataFlag" />
        <div id="heat-trend-charts" v-show="!dataFlag"></div>
      </div>
      <div class="wrap-card" style="width: 40%">
        <div class="title" style="margin-bottom: 50px">
          <div class="left-title">
            <div class="icon"></div>
            <p>情感分析</p>
          </div>
          <div class="right-title">
            <p>评论数量：{{ events_emotion_data.total }}个</p>
          </div>
        </div>
        <div class="wrap-left-box" style="height: 300px">
          <div style="margin-top: 20px">
            <div class="left-box">
              <p class="text-title">积极评论数量</p>
              <p class="text-value">{{ events_emotion_data.positive }}</p>
            </div>
            <div class="left-box">
              <p class="text-title">消极评论数量</p>
              <p class="text-value">{{ events_emotion_data.passive }}</p>
            </div>
          </div>
          <div id="emotion-charts"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import * as echarts from "echarts";
import { graphic } from "echarts";
import API from "@/plugins/axiosInstance";

// var events = ref({
//   title: "美国完成首例脑机接口设备人体移植",
//   tags: ["马斯克", "美国"],
//   hot_value: "100",
//   time: "2024-2-1",
//   location: "美国",
//   source: "新浪微博",
//   media: "人民日报",
//   text: " 2024年1月30日，据外媒报道，美国知名企业家埃隆·马斯克29日表示，他旗下的脑机接口技术公司“神经连接”于28日进行了首例脑机接口设备的人体移植，移植者目前恢复良好。马斯克在社交媒体平台X上发帖称：“初步结果显示神经元尖峰检测很有前景。”",
// });
var events = ref({
  title: "",
  tags: [],
  hot_value: "",
  time: "",
  location: "",
  source: "",
  media: "",
  text: "",
});
var dataFlag = ref(false);
// 获取title
import { useStore } from "vuex";
const store = useStore();
function api_get_events_detail() {
  API({
    url: "/database/api_get_events_detail",
    method: "get",
    params: {
      title: store.state.title,
    },
  })
    .then((res) => {
      events.value = res.data;
    })
    .catch((error) => {
      console.log(error);
    });
}

// 情感分析
var events_emotion_data = ref([]);
function api_get_events_emotion() {
  return new Promise((resolve, reject) => {
    API({
      url: "/database/api_get_review_emotion",
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
var emotion_charts;
async function emotionChartsInit() {
  events_emotion_data.value = await api_get_events_emotion();
  emotion_charts = echarts.init(document.getElementById("emotion-charts"));
  let option;
  let isDark = true;
  option = {
    grid: {
      containLabel: true,
    },
    legend: {
      left: "center",
      data: ["积极", "消极"],
      bottom: 30,
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
          top: "28%",
          style: {
            text: "评论数量",
            textAlign: "center",
            fill: isDark ? "#ffffffb3" : "#4E5969",
            fontSize: 16,
          },
        },
        {
          type: "text",
          left: "center",
          top: "38%",
          style: {
            text: events_emotion_data.value.total,
            textAlign: "center",
            fill: isDark ? "#ffffffb3" : "#1D2129",
            fontSize: 20,
            fontWeight: 500,
          },
        },
      ],
    },
    series: [
      {
        type: "pie",
        radius: ["40%", "75%"],
        center: ["50%", "35%"],
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
var time_select_value = ref("1");
var time_select_options = [
  {
    label: "全部",
    value: "1",
  },
  {
    label: "12小时内",
    value: "12",
  },
  {
    label: "24小时内",
    value: "24",
  },
];
var heat_trend_charts;
watch(time_select_value, (newValue) => {
  heat_trend_charts.dispose();
  heatTrendChartsInit(newValue);
});
function api_get_hot_value(range_value = 1) {
  return new Promise((resolve, reject) => {
    API({
      url: "/database/api_get_hot_values_trend",
      method: "get",
      params: {
        title: store.state.title,
        range_value: range_value,
      },
    })
      .then((res) => {
        resolve(res.data);
        if (res.data.length == 0) {
          dataFlag.value = true;
        } else {
          dataFlag.value = false;
        }
        console.log(res.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

async function heatTrendChartsInit(range_value = 1) {
  console.log(111);
  let events_time_data = [];
  events_time_data = await api_get_hot_value(range_value);
  // 修改x轴日期格式
  let xdata = [];
  for (let i = 0; i < events_time_data.length; i++) {
    let date = new Date(events_time_data[i]["datetime"]);
    if (range_value != 1) {
      xdata.push(
        date.toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" })
      );
    } else {
      xdata.push(
        date.toLocaleDateString("zh-CN", { day: "2-digit", hour: "2-digit" })
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
  function formatter(v) {
    v = v.toString();
    if (Math.abs(v) >= 100000000) {
      return (v / 100000000).toFixed(1) + "亿";
    } else if (Math.abs(v) >= 10000) {
      return (v / 10000).toFixed(1) + "万";
    } else {
      return v;
    }
  }
  option = {
    grid: {
      left: "8%",
      right: "3%",
      top: "10%",
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
      axisLabel: {
        formatter(v) {
          v = v.toString();
          if (Math.abs(v) >= 100000000) {
            return (v / 100000000).toFixed(1) + "亿";
          } else if (Math.abs(v) >= 10000) {
            return (v / 10000).toFixed(1) + "万";
          } else {
            return v;
          }
        },
      },
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
          '<div style="display: flex;justify-content: space-between;padding: 0 9px;background: rgba(255,255,255,.8);width: 140px;height: 32px;line-height: 32px;box-shadow: 6px 0 20px #2257bc1a;border-radius: 4px;margin: 8px 0;"><span>热度值</span><span class="tooltip-value">' +
          formatter(firstElement.value)+
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

onMounted(() => {
  emotionChartsInit();
  heatTrendChartsInit();
  api_get_events_detail();
});
onBeforeUnmount(() => {
  emotion_charts.dispose();
  heat_trend_charts.dispose();
});
</script>

<style scoped>
.wrap-msg {
  width: calc(100% - 50px);
  /* height: 280px; */
  margin: 30px auto 40px auto;
}
/* 卡片 */
.wrap-card {
  width: 100%;
  border-radius: 20px;
  /* backdrop-filter: blur(20px); */
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
#emotion-charts {
  width: 100%;
  height: 310px;
}
#heat-trend-charts {
  width: 960px;
  height: 380px;
}
@media (max-width: 1600px) {
  #heat-trend-charts {
    width: 770px;
  }
}
:deep(.t-descriptions__header) {
  font-size: 18px;
}
:deep(.el-empty) {
  padding-top: 80px;
}
</style>