# 获取微博热搜榜前50
from reptile.common.cookie_manager import get_cookie
from reptile.common.http_client import fetch_json


def weibo_hot_search(limit=50):
    """微博热搜榜。

    该接口只校验 Referer，不带 Referer 直接 403，带了就能拿到完整 50 条，
    有没有 Cookie 不影响结果。环境变量里配了就带上，没配也能跑。
    """
    limit = max(1, min(limit, 50))
    url = "https://weibo.com/ajax/side/hotSearch"

    data = fetch_json(
        url, platform="weibo",
        headers={
            "Referer": "https://weibo.com/",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/plain, */*",
            "Cookie": get_cookie("weibo"),
        },
    )["data"]["realtime"]
    hot_list = []
    for d in data:
        # 去除广告数据
        if "ad_type" in d:
            continue
        hot_list.append({
            "title": d["note"],
            "rank": len(hot_list) + 1,
            "hot_value": str(d["num"] // 10000) + "万",
            "url": "https://s.weibo.com/weibo?q=" + d["note"],
        })
        if len(hot_list) >= limit:
            break
    return hot_list


if __name__ == '__main__':
    for item in weibo_hot_search(10):
        print(item)
