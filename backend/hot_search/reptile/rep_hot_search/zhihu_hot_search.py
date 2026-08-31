# 获取知乎热搜榜前50
import os
from lxml import etree
from hot_search.reptile.common.requests_get import requests_get


# 获取知乎热搜榜单
def zhihu_hot_search(limit=50):
    if limit <= 0:
        limit = 1
    elif limit > 50:
        limit = 50
    url = "https://www.zhihu.com/hot"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'cookie': os.getenv("ZHIHU_COOKIE", ""),
    }
    content = requests_get(url,  headers=headers)
    tree = etree.HTML(content)  # 构造一个XPath解析对象并对HTML文本进行自动修正。
    hot_list_title = tree.xpath("//h2[@class='HotItem-title']/text()")[:limit]
    hot_list_value = tree.xpath("//div[@class='HotItem-metrics']/text()")[:limit]
    hot_list_link = tree.xpath("//div[@class='HotItem-content']/a/@href")[:limit]
    hot_list = [{
        "title": a.replace(' ', ''),
        "hot_value": b.replace(' ', '')[:-2],
        "url": c.replace(' ', '')}
        for a, b, c in zip(hot_list_title, hot_list_value, hot_list_link)]
    hot_list = str(hot_list).replace("'", '"')
    # with open('../reptile_static/zhihu_hot_search.json', 'w', encoding='utf-8') as fs:
    #     fs.write(hot_list)
    return hot_list


# if __name__ == '__main__':
#     # 热榜标题 热度值 热搜链接
#     hot_list = zhihu_hot_search(50)
#     print(hot_list)

