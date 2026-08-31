# 获取微博热搜榜前50
import json

from reptile.common.requests_get import requests_get


def weibo_hot_search():
    url = "https://weibo.com/ajax/side/hotSearch"
    content = requests_get(url)
    data = json.loads(content)["data"]["realtime"]
    hot_list = []
    for index, d in enumerate(data):
        # 去除广告数据
        if 'ad_type' in d.keys():
            continue
        obj = {
            "title": d["note"],
            "rank": d["rank"]+1,
            "hot_value": str(d["num"]//10000) + "万",
            "url": "https://s.weibo.com/weibo?q="+d["note"],
        }
        hot_list.append(obj)
    hot_list = str(hot_list).replace("'", '"')
    return hot_list


if __name__ == '__main__':
    print(weibo_hot_search())
