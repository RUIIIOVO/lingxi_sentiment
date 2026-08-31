# linux中无法读取上一级目录时在import前添加
import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

import json
import pymysql

from reptile import *

from reptile.weibo_hot_search import weibo_hot_search
from reptile.baidu_hot_search import baidu_hot_search
from reptile.toutiao_hot_search import toutiao_hot_search
from reptile.douyin_hot_search import douyin_hot_search
from reptile.zhihu_hot_search import zhihu_hot_search
from reptile.weixin_hot_search import weixin_hot_search
from reptile.bili_hot_search import bili_hot_search

hot_search_list = ["weibo", "baidu", "toutiao", "douyin", "zhihu", "weixin"]
functions = {
    "weibo_hot_search": weibo_hot_search,
    "baidu_hot_search": baidu_hot_search,
    "toutiao_hot_search": toutiao_hot_search,
    "douyin_hot_search": douyin_hot_search,
    "zhihu_hot_search": zhihu_hot_search,
    "weixin_hot_search": weixin_hot_search,
}
from db_config import db

# 存入数据库主体函数
def update_rank():
    # 连接数据库
    connect = pymysql.connect(
        host=db["host"],
        port=db["port"],  # 端口号
        user=db["user"],  # 数据库用户
        password=db["password"],  # 数据库密码
        database=db["database"]  # 要连接的数据库名称
    )
    cursor = connect.cursor()
    try:
        for item in hot_search_list:
            print(item)
            sql_del = f"delete from {item}_hot_search_rank"
            cursor.execute(sql_del)
            function_name = item+'_hot_search'
            if function_name in functions:
                data = json.loads(functions[function_name]())
            sql_insert = f"insert into {item}_hot_search_rank(title, `rank` ,hot_value,url)values(%s,%s,%s,%s)"
            for d in data:
                title = d["title"]
                rank = d["rank"]
                hot_value = d["hot_value"]
                url = d["url"]
                values = [(title, rank, hot_value, url)]
                # print(values)
                cursor.executemany(sql_insert, values)
                connect.commit()
    except Exception as e:
        print("存入数据库出错:", str(e))
    finally:
        cursor.close()  # 关闭游标
        connect.close()  # 关闭数据库连接


if __name__ == '__main__':
    update_rank()

