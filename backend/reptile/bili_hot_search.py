# 获取哔哩哔哩热搜榜前50
from reptile.common.http_client import fetch_json


def bili_hot_search(limit=50):
    """B 站热搜榜。接口不需要登录态，也不返回热度值。"""
    limit = max(1, min(limit, 50))
    url = f"https://app.bilibili.com/x/v2/search/trending/ranking?limit={limit}"
    data = fetch_json(url, platform="bili", headers={"Referer": "https://www.bilibili.com/"})["data"]["list"]

    hot_list = []
    for i, obj in enumerate(data[:limit]):
        keyword = obj["show_name"].strip()
        hot_list.append({
            "title": keyword,
            "rank": i + 1,
            # 该接口没有热度字段，留空由上层决定怎么展示
            "hot_value": "",
            "url": "https://search.bilibili.com/all?keyword=" + keyword,
        })
    return hot_list


if __name__ == '__main__':
    for item in bili_hot_search(10):
        print(item)
