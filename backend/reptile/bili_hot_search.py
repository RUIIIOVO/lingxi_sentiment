# 获取哔哩哔哩热搜榜前30
import json
from reptile.common.requests_get import requests_get


# 获取哔哩哔哩热搜榜单
def bili_hot_search(limit=50):
    if limit <= 0:
        limit = 1
    elif limit > 50:
        limit = 50
    url = f"https://app.bilibili.com/x/v2/search/trending/ranking?csrf=772613c993686ee6df3651d12942adf2&limit={limit}"
    content = requests_get(url)
    data = json.loads(content)["data"]["list"]
    hot_list = []
    for i,obj in enumerate(data):
        hot_obj = {
            "title": obj["show_name"].replace(' ', ''),
            "rank": i+1,
            "url": "https://search.bilibili.com/all?keyword="+obj["show_name"].replace(' ', ''),
        }
        hot_list.append(hot_obj)
    hot_list = str(hot_list).replace("'", '"')
    return hot_list


if __name__ == '__main__':
    # 热榜标题 热度值 热搜链接
    hot_list = bili_hot_search(50)
    print(hot_list)

