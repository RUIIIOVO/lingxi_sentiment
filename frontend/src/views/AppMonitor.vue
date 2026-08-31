<!-- 热搜监测 -->
<template>
  <div class="wrap-card">
    <div class="title">
      <div class="left-title">
        <div class="icon"><icon-dashboard /></div>
        <p>舆情监测</p>
      </div>
    </div>
    <a-grid
      :cols="24"
      :col-gap="12"
      :row-gap="12"
      style="width: 100%; height: 155px"
    >
      <a-grid-item :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 6, xxl: 6 }">
        <div
          class="msg-card"
          style="background: linear-gradient(135deg, #003d74, #3271ae)"
        >
          <div style="width: 100%">
            <div class="msg-card-title">监测总数</div>
            <div class="flex-align-items-center">
              <a-statistic
                :value="monitorListProceed.length"
                show-group-separator
                animation
                :value-style="{
                  color: 'rgba(255, 255, 255, 0.9)',
                  fontSize: '30px',
                }"
              />
              <span class="msg-card-value">条</span>
            </div>
          </div>
          <div id="line_charts1"></div>
        </div>
      </a-grid-item>
      <a-grid-item :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 6, xxl: 6 }">
        <div
          class="msg-card"
          style="background: linear-gradient(135deg, #3271ae, #0f5f8e)"
        >
          <div style="float: left">
            <div class="msg-card-title">最新预警数量</div>
            <div class="flex-align-items-center">
              <a-statistic
                :value="alarm_activities.length"
                show-group-separator
                animation
                :value-style="{
                  color: 'rgba(255, 255, 255, 0.9)',
                  fontSize: '30px',
                }"
              />
              <span class="msg-card-value">条</span>
            </div>
          </div>
          <div id="bar_charts"></div>
        </div>
      </a-grid-item>
      <a-grid-item :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 6, xxl: 6 }">
        <div
          class="msg-card"
          style="background: linear-gradient(135deg, #0f5f8e, #213180)"
        >
          <div style="float: left">
            <div class="msg-card-title">消极预警数量</div>
            <div class="flex-align-items-center">
              <a-statistic
                :value="negativeEmotionCount"
                show-group-separator
                animation
                :value-style="{
                  color: 'rgba(255, 255, 255, 0.9)',
                  fontSize: '30px',
                }"
              />
              <span class="msg-card-value">条</span>
            </div>
          </div>
          <div id="line_charts2"></div>
        </div>
      </a-grid-item>
      <a-grid-item :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 6, xxl: 6 }">
        <div
          class="msg-card"
          style="background: linear-gradient(135deg, #003d74, #4a4b9d)"
        >
          <div style="float: left">
            <div class="msg-card-title">预警频率</div>
            <div class="flex-align-items-center">
              <a-statistic
                :value="60"
                show-group-separator
                animation
                :value-style="{
                  color: 'rgba(255, 255, 255, 0.9)',
                  fontSize: '30px',
                }"
              />
              <span class="msg-card-value">秒/次</span>
            </div>
          </div>
          <div id="gauge_charts"></div>
        </div>
      </a-grid-item>
    </a-grid>
    <div class="content">
      <div class="flex-space-between" style="height: 100%; flex-shrink: 0">
        <div class="content-card">
          <p class="content-card-title">最新预警</p>
          <el-scrollbar height="calc(100% - 55px)">
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
                <t-tag
                  :theme="activity.emotion == '积极' ? 'primary' : 'danger'"
                  variant="light"
                  style="margin-right: 8px"
                  v-if="activity.emotion != null"
                  >{{ activity.emotion }}</t-tag
                >
                <span v-html="highlightKeyword(activity)"></span>
              </el-timeline-item>
            </el-timeline>
          </el-scrollbar>
        </div>
        <div class="content-card" style="width: calc(75% - 48px)">
          <el-button type="primary" class="addBtn" :icon="Plus" @click="addShow"
            >新增预警</el-button
          >
          <t-tabs
            :default-value="1"
            class="wrap-tabs"
            :lazy="true"
            style="height: 100%"
          >
            <t-tab-panel
              :value="1"
              label="全部"
              style="height: calc(100% - 80px)"
            >
              <el-scrollbar max-height="100%">
                <div v-if="!dataEmptyFlag1">
                  <div
                    class="warn"
                    v-for="(item, index) in monitorList"
                    :key="index"
                  >
                    <div class="flex-space-between">
                      <div class="warn-top">
                        <p class="warn-title" @click="detailShow(item.keyword)">
                          {{ item.keyword }}
                        </p>
                        <el-tag type="danger" v-if="item.status == '1'"
                          >监测中</el-tag
                        >
                        <el-tag plain v-if="item.status == '0'">已结束</el-tag>
                      </div>
                      <div>
                        <el-button
                          type="primary"
                          :icon="List"
                          size="small"
                          @click="detailShow(item.keyword)"
                          >详情</el-button
                        >
                      </div>
                    </div>
                    <div class="warn-detial flex-space-between">
                      <div>
                        <div>
                          <span class="warn-detial-title">平台:</span
                          ><span v-for="(s, i) in item.source" :key="i">{{
                            s + " "
                          }}</span>
                        </div>
                        <div>
                          <span class="warn-detial-title">时间:</span
                          ><span>{{ item.time }}</span>
                        </div>
                      </div>
                      <div>
                        <el-button
                          type="primary"
                          :icon="Delete"
                          size="small"
                          @click="deleteShow(item.keyword)"
                          >删除</el-button
                        >
                      </div>
                    </div>
                  </div>
                </div>
                <el-empty v-if="dataEmptyFlag1" description="暂无预警" />
              </el-scrollbar>
            </t-tab-panel>
            <t-tab-panel
              :value="2"
              label="监测中"
              style="height: calc(100% - 80px)"
            >
              <el-scrollbar max-height="100%">
                <div v-if="!dataEmptyFlag2">
                  <div
                    class="warn"
                    v-for="(item, index) in monitorListProceed"
                    :key="index"
                  >
                    <div class="flex-space-between">
                      <div class="warn-top">
                        <p class="warn-title" @click="detailShow(item.keyword)">
                          {{ item.keyword }}
                        </p>
                        <el-tag type="danger" v-if="item.status == '1'"
                          >监测中</el-tag
                        >
                        <el-tag plain v-if="item.status == '0'">已结束</el-tag>
                      </div>
                      <div>
                        <el-button
                          type="primary"
                          :icon="List"
                          size="small"
                          @click="detailShow(item.keyword)"
                          >详情</el-button
                        >
                      </div>
                    </div>
                    <div class="warn-detial flex-space-between">
                      <div>
                        <div>
                          <span class="warn-detial-title">平台:</span
                          ><span v-for="(s, i) in item.source" :key="i">{{
                            s + " "
                          }}</span>
                        </div>
                        <div>
                          <span class="warn-detial-title">时间:</span
                          ><span>{{ item.time }}</span>
                        </div>
                      </div>
                      <div>
                        <el-button
                          type="primary"
                          :icon="Delete"
                          size="small"
                          @click="deleteShow(item.keyword)"
                          >删除</el-button
                        >
                      </div>
                    </div>
                  </div>
                </div>
                <el-empty v-if="dataEmptyFlag2" description="暂无预警" />
              </el-scrollbar>
            </t-tab-panel>
            <t-tab-panel
              :value="3"
              label="已结束"
              style="height: calc(100% - 80px)"
            >
              <el-scrollbar max-height="100%">
                <div v-if="!dataEmptyFlag3">
                  <div
                    class="warn"
                    v-for="(item, index) in monitorListEnd"
                    :key="index"
                  >
                    <div class="flex-space-between">
                      <div class="warn-top">
                        <p class="warn-title" @click="detailShow(item.keyword)">
                          {{ item.keyword }}
                        </p>
                        <el-tag type="danger" v-if="item.status == '1'"
                          >监测中</el-tag
                        >
                        <el-tag plain v-if="item.status == '0'">已结束</el-tag>
                      </div>
                      <div>
                        <el-button
                          type="primary"
                          :icon="List"
                          size="small"
                          @click="detailShow(item.keyword)"
                          >详情</el-button
                        >
                      </div>
                    </div>
                    <div class="warn-detial flex-space-between">
                      <div>
                        <div>
                          <span class="warn-detial-title">平台:</span
                          ><span v-for="(s, i) in item.source" :key="i">{{
                            s + " "
                          }}</span>
                        </div>
                        <div>
                          <span class="warn-detial-title">时间:</span
                          ><span>{{ item.time }}</span>
                        </div>
                      </div>
                      <div>
                        <el-button
                          type="primary"
                          :icon="Delete"
                          size="small"
                          @click="deleteShow(item.keyword)"
                          >删除</el-button
                        >
                      </div>
                    </div>
                  </div>
                </div>
                <div v-if="dataEmptyFlag3">
                  <el-empty description="暂无预警" />
                </div>
              </el-scrollbar>
            </t-tab-panel>
          </t-tabs>
        </div>
      </div>
    </div>
  </div>
  <!-- 详情 -->
  <el-dialog v-model="detailVisible" title="详情" width="500" align-center>
    <!-- <p class="detail-title" style="margin-top:0">预警概述</p> -->
    <el-descriptions column="1" border>
      <el-descriptions-item label="预警关键词">{{
        detailObj.keyword
      }}</el-descriptions-item>
      <el-descriptions-item label="预警状态">
        <el-tag type="danger" v-if="detailObj.status == '1'">监测中</el-tag>
        <el-tag plain v-if="detailObj.status == '0'">已结束</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="预警时间">{{
        detailObj.time
      }}</el-descriptions-item>
      <el-descriptions-item label="预警平台"
        ><span v-for="(s, i) in detailObj.source" :key="i">{{
          s + " "
        }}</span></el-descriptions-item
      >
    </el-descriptions>
    <p class="detail-title">历史预警</p>
    <el-scrollbar max-height="200px">
      <a-empty v-if="detail_alarm_flag">
        <template #image>
          <icon-empty />
        </template>
        <p style="margin-top: 10px; color: rgb(255, 255, 255, 0.7)">
          暂无预警数据
        </p>
      </a-empty>
      <el-timeline
        v-if="!detail_alarm_flag"
        style="margin-left: 5px; margin-top: 6px"
      >
        <el-timeline-item
          v-for="(activity, index) in detail_alarm_activities"
          :key="index"
          :icon="activity.icon"
          :type="activity.type"
          :color="activity.color"
          :size="activity.size"
          :hollow="activity.hollow"
          :timestamp="activity.timestamp"
        >
          <t-tag theme="primary" variant="outline" style="margin-right: 8px">{{
            activity.source
          }}</t-tag>
          <t-tag
            :theme="activity.emotion == '积极' ? 'primary' : 'danger'"
            variant="light"
            style="margin-right: 8px;margin-bottom:2px;"
            v-if="activity.emotion != null"
            >{{ activity.emotion }}</t-tag
          >
          <span v-html="highlightKeyword(activity)"></span>
        </el-timeline-item>
      </el-timeline>
    </el-scrollbar>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" plain @click="detailVisible = false"
          >确认</el-button
        >
      </div>
    </template>
  </el-dialog>
  <!-- 确认删除 -->
  <el-dialog
    v-model="deleteVisible"
    title="确认删除"
    width="300"
    align-center
    center
  >
    <p style="text-align: center">是否确定删除预警?</p>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="deleteVisible = false">取消</el-button>
        <el-button type="primary" @click="deleteOK"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
  <!-- 新增预警 -->
  <el-dialog
    v-model="addVisible"
    title="新增预警"
    width="500"
    align-center
    center
  >
    <el-form :model="form" label-width="auto" style="max-width: 600px">
      <el-form-item label="预警关键词">
        <el-input v-model="form.keyword" placeholder="请输入预警关键词" />
      </el-form-item>
      <el-form-item label="预警时间">
        <el-col :span="11">
          <el-date-picker
            v-model="form.time1"
            type="date"
            placeholder="请输入开始时间"
            style="width: 100%"
          />
        </el-col>
        <el-col :span="2" class="text-center">
          <span class="text-gray-500" style="margin-left: 10px">-</span>
        </el-col>
        <el-col :span="11">
          <el-date-picker
            v-model="form.time2"
            type="date"
            placeholder="请输入结束时间"
            style="width: 100%"
          />
        </el-col>
      </el-form-item>
      <el-form-item label="预警平台">
        <el-checkbox
          v-model="checkAll"
          :indeterminate="isIndeterminate"
          @change="handleCheckAllChange"
          style="margin-right: 20px"
          >全选</el-checkbox
        >
        <el-checkbox-group
          v-model="checked_tags"
          @change="handleCheckedCitiesChange"
        >
          <el-checkbox v-for="tag in tags" :key="tag" :label="tag">{{
            tag
          }}</el-checkbox>
        </el-checkbox-group>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="addVisible = false">取消</el-button>
        <el-button type="primary" @click="addOK"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import * as echarts from "echarts";
import { onMounted, onBeforeUnmount, ref, watch } from "vue";

function generateLineRandomData(num) {
  return Array.from({ length: num }, () => Math.floor(Math.random() * 100));
}
var line_charts1;
var dataNum = 16; // 增加数据点数量
if (window.innerWidth <= 1600) {
  dataNum = 13; // 增加数据点数量
}
function lineCharts1Init() {
  line_charts1 = echarts.init(document.getElementById("line_charts1"));

  let option;
  let smoothValue = 0.5; // 调整 smooth 参数

  function generateSeriesData() {
    return generateLineRandomData(dataNum);
  }

  option = {
    grid: {
      left: 0,
      right: 0,
      top: 15,
      bottom: 0,
    },
    xAxis: {
      type: "category",
      show: false,
    },
    yAxis: {
      show: false,
    },
    tooltip: {
      show: false,
    },
    series: [
      {
        data: generateSeriesData(),
        type: "line",
        showSymbol: false,
        smooth: smoothValue,
        lineStyle: {
          color: "#aed0ee",
          width: 3,
          type: "dashed",
        },
      },
    ],
  };
  option && line_charts1.setOption(option);
}
var line_charts2;
function lineCharts2Init() {
  line_charts2 = echarts.init(document.getElementById("line_charts2"));

  let option;
  let smoothValue = 0.5; // 调整 smooth 参数

  function generateSeriesData() {
    return generateLineRandomData(dataNum);
  }

  option = {
    grid: {
      left: 0,
      right: 0,
      top: 15,
      bottom: 0,
    },
    xAxis: {
      type: "category",
      show: false,
    },
    yAxis: {
      show: false,
    },
    tooltip: {
      show: false,
    },
    series: [
      {
        data: generateSeriesData(),
        type: "line",
        showSymbol: false,
        smooth: smoothValue,
        lineStyle: {
          color: "#aed0ee",
          width: 3,
          type: "dashed",
        },
      },
    ],
  };
  option && line_charts2.setOption(option);
}

function generateBarRandomData(dataNum) {
  let data = [];
  for (let i = 0; i < dataNum; i++) {
    let value = Math.floor(Math.random() * 81) + 20; // 生成20到100之间的随机数
    data.push(value);
  }
  return data;
}
var bar_charts;
function barChartsInit() {
  bar_charts = echarts.init(document.getElementById("bar_charts"));

  let option;
  option = {
    grid: {
      left: 0,
      right: 0,
      top: 10,
      bottom: 0,
    },
    xAxis: {
      type: "category",
      show: false,
    },
    yAxis: {
      show: false,
    },
    tooltip: {
      show: false,
      // trigger: "axis",
    },
    series: {
      name: "total",
      data: generateBarRandomData(dataNum),
      type: "bar",
      barWidth: 7,
      itemStyle: {
        borderRadius: 2,
        // 使用条件判断设置颜色
        color: function (params) {
          return params.dataIndex % 2 === 0 ? "#30baf7" : "#aed0ee";
        },
      },
    },
  };
  option && bar_charts.setOption(option);
}

var gauge_charts;
function gaugeChartsInit() {
  gauge_charts = echarts.init(document.getElementById("gauge_charts"));
  let option;
  option = {
    series: [
      {
        type: "gauge",
        radius: "140%",
        center: ["50%", "75%"],
        startAngle: 180,
        endAngle: 0,
        min: 0,
        max: 15,
        splitNumber: 4,
        itemStyle: {
          color: "#a1d3ff",
        },
        progress: {
          show: true,
          roundCap: true,
          width: 10,
        },
        pointer: {
          icon: "path://M2090.36389,615.30999 L2090.36389,615.30999 C2091.48372,615.30999 2092.40383,616.194028 2092.44859,617.312956 L2096.90698,728.755929 C2097.05155,732.369577 2094.2393,735.416212 2090.62566,735.56078 C2090.53845,735.564269 2090.45117,735.566014 2090.36389,735.566014 L2090.36389,735.566014 C2086.74736,735.566014 2083.81557,732.63423 2083.81557,729.017692 C2083.81557,728.930412 2083.81732,728.84314 2083.82081,728.755929 L2088.2792,617.312956 C2088.32396,616.194028 2089.24407,615.30999 2090.36389,615.30999 Z",
          length: "80%",
          width: 8,
          offsetCenter: [0, "5%"],
        },
        axisLine: {
          roundCap: true,
          lineStyle: {
            width: 10,
          },
        },
        axisTick: {
          // splitNumber: 2,
          lineStyle: {
            width: 2,
            color: "#999",
          },
        },
        splitLine: {
          length: 8,
          lineStyle: {
            width: 2,
            color: "#999",
          },
        },
        axisLabel: {
          show: false,
          distance: 10,
          color: "#999",
          fontSize: 10,
        },
        title: {
          show: false,
        },
        detail: {
          show: false,
        },
        data: [
          {
            value: 10,
          },
        ],
      },
    ],
  };
  option && gauge_charts.setOption(option);
}

// 引入user_id
import { useStore } from "vuex";
const store = useStore();
var user_id = ref(store.state.user_id);
var negativeEmotionCount = ref(0);
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
      let formattedTimestamp =
        timestamp.getFullYear() +
        "-" +
        (timestamp.getMonth() +
        1) +
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
      negativeEmotionCount.value = alarm_activities.value.filter(
        (activity) => activity.emotion === "消极"
      ).length;
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

import { Plus, Delete, List } from "@element-plus/icons-vue";

var monitorList = ref([]);
// var monitorList = ref([
//   {
//     keyword: "哇哈哈",
//     status: "1",
//     source: ["新浪微博", "抖音"],
//     time: "2024-03-05 16:31 - 2024-03-06 16:31",
//   },
// ]);

// 分类数据，1为监测中，0为已结束
var monitorListProceed = ref([]);
var monitorListEnd = ref([]);

var dataEmptyFlag1 = ref(false);
var dataEmptyFlag2 = ref(false);
var dataEmptyFlag3 = ref(false);

function api_get_total_monitor() {
  API({
    url: "/monitor/api_get_total_monitor",
    method: "get",
    params: {
      user_id: user_id.value,
    },
  }).then((res) => {
    monitorList.value = [];
    monitorListProceed.value = [];
    monitorListEnd.value = [];
    res.data.forEach((element) => {
      monitorList.value.unshift(element); // 逆序插入
    });

    // 分类数据，1为监测中，0为已结束
    monitorListProceed.value = monitorList.value.filter(
      (item) => item.status === "1"
    );
    monitorListEnd.value = monitorList.value.filter(
      (item) => item.status === "0"
    );

    // 初始化设置空状态
    if (monitorList.value.length == 0) {
      dataEmptyFlag1.value = true;
    } else {
      dataEmptyFlag1.value = false;
    }
    if (monitorListProceed.value.length == 0) {
      dataEmptyFlag2.value = true;
    } else {
      dataEmptyFlag2.value = false;
    }
    if (monitorListEnd.value.length == 0) {
      dataEmptyFlag3.value = true;
    } else {
      dataEmptyFlag3.value = false;
    }
  });
}

// 详情
var detailObj = ref({});
var detailVisible = ref(false);
var detail_alarm_activities = ref([]);
var detail_alarm_flag = ref(false);
function detailShow(keyword) {
  detailVisible.value = true;
  monitorList.value.forEach((element) => {
    if (element.keyword == keyword) {
      detailObj.value = element;
    }
  });
  API({
    url: "/monitor/api_get_one_alarm_msg",
    method: "get",
    params: {
      keyword: keyword,
      user_id: user_id.value,
    },
  }).then((res) => {
    console.log(res);
    detail_alarm_activities.value = [];
    if (res.data.length == 0) {
      detail_alarm_flag.value = true;
    } else {
      detail_alarm_flag.value = false;
    }
    res.data.forEach((element) => {
      let timestamp = new Date(element[2]);
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
      detail_alarm_activities.value.unshift(obj);
    });
  });
}

// 删除
import { MessagePlugin } from "tdesign-vue-next";
var deleteKeyword = ref("");
var deleteVisible = ref(false);
function deleteShow(keyword) {
  deleteVisible.value = true;
  deleteKeyword.value = keyword;
}
function deleteOK() {
  API({
    url: "/monitor/api_delete_monitor",
    method: "get",
    params: {
      keyword: deleteKeyword.value,
      user_id: user_id.value,
    },
  })
    .then(() => {
      MessagePlugin.success("删除成功");
      api_get_total_monitor();
      api_get_alarm_msg();
    })
    .catch(() => {
      MessagePlugin.error("删除失败");
    });
  deleteVisible.value = false;
}

// 标签选择
const checkAll = ref(false);
const isIndeterminate = ref(false);
const checked_tags = ref([]);
const tags = ["新浪微博", "百度", "抖音", "今日头条", "知乎", "微信"];
const handleCheckAllChange = (val) => {
  checked_tags.value = val ? tags : [];
  isIndeterminate.value = false;
};
const handleCheckedCitiesChange = (value) => {
  const checkedCount = value.length;
  checkAll.value = checkedCount === tags.length;
  isIndeterminate.value = checkedCount > 0 && checkedCount < tags.length;
};

// 新增预警
var addVisible = ref(false);
function addShow() {
  console.log(user_id.value);
  if (user_id.value != undefined && user_id.value != "0") {
    addVisible.value = true;
  } else {
    MessagePlugin.warning("请在登录后使用该功能");
  }
}

const form = ref({
  user_id: user_id,
  keyword: "",
  time1: "",
  time2: "",
  source: checked_tags,
});
function addOK() {
  // 检查表单是否有空值
  const hasEmptyValue = Object.values(form.value).some((value) => value === "");
  // 检查source字段是否为空
  const isSourceEmpty = checked_tags.value.length === 0;

  // 检查时间逻辑
  const time1 = new Date(form.value.time1);
  const time2 = new Date(form.value.time2);
  const isValidTime = time2 > time1 && time1.getTime() !== time2.getTime();

  if (hasEmptyValue || isSourceEmpty) {
    MessagePlugin.error("请完整填写表单");
  } else if (!isValidTime) {
    MessagePlugin.error("起始时间不能重复，请重新选择");
  } else {
    console.log(form.value);
    API({
      url: "/monitor/api_add_monitor/",
      method: "post",
      data: form.value,
    })
      .then((res) => {
        if(res.data.code==200){
          MessagePlugin.success("新建成功");
          api_get_total_monitor();
        }else{
          MessagePlugin.error("该关键词已存在");
        }
        checkAll.value = false;
      })
      .catch(() => {
        MessagePlugin.error("该关键词已存在");
        checkAll.value = false;
      });
    checked_tags.value = [];
    form.value.keyword = "";
    form.value.time1 = "";
    form.value.time2 = "";
    form.value.source = checked_tags;
    // form.value = {
    //   keyword: "",
    //   time1: "",
    //   time2: "",
    //   source: checked_tags,
    //   user_id:user_id,
    // };
    addVisible.value = false;
  }
}

watch(
  store.state,
  () => {
    user_id.value = store.state.user_id;
    api_get_alarm_msg();
    api_get_total_monitor();
  },
  { deep: true }
);

// 设置空状态
watch(monitorList.value.length, () => {
  if (monitorList.value.length == 0) {
    dataEmptyFlag1.value = true;
  } else {
    dataEmptyFlag1.value = false;
  }
});

watch(monitorListProceed.value.length, () => {
  if (monitorListProceed.value.length == 0) {
    dataEmptyFlag2.value = true;
  } else {
    dataEmptyFlag2.value = false;
  }
});

watch(monitorListEnd.value.length, () => {
  if (monitorListEnd.value.length == 0) {
    dataEmptyFlag3.value = true;
  } else {
    dataEmptyFlag3.value = false;
  }
});

onMounted(() => {
  lineCharts1Init();
  lineCharts2Init();
  barChartsInit();
  gaugeChartsInit();
  api_get_alarm_msg();
  api_get_total_monitor();
});
onBeforeUnmount(() => {
  line_charts1.dispose();
  line_charts2.dispose();
  bar_charts.dispose();
  gauge_charts.dispose();
});
</script>

<style scoped >
/* 卡片 */
.wrap-card {
  height: calc(100% - 40px);
  position: relative;
  color: rgb(255, 255, 255, 0.86);
}
/* 卡片标题 */
.wrap-card .title {
  width: calc(100% - 10px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 20px;
  z-index: 20;
  margin: 5px 5px 15px 5px;
}
.wrap-card .left-title {
  display: flex;
  align-items: center;
}
.wrap-card .right-title {
  font-size: 14px;
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
.wrap-card .top {
  width: calc(100% - 40px);
  height: 120px;
  margin-bottom: 35px;
  border-radius: 10px;
  backdrop-filter: blur(20px);
}
.top-title {
  font-size: 16px;
}
.wrap-card .top-title {
  margin-right: 16px;
  white-space: nowrap;
}
.wrap-card .content {
  margin-top: 10px;
  height: calc(100% - 190px);
}
.footer {
  width: calc(100% - 14px);
  position: absolute;
  bottom: 10px;
}
/* 顶部信息栏 */
.msg-card {
  width: calc(100% - 40px);
  background: linear-gradient(135deg, #003d74, #4a4b9d);
  height: 100px;
  border-radius: 10px;
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}
.msg-card-title {
  color: rgba(255, 255, 255, 0.85);
  font-size: 20px;
  font-weight: bold;
  white-space: nowrap;
  margin-top: 6px;
  margin-bottom: 14px;
}
.msg-card-value {
  color: rgba(255, 255, 255, 0.9);
  font-size: 24px;
  padding-left: 5px;
  padding-top: 1px;
  white-space: nowrap;
}
#line_charts1 {
  width: 200px;
  height: 90px;
  z-index: 20;
}
#line_charts2 {
  width: 180px;
  height: 90px;
  z-index: 20;
}
#bar_charts {
  width: 180px;
  height: 90px;
  z-index: 20;
}
#gauge_charts {
  width: 180px;
  height: 110px;
  z-index: 20;
}
@media (max-width: 1600px) {
  #line_charts1 {
    width: 180px;
  }
  #line_charts2 {
    width: 130px;
  }
  #bar_charts {
    width: 130px;
  }
}
/* 预警信息 */
.content-card {
  width: calc(25% - 51px);
  height: calc(100% - 30px);
  padding: 10px 20px 20px 20px;
  border-radius: 10px;
  backdrop-filter: blur(20px);
  background-color: #202021;
  border: 1px solid #2d2e2f;
  position: relative;
}
.content-card-title {
  font-size: 18px;
  font-weight: 600;
  margin-top: 14px;
  margin-bottom: 20px;
}
.addBtn {
  position: absolute;
  right: 20px;
  top: 15px;
  z-index: 20;
}
:deep .t-tabs {
  background-color: #202021;
}
/* 我的预警 */
.warn {
  width: calc(100% - 20px);
  height: 90px;
  padding: 10px;
  border-bottom: 1px solid rgba(128, 128, 128, 0.6);
}
.warn-top {
  display: flex;
  align-items: center;
  height: 40px;
}
.warn-title {
  font-size: 16px;
  margin-right: 10px;
  cursor: pointer;
}
.warn-detial {
  font-size: 12px;
  color: #999;
}
.warn-detial-title {
  color: rgb(189, 189, 189);
  margin-right: 10px;
}
:deep(.el-empty) {
  padding-top: 12%;
}
:deep(.t-tabs__content, .t-tab-panel) {
  width: 100%;
  height: calc(100% + 30px);
}
:deep(.el-descriptions__label) {
  white-space: nowrap;
}
.detail-title {
  font-size: 16px;
  font-weight: 600;
  margin: 24px 0;
}
/* :deep(.t-timeline-item__wrapper) {
  margin-left: 70px !important;
} */
:deep(.t-timeline-item__label) {
  font-size: 12px !important;
  margin-top: 4px;
}
</style>