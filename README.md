# 灵犀舆情

#### 介绍
灵犀舆情是一款面向舆情领域的智能化舆情分析预警可视化平台，平台集舆情数据可视化分析、舆情事件实时检索和浏览、舆情热度及情感趋势分析、热点话题实时监测、预警和追踪等功能于一体，帮助政府和企事业单位及时感知网络动向，快速应对重大舆情。灵犀舆情集舆情分析和舆情预警一体化，旨在为用户提供全方位的舆情管理数据可视化平台。
本项目仅供学习参考，未经授权严禁商用。

## 目录结构

```
backend/    Django 后端：接口、爬虫、词云、入库任务
  control/        项目配置与路由
  home/           首页数据接口
  database/       舆情数据检索接口
  monitor/        实时监测与预警接口
  hot_search/     热搜聚合（含 reptile 爬虫与 emotion 情感模块）
  user/           登录注册
  word_cloud/     词云生成
  reptile/        各平台热搜爬虫（微博、知乎、百度、B站、抖音、头条、微信）
  write_database/ 定时抓取与写库脚本
  db_config/      数据库连接配置（读环境变量）
frontend/   Vue 3 前端：数据大屏与管理页
model/      情感分类模型
  model.py        训练脚本（PaddleNLP）
  deploy.py       Flask 推理服务，默认 0.0.0.0:8080
```

## 技术栈

| 层 | 技术 |
| --- | --- |
| 后端 | Django 3.2 + PyMySQL + APScheduler |
| 前端 | Vue 3 + Element Plus + ECharts + AntV G2 + 百度地图 |
| 模型 | PaddlePaddle + PaddleNLP（Jieba 分词 + 文本分类） |
| 存储 | MySQL 8 |

## 环境变量

所有口令与 Cookie 都从环境变量读取，仓库里不存任何真实凭据。
复制 `backend/.env.example`、`frontend/.env.example` 后填写。

| 变量 | 用途 |
| --- | --- |
| `LINGXI_DB_HOST` / `_PORT` / `_USER` / `_PASSWORD` / `_NAME` | MySQL 连接 |
| `DJANGO_SECRET_KEY` | Django 签名密钥 |
| `WEIBO_COOKIE` / `BAIDU_COOKIE` / `ZHIHU_COOKIE` / `SINA_COOKIE` | 各平台抓取所需的登录 Cookie，留空则对应平台抓不到数据 |
| `VUE_APP_API_BASE_URL` | 前端请求的后端地址 |

## 本地启动

```bash
# 后端
cd backend
pip install -r requirements.txt
cp .env.example .env && vim .env      # 填数据库与 Cookie
set -a && source .env && set +a
python manage.py runserver 0.0.0.0:8000

# 前端
cd frontend
npm install
cp .env.example .env.local
npm run serve                          # 构建产物用 npm run build
```

## 模型

训练数据集未随仓库分发，来自 AI Studio 公开数据集 `data283895`，
下载后按 `model/data/data283895/{train,dev,test}.tsv` 放置，再运行：

```bash
cd model
python model.py      # 训练
python deploy.py     # 起 Flask 推理服务（0.0.0.0:8080）
```

## 已知问题

- `backend/reptile/` 与 `backend/hot_search/reptile/` 是两份重复的爬虫代码，尚未合并。
- `backend/user/views.py` 用字符串拼接 SQL，且用户密码明文存库，勿直接用于生产。
- 各平台 Cookie 有效期短，抓取失败时先检查 Cookie 是否过期。

## 许可证

[Apache-2.0](LICENSE)
