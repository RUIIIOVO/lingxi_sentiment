# 获取今日头条热搜榜前50
import json
from hot_search.reptile.common.requests_get import requests_get


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
    for obj in data:
        hot_obj = {
            "title": obj["Title"].replace(' ', ''),
            "hot_value": obj["HotValue"].replace(' ', ''),
            "url": obj["Url"].split('?')[0].replace(' ', ''),
            "img": obj["Image"]["url"].replace(' ', ''),
        }
        hot_list.append(hot_obj)
    # hot_list = hot_list[:output_num]
    hot_list = str(hot_list[:limit]).replace("'", '"')
    # with open('../reptile_static/toutiao_hot_search.json', 'w', encoding='utf-8') as fs:
    #     fs.write(str(hot_list))
    return hot_list


# if __name__ == '__main__':
#     # 热榜标题 热度值 热搜链接
#     hot_list = toutiao_hot_search(50)
#     print(hot_list)

