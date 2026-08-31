# 获取知乎热搜榜前50
from reptile.common.cookie_manager import get_cookie
from reptile.common.http_client import AuthRequired, fetch_json


def zhihu_hot_search(limit=50):
    """知乎热榜。

    知乎不接受游客身份：网页版热榜返回 403，开放 API 返回 401，
    绕过需要逆向 x-zse-96 签名。所以这里只认 ZHIHU_COOKIE 里的登录态，
    没有就直接抛错，由调用方记录日志——不返回空列表冒充成功。
    """
    limit = max(1, min(limit, 50))
    cookie = get_cookie("zhihu")  # 缺失时抛 AuthRequired

    url = f"https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit={limit}"
    data = fetch_json(
        url, platform="zhihu",
        headers={
            "Referer": "https://www.zhihu.com/hot",
            "x-requested-with": "fetch",
            "Accept": "application/json",
            "Cookie": cookie,
        },
    ).get("data", [])

    hot_list = []
    for i, item in enumerate(data[:limit]):
        target = item.get("target", {})
        hot_list.append({
            "title": target.get("title", "").strip(),
            "rank": i + 1,
            "hot_value": (item.get("detail_text") or "").replace("万热度", "万").strip(),
            "url": target.get("url", "").replace("api.zhihu.com/questions", "www.zhihu.com/question"),
        })
    return hot_list


if __name__ == '__main__':
    try:
        for item in zhihu_hot_search(10):
            print(item)
    except AuthRequired as exc:
        print("跳过知乎：", exc)
