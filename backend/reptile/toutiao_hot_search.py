# 获取今日头条热搜榜前50
from reptile.common.http_client import fetch_json


def toutiao_hot_search(limit=50):
    """今日头条热榜。该接口不需要登录态。"""
    limit = max(1, min(limit, 50))
    url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
    data = fetch_json(url, platform="toutiao", headers={"Referer": "https://www.toutiao.com/"})["data"]

    hot_list = []
    for i, obj in enumerate(data[:limit]):
        raw = str(obj.get("HotValue", "0")).strip()
        hot_value = str(int(raw) // 10000) + "万" if raw.isdigit() else raw
        hot_list.append({
            "title": obj["Title"].strip(),
            "rank": i + 1,
            "hot_value": hot_value,
            "url": obj["Url"].split("?")[0].strip(),
            # 话题聚合 id，抓正文时用得上
            "cluster_id": obj.get("ClusterIdStr", ""),
        })
    return hot_list


if __name__ == '__main__':
    for item in toutiao_hot_search(10):
        print(item)
