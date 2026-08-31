# -*- coding: utf-8 -*-
"""历史遗留的抓取入口，转调 reptile.common.http_client。

这个目录是 reptile/ 的一份旧副本，仍被 update_weibo.py 和 hot_search/views.py 引用。
新代码请写在 reptile/ 下，不要再往这里加东西。
"""
from reptile.common.http_client import default_headers, fetch_text

headers_obj = default_headers()


def requests_get(url, headers=None):
    return fetch_text(url, headers=headers)
