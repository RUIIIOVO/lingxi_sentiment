# -*- coding: utf-8 -*-
"""历史遗留的抓取入口，保留给尚未迁移的调用方。

原实现内置了 22 个免费代理 IP 且随机轮换，这些代理现已全部失效，
任何请求都会超时。现在改为转调 http_client，代理由环境变量 LINGXI_HTTP_PROXY 控制。

新代码请直接用 reptile.common.http_client 的 fetch_text / fetch_json，
它们会在 Cookie 失效时抛 AuthRequired，而不是让调用方拿到一个空串。
"""
from reptile.common.http_client import default_headers, fetch_text

headers_obj = default_headers()


def requests_get(url, headers=None):
    return fetch_text(url, headers=headers)
