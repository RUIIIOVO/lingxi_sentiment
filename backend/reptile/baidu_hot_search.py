# coding=gb2312
# 获取百度热搜榜前50
from lxml import etree
from reptile.common.requests_get import requests_get


# 获取百度热搜榜单
def baidu_hot_search(limit=30):
    if limit <= 0:
        limit = 1
    elif limit > 30:
        limit = 30
    url = "https://top.baidu.com/board?tab=realtime"
    content = requests_get(url)
    tree = etree.HTML(content)
    hot_list_title = tree.xpath("//div[@class='c-single-text-ellipsis']/text()")[:limit]
    hot_list_value = tree.xpath("//div[@class='hot-index_1Bl1a']/text()")[:limit]
    hot_list = [{
        "title": a.replace(' ', ''),
        "rank": i + 1,
        "hot_value": str(int(b.replace(' ', '')) // 10000) + "万",
        "url": f"https://www.baidu.com/s?wd={a.replace(' ', '')}&sa=fyb_news&rsv_dl=fyb_news"}
        for i, (a, b) in enumerate(zip(hot_list_title, hot_list_value))]
    hot_list = str(hot_list).replace("'", '"')
    return hot_list


if __name__ == '__main__':
    # 热榜标题 热度值 热搜链接
    hot_list = baidu_hot_search()
    print(hot_list)
