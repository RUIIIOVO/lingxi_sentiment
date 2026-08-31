# 获取微信热文榜前50
from reptile.common.tophub import fetch_tophub_board


def weixin_hot_search(limit=50):
    """微信热文榜。微信公众号没有公开搜索接口，走 tophub 的聚合页。"""
    board = fetch_tophub_board("https://tophub.today/n/WnBe01o371", "weixin", limit)
    for item in board:
        # 站点把热度写成 "12,345 在看"，取数字部分
        item["hot_value"] = item["hot_value"].split("在看")[0].strip()
        if item["url"].startswith("/"):
            item["url"] = "https://tophub.today" + item["url"]
    return board


if __name__ == '__main__':
    for item in weixin_hot_search(10):
        print(item)
