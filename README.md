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
  hot_search/     热搜聚合接口（emotion 为未启用的实验模块）
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
| `WEIBO_COOKIE` / `BAIDU_COOKIE` / `SINA_COOKIE` | 可选。留空时自动申请游客身份 |
| `ZHIHU_COOKIE` | 知乎必填。该站不接受游客身份，留空则跳过知乎榜单 |
| `LINGXI_HTTP_PROXY` | 可选代理，如 `http://127.0.0.1:7890`。留空直连 |
| `VUE_APP_API_BASE_URL` | 前端请求的后端地址 |

## 爬虫

各平台榜单抓取位于 `backend/reptile/`，每个文件都能单独运行来验证：

```bash
cd backend
PYTHONPATH=. python reptile/weibo_hot_search.py     # 单个平台
PYTHONPATH=. python write_database/update_rank.py --dry-run   # 全部平台，只抓不写库
```

Cookie 由 `reptile/common/cookie_manager.py` 统一从环境变量读取。必需的 Cookie 缺失时
会抛 `AuthRequired`，调度层跳过该平台并打日志，不会拿空数据当成功。

各平台当前的可抓取范围（实测）：

| 平台 | 榜单 | 正文与评论 |
| --- | --- | --- |
| 微博 | 免登录（只校验 Referer） | 需要登录 Cookie |
| 百度 | 免登录 | 搜索页一律跳验证码 |
| 今日头条 | 免登录 | 正文由 JS 渲染，需无头浏览器 |
| 抖音 / 微信 | 经 tophub 聚合 | 无公开接口 |
| 知乎 | 需要登录 Cookie | 接口需 `x-zse-96` 签名 |
| 哔哩哔哩 | 免登录 | 免登录（搜索、评论、用户信息均可取） |

官方游客身份（微博 passport 的 genvisitor、百度的 BAIDUID）实测对以上接口都不起作用，
因此未引入自动申请机制。

各平台 Cookie 有效期短。抓取失败先看日志里有没有 `AuthRequired`：有就是 Cookie 过期或缺失，
重新抓一份填回 `.env` 即可；报 `FetchError` 则是网络或站点改版。

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

## 许可证

[Apache-2.0](LICENSE)
