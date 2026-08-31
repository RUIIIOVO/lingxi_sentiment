<!-- 事件库 -->
<template>
  <div class="wrap-card">
    <div class="title">
      <div class="left-title">
        <div class="icon"><icon-storage /></div>
        <p>事件库</p>
      </div>
      <div class="right-title">
        <p>事件数量：{{ totalNum }}条</p>
      </div>
    </div>
    <div class="choose">
      <div class="flex-space-between" style="margin-bottom: 20px">
        <div class="flex-space-between">
          <p class="choose-title">事件库</p>
          <el-radio-group v-model="database_choose" class="ml-4">
            <el-radio label="0">热门事件库</el-radio>
            <el-radio label="1">自定义事件库</el-radio>
          </el-radio-group>
        </div>
        <div class="flex-space-between">
          <p class="choose-title">排序方式</p>
          <el-select
            v-model="sort_value"
            class="m-2"
            placeholder="请选择排序方式"
            style="width: 240px"
          >
            <el-option
              v-for="item in sort_options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
        <div class="flex-space-between">
          <p class="choose-title">时间</p>
          <el-date-picker
            v-model="time_value"
            type="daterange"
            unlink-panels
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            :shortcuts="shortcuts"
          />
        </div>
        <div class="flex-space-between">
          <p class="choose-title">搜索</p>
          <el-input
            v-model="search_value"
            class="w-50 m-2"
            placeholder="请输入事件名称"
            :suffix-icon="Search"
            @keydown.enter="submit"
          />
        </div>
      </div>
      <div class="flex-space-between">
        <div style="display: flex; align-items: center">
          <p class="choose-title">标签</p>
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
        </div>
        <el-button type="primary" @click="clickSubmit">查询</el-button>
      </div>
    </div>
    <div class="content">
      <el-empty description="暂无数据" v-if="dataFlag" />
      <el-scrollbar height="100%" v-if="!dataFlag">
        <div
          class="event flex-space-between"
          v-for="(event, index) in events"
          :key="index"
        >
          <div class="event-left-side">
            <div class="event-icon">{{ event.title.slice(0, 1) }}</div>
            <div>
              <div style="display: flex; align-items: center">
                <div class="event-title" @click="gotoDetail(event.title)">
                  {{ event.title }}
                </div>
                <el-tag
                  style="margin-left: 10px; cursor: pointer"
                  v-for="(tag, index) in event.tags"
                  :key="index"
                  >{{ tag }}</el-tag
                >
              </div>
              <div class="event-text" @click="gotoDetail(event.title)">
                {{ event.text }}
              </div>
            </div>
          </div>
          <div class="event-right-side">
            <div class="event-hot-value-title">热度值</div>
            <div class="event-hot-value">{{ event.hot_value }}</div>
            <div class="event-time">{{ event.time }}</div>
          </div>
        </div>
      </el-scrollbar>
      <t-space class="footer" direction="vertical">
        <t-pagination
          v-model="current"
          :total="totalNum"
          size="small"
          v-model:pageSize="pageSize"
        />
      </t-space>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { Search } from "@element-plus/icons-vue";
var dataFlag = ref(false);
// 事件库选择
var database_choose = ref("0");
// 排序方式选项
// var sort_value = ref("hot_down");
var sort_value = ref("time_down");
const sort_options = [
  {
    value: "time_down",
    label: "按时间降序",
  },
  {
    value: "time_up",
    label: "按时间升序",
  },
  {
    value: "hot_down",
    label: "按热度降序",
  },
  {
    value: "hot_up",
    label: "按热度升序",
  },
];
// 时间选择
var time_value = ref("");
// const shortcuts = [
//   {
//     text: "近一周",
//     value: () => {
//       const end = new Date();
//       const start = new Date();
//       start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
//       return [start, end];
//     },
//   },
//   {
//     text: "近一个月",
//     value: () => {
//       const end = new Date();
//       const start = new Date();
//       start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
//       return [start, end];
//     },
//   },
//   {
//     text: "近三个月",
//     value: () => {
//       const end = new Date();
//       const start = new Date();
//       start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
//       return [start, end];
//     },
//   },
// ];
const shortcuts = [
  {
    text: "近一周",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setHours(0, 0, 0, 0); // 将小时、分钟、秒和毫秒设置为0
      start.setDate(end.getDate() - 7); // 减去7天
      return [start, end];
    },
  },
  {
    text: "近一个月",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setHours(0, 0, 0, 0); // 将小时、分钟、秒和毫秒设置为0
      start.setMonth(end.getMonth() - 1); // 减去1个月
      return [start, end];
    },
  },
  {
    text: "近三个月",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setHours(0, 0, 0, 0); // 将小时、分钟、秒和毫秒设置为0
      start.setMonth(end.getMonth() - 3); // 减去3个月
      return [start, end];
    },
  },
];

// 搜索框
var search_value = ref("");
// 标签选择
const checkAll = ref(true);
const isIndeterminate = ref(false);
const checked_tags = ref([
  "社会新闻",
  "财经",
  "教育",
  "灾难",
  "综艺",
  "艺人",
  "演出",
  "电影",
  "体育",
  "情感",
  "数码",
  "幽默",
  "电竞",
]);
const tags = [
  "社会新闻",
  "财经",
  "教育",
  "灾难",
  "综艺",
  "艺人",
  "演出",
  "电影",
  "体育",
  "情感",
  "数码",
  "幽默",
  "电竞",
];


import API from "@/plugins/axiosInstance";
var events = ref([]);
// 当前页码
var pageSize = ref(5);
var current = ref(1);
// 数据总数，用于设置分页
var totalNum = ref(100);
// 查询表单
var search_form = ref({
  database_choose: database_choose,
  sort_value: sort_value,
  time_value: time_value,
  search_value: search_value,
  checked_tags: checked_tags,
  check_all:checkAll.value,
  isIndeterminate:isIndeterminate.value,
  pageSize: pageSize,
  current: current,
});

// watch(
//   search_form.value,
//   () => {
//     submit();
//   }
// );

const handleCheckAllChange = (val) => {
  checked_tags.value = val ? tags : [];
  isIndeterminate.value = false;
  search_form.value.check_all = checkAll.value;
  search_form.value.isIndeterminate = isIndeterminate.value;
};

const handleCheckedCitiesChange = (value) => {
  const checkedCount = value.length;
  checkAll.value = checkedCount === tags.length;
  isIndeterminate.value = checkedCount > 0 && checkedCount < tags.length;
  search_form.value.check_all = checkAll.value;
  search_form.value.isIndeterminate = isIndeterminate.value;
};

function submit() {
  console.log(search_form.value);
  API({
    url: "/database/api_search_events/",
    method: "post",
    data: search_form.value,
  })
    .then((res) => {
      console.log(res);
      events.value = [];
      res.data.data.forEach((e) => {
        events.value.push(e);
      });
      totalNum.value = res.data.total_count;
      if(totalNum.value==0){
        dataFlag.value = true;
      }else{
        dataFlag.value = false;
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function clickSubmit() {
  current.value = 1;
  submit();
}

onMounted(() => {
  submit();
});
watch([pageSize, current], () => {
  // if (search_value.value) current.value = 1;
  submit(); 
});

import { useRouter } from "vue-router";
import { useStore } from "vuex";
const store = useStore();
const router = useRouter();
function gotoDetail(title) {
  store.commit("updateTitle", title);
  router.push({
    path: "/AppDetail",
  });
}
</script>

<style scoped>
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
  margin: 10px 5px 20px 5px;
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
.wrap-card .choose {
  width: calc(100% - 40px);
  height: 90px;
  padding: 20px;
  margin-bottom: 10px;
  border-radius: 10px;
  backdrop-filter: blur(20px);
  background-color: #282828;
  border: 1px solid #2d2e2f;
}
.wrap-card .choose-title {
  margin-right: 16px;
  white-space: nowrap;
}
.wrap-card .content {
  width: calc(100% - 40px);
  height: calc(100% - 207px);
  padding: 10px 20px 40px 20px;
  border-radius: 10px;
  backdrop-filter: blur(20px);
  background-color: #202021;
  border: 1px solid #2d2e2f;
  position: relative;
}
.footer {
  width: calc(100% - 14px);
  position: absolute;
  bottom: 10px;
}
/* 事件列表 */
.event {
  width: 98%;
  height: 130px;
  border-bottom: 1px solid rgba(128, 128, 128, 0.6);
}
.event-left-side {
  display: flex;
  align-items: center;
  justify-content: baseline;
  margin-left: 10px;
}
.event-icon {
  width: 70px;
  min-width: 70px;
  height: 70px;
  margin: 15px;
  margin-right: 25px;
  border-radius: 50px;
  background-color: #409eff;
  color: rgba(255, 255, 255, 0.9);
  font-size: 34px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.event-title {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 1.3px;
  cursor: pointer;
}
.event-text {
  /* width: 85%; */
  /* min-width: 70%; */
  margin-top: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: rgba(255, 255, 255, 0.85);
  line-height: 20px;
  cursor: pointer;
}
.event-right-side {
  text-align: center;
  margin: -12px 10px 0 80px;
}
.event-hot-value {
  width: 180px;
  min-width: 180px;
  font-size: 32px;
  font-weight: 600;
  color: #409eff;
  background-image: -webkit-linear-gradient(279deg, #0396ff, #abdcff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 8px 0 10px 0;
}
.event-hot-value-title {
  font-size: 16px;
}
.event-time {
  font-size: 14px;
}
:deep(.el-empty) {
  padding-top: 10%;
}
</style>