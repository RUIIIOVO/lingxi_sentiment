# -*- coding: utf-8 -*-
from reptile.common.http_client import default_headers, fetch_text

headers_obj = default_headers()


def requests_get(url, headers=None):
    return fetch_text(url, headers=headers)
