<!-- 详情 -->
<template>
  <el-page-header @back="goBack" title="返回" style="font-size: 20px">
    <template #content>
      <span class="head-title">{{ event_title }}</span>
    </template>
  </el-page-header>
  <!-- <el-tabs
    v-model="activeName"
    type="card"
    class="wrap-tabs"
  >
    <el-tab-pane label="事件概况" name="first"><DetailSituation /></el-tab-pane>
    <el-tab-pane label="事件脉络" name="second"><DetailVein /></el-tab-pane>
    <el-tab-pane label="人群画像" name="third"><DetailPeople /></el-tab-pane>
  </el-tabs> -->
  <t-tabs :default-value="1" class="wrap-tabs" :lazy="true">
    <t-tab-panel :value="1" label="事件概况" style="height:calc(100% - 50px)">
      <el-scrollbar max-height="100%">
        <DetailSituation />
      </el-scrollbar>
    </t-tab-panel>
    <t-tab-panel :value="2" label="事件脉络" v-if="VeinFlag" style="height:calc(100% - 50px)">
      <el-scrollbar max-height="100%">
        <DetailVein />
      </el-scrollbar>
    </t-tab-panel>
    <t-tab-panel :value="3" label="人群画像" style="height:calc(100% - 50px)">
      <el-scrollbar max-height="100%">
        <DetailPeople />
      </el-scrollbar>
    </t-tab-panel>
  </t-tabs>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import DetailSituation from "./Detail/DetailSituation.vue";
import DetailVein from "./Detail/DetailVein.vue";
import DetailPeople from "./Detail/DetailPeople.vue";
// 返回上一页
const router = useRouter();
const goBack = () => {
  router.push({ path: "/AppDatabase" });
};
import { useStore } from "vuex";
const store = useStore();
var event_title = ref(store.state.title);

var VeinFlag = ref(false);
import API from "@/plugins/axiosInstance";
function api_get_event_msg() {
  API({
    url: "/database/api_get_timeline",
    method: "get",
    params: {
      title: store.state.title,
    },
  }).then((res) => {
    console.log(res.data);
    if (res.data.length == 0) {
      VeinFlag.value = false;
      console.log(VeinFlag.value);
    } else {
      VeinFlag.value = true;
      console.log(VeinFlag.value);
    }
  });
}

onMounted(() => {
  api_get_event_msg();
});

// 详情
// const activeName = ref("first");
</script>

<style scoped>
.head-title {
  font-size: 18px;
}
.wrap-tabs {
  margin: 26px 80px 20px 80px;
  height: calc(100% - 60px);
  border-radius: 10px;
  /* background-color: #171717;  */
  /* border: 1px solid #2d2e2f; */
}
:deep(.t-tabs__content,.t-tab-panel) {
  width: 100%;
  height: 100%;
}
</style>