# -*- coding: utf-8 -*-
"""tophub.today 榜单页的共用解析。

抖音榜和微信榜都托管在这里，页面结构一致：
每行 4 个 td —— 序号、标题（带外链）、热度、图标。
原来的选择器写的是 td[@class='al']，该 class 站点已经改掉，现按列位置取。
"""
from lxml import etree

from reptile.common.http_client import fetch_text


def fetch_tophub_board(url, platform, limit=50):
    """返回 [{title, rank, hot_value, url}]，hot_value 保留站点原始写法。"""
    limit = max(1, min(limit, 50))
    tree = etree.HTML(fetch_text(url, platform=platform, headers={"Referer": "https://tophub.today/"}))

    rows = []
    for tr in tree.xpath("//table//tr"):
        cells = tr.xpath("./td")
        if len(cells) < 3:
            continue
        title = "".join(cells[1].itertext()).strip()
        if not title:
            continue
        links = cells[1].xpath(".//a/@href")
        rows.append({
            "title": title,
            "rank": len(rows) + 1,
            "hot_value": "".join(cells[2].itertext()).strip(),
            "url": links[0] if links else "",
        })
        if len(rows) >= limit:
            break
    return rows
