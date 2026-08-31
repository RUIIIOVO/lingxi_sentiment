//axiosInstance.js
//导入axios
import axios from 'axios'

//使用axios下面的create([config])方法创建axios实例，其中config参数为axios最基本的配置信息。
const API = axios.create({
	// 后端地址，改 .env 里的 VUE_APP_API_BASE_URL，不要写死在代码里
	baseURL: process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000/',
	timeout: 10000,                   //请求超时设置，单位ms
	// 原生的django对于content-type为application/x-www-form-urlencoded
	// axios默认content-type为 application/json
	headers: {
		'Content-Type': 'application/x-www-form-urlencoded'
	},
})

//导出我们建立的axios实例模块，ES6 export用法
export default API
