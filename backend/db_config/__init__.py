# 数据库连接配置信息，从环境变量读取，见根目录 .env.example
import os

db = {
    "host": os.getenv("LINGXI_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("LINGXI_DB_PORT", "3306")),
    "user": os.getenv("LINGXI_DB_USER", "root"),
    "password": os.getenv("LINGXI_DB_PASSWORD", ""),
    "database": os.getenv("LINGXI_DB_NAME", "lingxi"),
}
