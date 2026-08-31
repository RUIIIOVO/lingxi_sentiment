<!-- 侧边导航栏 -->
<template>
  <div class="wrap-nav">
    <div class="logo">
      <img src="@/assets/img/logo.png" alt="" />
    </div>
    <ul>
      <li
        v-for="(item, index) in navList"
        :key="index"
        class="nav-item"
        :class="nowPath === item.url ? 'nav-item-focus' : ''"
        @click="changeNav(item.url)"
      >
        <div class="wrap-nav-icon">
          <el-icon class="nav-icon">
            <component :is="item.icon"></component>
          </el-icon>
        </div>
      </li>
    </ul>
    <!-- 登录/注册入口按钮及默认头像 -->
    <t-dropdown
      :min-column-width="60"
      trigger="click"
      @click="clickHandler"
      v-if="!userVisible"
      placement="right"
    >
      <el-avatar variant="text" :icon="UserFilled" class="avatar" />
      <t-dropdown-menu>
        <t-dropdown-item :value="1" @click="loginVisible = true">
          <p class="user-tips">登录/注册</p>
        </t-dropdown-item>
      </t-dropdown-menu>
    </t-dropdown>
    <!-- 登录后头像 -->
    <t-dropdown
      :min-column-width="60"
      trigger="click"
      @click="clickHandler"
      v-if="userVisible"
      placement="right"
    >
      <el-avatar variant="text" class="avatar user-avatar">{{
        username.slice(0, 1)
      }}</el-avatar>
      <t-dropdown-menu>
        <t-dropdown-item :value="1">
          <p>账户：{{ username }}</p>
        </t-dropdown-item>
        <t-dropdown-item :value="2" @click="logoutVisible = true">
          <p class="user-tips">退出登录</p>
        </t-dropdown-item>
      </t-dropdown-menu>
    </t-dropdown>
  </div>
  <!-- 登录注册弹窗 -->
  <el-dialog
    v-model="loginVisible"
    :title="registerVisible ? '注册新账号' : '登录'"
    width="450"
    align-center
    center
  >
    <div class="login-content" v-if="!registerVisible">
      <t-form
        ref="loginForm"
        :rules="rules"
        :data="loginFormData"
        :colon="true"
        :label-width="0"
        @submit="loginOnSubmit"
        @reset="onReset"
        id="loginForm"
      >
        <t-form-item name="username">
          <t-input
            v-model="loginFormData.username"
            clearable
            placeholder="请输入账户名"
          >
            <template #prefix-icon>
              <User1Icon />
            </template>
          </t-input>
        </t-form-item>

        <t-form-item name="password">
          <t-input
            v-model="loginFormData.password"
            type="password"
            clearable
            placeholder="请输入密码"
          >
            <template #prefix-icon>
              <lock-on-icon />
            </template>
          </t-input>
        </t-form-item>

        <t-form-item style="margin-bottom: 14px">
          <t-button theme="primary" type="submit" block>登录</t-button>
        </t-form-item>
        <t-form-item>
          <t-button
            class="login-btn"
            variant="text"
            theme="default"
            @click="registerVisible = true"
            >注册账号</t-button
          >
        </t-form-item>
      </t-form>
    </div>
    <div class="login-content" v-if="registerVisible">
      <t-form
        ref="registerForm"
        :rules="rules"
        :data="registerFormData"
        :colon="true"
        :label-width="0"
        @submit="registerOnSubmit"
        id="registerForm"
      >
        <t-form-item name="username">
          <t-input
            v-model="registerFormData.username"
            clearable
            placeholder="请输入账户名"
          >
            <template #prefix-icon>
              <User1Icon />
            </template>
          </t-input>
        </t-form-item>

        <t-form-item name="password">
          <t-input
            v-model="registerFormData.password"
            type="password"
            clearable
            placeholder="请输入密码"
          >
            <template #prefix-icon>
              <lock-on-icon />
            </template>
          </t-input>
        </t-form-item>

        <t-form-item style="margin-bottom: 14px">
          <t-button theme="primary" type="submit" block>注册</t-button>
        </t-form-item>
        <t-form-item>
          <t-button
            class="login-btn"
            variant="text"
            theme="default"
            @click="registerVisible = false"
            >登录账号</t-button
          >
        </t-form-item>
      </t-form>
    </div>
  </el-dialog>
  <!-- 退出登录确认弹窗 -->
  <el-dialog
    v-model="logoutVisible"
    title="退出登录"
    width="300"
    align-center
    center
  >
    <p style="text-align: center">是否确认退出登录</p>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="logoutVisible = false">取消</el-button>
        <el-button type="primary" @click="logout"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
let navList = reactive([
  {
    name: "首页",
    icon: "House",
    url: "AppHome",
  },
  {
    name: "事件库",
    icon: "Files",
    url: "AppDatabase",
  },
  {
    name: "热搜监测",
    icon: "Odometer",
    url: "AppMonitor",
  },
]);
function changeNav(url) {
  router.push({ path: "/" + url });
}
// 动态监测路径
let nowPath = ref(router.currentRoute.fullPath);
watch(
  router.currentRoute,
  (newValue) => {
    nowPath.value = newValue.fullPath.slice(1);
    if (newValue.fullPath.slice(1) == "") {
      nowPath.value = "AppHome";
    }
  },
  { immediate: true }
);

// 用户头像
import { UserFilled } from "@element-plus/icons-vue";
import { useStore } from "vuex";
const store = useStore();
var user_id = ref(store.state.user_id);
var username = ref(store.state.username);
const userVisible = ref(false);

onMounted(()=>{
  if (username.value != undefined && username.value != "0") {
      userVisible.value = true;
    } else {
      userVisible.value = false;
    }
})

const logoutVisible = ref(false);
import Cookies from "js-cookie";
// 登出
function logout() {
  logoutVisible.value = false;
  userVisible.value = false;
  store.commit("updateUserName", "0");
  store.commit("updateUserId", "0");
  Cookies.remove("user_id");
  Cookies.remove("username");
  MessagePlugin.success("退出登录成功");
}

// 登录
const loginVisible = ref(false);
const registerVisible = ref(false);
import { MessagePlugin } from "tdesign-vue-next";
import { LockOnIcon, User1Icon } from "tdesign-icons-vue-next";
const rules = {
  username: [
    { required: true, message: "姓名必填", type: "error", trigger: "blur" },
    { required: true, message: "姓名必填", type: "error", trigger: "change" },
    { whitespace: true, message: "姓名不能为空" },
  ],
  password: [{ required: true, message: "密码必填", type: "error" }],
};
import API from "@/plugins/axiosInstance";

const loginFormData = ref({
  username: "",
  password: "",
});

// 用于清除校验，loginForm.value.clearValidate();不生效，待解决
// const loginForm = ref(null);
// const registerForm = ref(null);

const loginOnSubmit = ({ validateResult }) => {
  if (validateResult === true) {
    API({
      url: "/user/api_login/",
      method: "post",
      data: loginFormData.value,
    }).then((res) => {
      if (res.data.code == 200) {
        MessagePlugin.success("登录成功");

        // 存入vuex
        username.value = res.data.data.username;
        store.commit("updateUserName", username.value);
        user_id.value = res.data.data.user_id;
        store.commit("updateUserId", user_id.value);

        userVisible.value = true;
        loginVisible.value = false;
        setTimeout(() => {
          loginFormData.value = {
            username: "",
            password: "",
          };
          // loginForm.value.clearValidate();
        }, 1000);
      } else {
        MessagePlugin.error("用户名或密码错误");
      }
    });
  }
};

// 注册
const registerFormData = ref({
  username: "",
  password: "",
});
const registerOnSubmit = ({ validateResult }) => {
  if (validateResult === true) {
    API({
      url: "/user/api_register/",
      method: "post",
      data: registerFormData.value,
    }).then((res) => {
      console.log(res.data.code);
      if (res.data.code == 200) {
        MessagePlugin.success("注册成功");
        registerVisible.value = false;
        loginFormData.value = registerFormData.value;
        setTimeout(() => {
          registerFormData.value = {
            username: "",
            password: "",
          };
          // registerForm.value.clearValidate();
        }, 1000);
      } else {
        MessagePlugin.warning("该用户名已占用");
      }
    });
  }
};
</script>

<style scoped>
.wrap-nav {
  width: 70px;
  height: 100%;
  /* background-color: rgba(35, 35, 35, 0.8); */
  background-color: #1b1b1b;
  border-right: 1px solid #2d2e2f;
  backdrop-filter: 20px;
  position: fixed;
  top: 0px;
  z-index: 4;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: column;
}
.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 70px;
  /* position: absolute;
  top: 10px; */
}
.logo img {
  width: 35px;
  height: 35px;
}
ul {
  margin-bottom: 40px;
}
.nav-item {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  height: 50px;
  margin-bottom: 10px;
  font-size: 14px;
  color: rgb(82, 82, 82);
  transition: all 0.2s;
  cursor: pointer;
  border-radius: 10px;
}
.nav-item:hover {
  /* background-color: rgba(112, 112, 112, 0.3); */
  background-color: #424446;
  color: rgb(172, 172, 172);
}
.wrap-nav-icon {
  display: flex;
  align-items: center;
}
.nav-icon {
  font-size: 20px;
}
.nav-item-focus {
  color: rgba(255, 255, 255, 0.8) !important;
}
.avatar {
  margin-bottom: 20px;
  cursor: pointer;
  background-color: #3393f5;
}
.user-avatar {
  font-size: 16px;
}
.user-tips {
  text-align: center;
  font-size: 12px;
  /* width: 70px; */
}
.login-content {
  width: 70%;
  margin: 0 auto;
}
.login-input {
  margin: 0px auto 20px auto;
}
.login-btn {
  width: 100%;
}
:deep(.t-form__item) {
  margin-bottom: 20px;
}
</style>