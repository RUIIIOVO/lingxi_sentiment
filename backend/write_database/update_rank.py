# linux中无法读取上一级目录时在import前添加
import sys
import os

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

import pymysql

from db_config import db
from reptile.baidu_hot_search import baidu_hot_search
from reptile.bili_hot_search import bili_hot_search
from reptile.common.http_client import AuthRequired, FetchError
from reptile.douyin_hot_search import douyin_hot_search
from reptile.toutiao_hot_search import toutiao_hot_search
from reptile.weibo_hot_search import weibo_hot_search
from reptile.weixin_hot_search import weixin_hot_search
from reptile.zhihu_hot_search import zhihu_hot_search

# 表名前缀 -> 抓取函数
FETCHERS = {
    "weibo": weibo_hot_search,
    "baidu": baidu_hot_search,
    "toutiao": toutiao_hot_search,
    "douyin": douyin_hot_search,
    "zhihu": zhihu_hot_search,
    "weixin": weixin_hot_search,
    "bili": bili_hot_search,
}

# 实际写库的平台。bili 没有对应的数据表，只在单独调用时用
ENABLED = ["weibo", "baidu", "toutiao", "douyin", "zhihu", "weixin"]


def fetch_all(platforms=None):
    """先把所有榜单抓完再入库。

    单个平台失败不影响其他平台：知乎缺 Cookie、某站改版都只跳过它自己。
    """
    results = {}
    for name in platforms or ENABLED:
        try:
            rows = FETCHERS[name]()
        except AuthRequired as exc:
            print(f"[{name}] 跳过，需要有效 Cookie：{exc}")
            continue
        except (FetchError, KeyError, ValueError, IndexError) as exc:
            print(f"[{name}] 抓取失败：{type(exc).__name__}: {exc}")
            continue
        if not rows:
            print(f"[{name}] 返回空榜单，跳过")
            continue
        results[name] = rows
        print(f"[{name}] 抓到 {len(rows)} 条")
    return results


# 存入数据库主体函数
def update_rank():
    # 先抓取，全部拿到手再动数据库。抓取失败时不清空原有数据
    boards = fetch_all()
    if not boards:
        print("所有平台都没抓到数据，本次不更新数据库")
        return

    connect = pymysql.connect(
        host=db["host"],
        port=db["port"],  # 端口号
        user=db["user"],  # 数据库用户
        password=db["password"],  # 数据库密码
        database=db["database"]  # 要连接的数据库名称
    )
    cursor = connect.cursor()
    try:
        for name, rows in boards.items():
            table = f"{name}_hot_search_rank"
            cursor.execute(f"delete from {table}")
            sql_insert = f"insert into {table}(title, `rank`, hot_value, url) values(%s,%s,%s,%s)"
            cursor.executemany(sql_insert, [
                (d["title"], d["rank"], d["hot_value"], d["url"]) for d in rows
            ])
            connect.commit()
            print(f"[{name}] 写入 {len(rows)} 条")
    except Exception as e:
        connect.rollback()
        print("存入数据库出错:", str(e))
    finally:
        cursor.close()  # 关闭游标
        connect.close()  # 关闭数据库连接


if __name__ == '__main__':
    # 只跑抓取、不写库：python write_database/update_rank.py --dry-run
    if "--dry-run" in sys.argv:
        for name, rows in fetch_all().items():
            print(f"\n===== {name} =====")
            for item in rows[:5]:
                print("  ", item)
    else:
        update_rank()
