<!-- 事件脉络 -->
<template>
  <div class="main">
    <div class="head-title flex-space-between">
      <div class="sort-button" @click="changeSort">
        <el-icon :size="18"><Sort /></el-icon>
        <span style="margin-left: 6px">{{ sort_tip }}</span>
      </div>
      <span class="time">更新至{{ update_time }}</span>
    </div>
    <el-scrollbar class="wrap-event-activities" >
      <el-timeline style="margin-left: 5px">
        <el-timeline-item
          v-for="(event, index) in event_activities"
          :key="index"
          :icon="event.icon"
          :type="event.type"
          :color="event.color"
          :size="event.size"
          :hollow="event.hollow"
          :timestamp="event.timestamp"
        >
          <p>{{ event.content }}</p>
        </el-timeline-item>
      </el-timeline>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import API from "@/plugins/axiosInstance";
// 获取title
import { useStore } from "vuex";
const store = useStore();

var sort_tip = ref("时间升序");
function changeSort() {
  if (sort_tip.value == "时间降序") {
    sort_tip.value = "时间升序";
  } else {
    sort_tip.value = "时间降序";
  }
  event_activities.reverse();
}

// 事件脉络
const event_activities = reactive([]);
const event_total_num = ref(0);
const update_time = ref("");
// 格式化时间
function formatteTime1(time){
  let timestamp = new Date(time);
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
  return formattedTimestamp
}
function formatteTime2(time){
  let timestamp = new Date(time);
  let formattedTimestamp =
    timestamp.getFullYear() +
    "年" +
    (timestamp.getMonth() + 1) +
    "月" +
    timestamp.getDate() +
    "日 " +
    timestamp.getHours() +
    ":" +
    (timestamp.getMinutes() < 10 ? "0" : "") +
    timestamp.getMinutes();
  return formattedTimestamp
}
function api_get_event_msg() {
  API({
    url: "/database/api_get_timeline",
    method: "get",
    params: {
      title: store.state.title,
    },
  }).then((res) => {
    event_total_num.value = res.data.length;
    update_time.value = formatteTime2(res.data[0][2])
    res.data.forEach((element) => {
      let obj = {
        content: element[1],
        timestamp: formatteTime1(element[2]),
        type: "primary",
        hollow: true,
      };
      event_activities.push(obj);
    });
  });
}
onMounted(() => {
  api_get_event_msg();
});
</script>

<style scoped>
.main {
  width: 60%;
  margin: 0 auto;
  padding: 20px;
}
.head-title {
  font-size: 16px;
  margin: 10px 0 20px 0;
  color: rgba(255, 255, 255, 0.9);
}
.sort-button {
  cursor: pointer;
  color: #409eff;
  transition: all 0.2s;
  display: flex;
  align-items: center;
}
.sort-button:hover {
  color: #66b1ff;
}
.wrap-event-activities {
  margin-top: 40px;
  width: 100%;
  align-self: baseline;
}
.wrap-event-activities p {
  color: #fff;
}
</style>