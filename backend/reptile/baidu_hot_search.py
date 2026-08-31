# 获取百度热搜榜前30
from lxml import etree

from reptile.common.cookie_manager import get_cookie
from reptile.common.http_client import fetch_text


def baidu_hot_search(limit=30):
    """百度实时热搜榜。榜单页面免登录，不需要 Cookie。"""
    limit = max(1, min(limit, 30))
    url = "https://top.baidu.com/board?tab=realtime"

    tree = etree.HTML(fetch_text(url, platform="baidu", headers={"Cookie": get_cookie("baidu")}))
    titles = tree.xpath("//div[@class='c-single-text-ellipsis']/text()")[:limit]
    values = tree.xpath("//div[contains(@class,'hot-index_')]/text()")[:limit]

    hot_list = []
    for i, title in enumerate(titles):
        title = title.strip()
        raw = values[i].strip() if i < len(values) else "0"
        hot_value = str(int(raw) // 10000) + "万" if raw.isdigit() else raw
        hot_list.append({
            "title": title,
            "rank": i + 1,
            "hot_value": hot_value,
            "url": f"https://www.baidu.com/s?wd={title}&sa=fyb_news&rsv_dl=fyb_news",
        })
    return hot_list


if __name__ == '__main__':
    for item in baidu_hot_search(10):
        print(item)
