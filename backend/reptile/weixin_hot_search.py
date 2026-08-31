# 获取微信热文榜前50
from lxml import etree
from reptile.common.requests_get import requests_get


# 获取微信热文榜单
def weixin_hot_search(limit=50):
    if limit <= 0:
        limit = 1
    elif limit > 50:
        limit = 50
    url = "https://tophub.today/n/WnBe01o371"
    content = requests_get(url)
    tree = etree.HTML(content)
    hot_list_title = tree.xpath("//td[@class='al']//a/text()")[:limit]
    hot_list_value = tree.xpath("//td/text()")[1::2][:limit]
    hot_list_url = tree.xpath("//td[@class='al']//a/@href")[:limit]
    hot_list = [{
        "title": a.replace(' ', ''),
        "rank": i+1,
        "hot_value": b.replace(' ', '').split(',')[1].split('在看')[0],
        "url": "https://tophub.today" + c.replace(' ', '')}
        for i, (a, b, c) in enumerate(zip(hot_list_title, hot_list_value,hot_list_url))]
    hot_list = str(hot_list).replace("'", '"')
    return hot_list


if __name__ == '__main__':
    # 热榜标题 热度值 热搜链接
    hot_list = weixin_hot_search(50)
    print(hot_list)

