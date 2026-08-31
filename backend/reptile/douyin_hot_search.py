# 获取抖音热搜榜前50
from reptile.common.tophub import fetch_tophub_board


def douyin_hot_search(limit=50):
    """抖音热榜。抖音官方接口需要 a_bogus 签名，这里走 tophub 的聚合页。"""
    board = fetch_tophub_board("https://tophub.today/n/K7GdaMgdQy", "douyin", limit)
    for item in board:
        if not item["url"]:
            item["url"] = "https://www.douyin.com/search/" + item["title"]
    return board


if __name__ == '__main__':
    for item in douyin_hot_search(10):
        print(item)
