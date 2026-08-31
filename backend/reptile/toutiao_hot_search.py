# 获取今日头条热搜榜前50
import json
from reptile.common.requests_get import requests_get


# 获取今日头条热搜榜单
def toutiao_hot_search(limit=50):
    if limit <= 0:
        limit = 1
    elif limit > 50:
        limit = 50
    url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
    content = requests_get(url)
    data = json.loads(content)["data"]
    hot_list = []
    for i, obj in enumerate(data):
        hot_obj = {
            "title": obj["Title"].replace(' ', ''),
            "rank": i + 1,
            "hot_value": str(int(obj["HotValue"].replace(' ', ''))//10000) + "万",
            "url": obj["Url"].split('?')[0].replace(' ', ''),
            # "img": obj["Image"]["url"].replace(' ', ''),
        }
        hot_list.append(hot_obj)
    hot_list = str(hot_list[:limit]).replace("'", '"')
    return hot_list


# if __name__ == '__main__':
#     # 热榜标题 热度值 热搜链接
#     hot_list = toutiao_hot_search(50)
#     print(hot_list)

