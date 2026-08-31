# -*- coding: utf-8 -*-
"""统一的 HTTP 抓取客户端。

替代原来的 requests_get：原实现内置了 22 个免费代理 IP，现已全部失效，
每次请求随机挑一个必然超时。这里改为默认直连，代理通过环境变量可选开启。

失败时抛出明确的异常，而不是静默返回空串——上层要能区分"网络抖动"和"Cookie 过期"。
"""
import os
import random
import time

import requests
import urllib3

urllib3.disable_warnings()

# 请求超时（连接, 读取），单位秒
TIMEOUT = (5, 15)
# 失败重试次数
MAX_RETRY = 3

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
]

MOBILE_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)


class FetchError(Exception):
    """网络层失败：超时、连接错误、5xx、重试耗尽。"""


class AuthRequired(FetchError):
    """站点要求登录：401/403，或被重定向到登录页。上层应刷新 Cookie 后重试。"""

    def __init__(self, platform, detail=""):
        self.platform = platform
        super().__init__(f"[{platform}] 需要有效 Cookie：{detail}")


def _proxies():
    """代理可选。设了 LINGXI_HTTP_PROXY 才走代理，否则直连。"""
    proxy = os.getenv("LINGXI_HTTP_PROXY", "").strip()
    if not proxy:
        return None
    return {"http": proxy, "https": proxy}


def default_headers(mobile=False):
    return {
        "User-Agent": MOBILE_USER_AGENT if mobile else random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
    }


def _looks_like_login_page(response):
    """有些站点不返回 401/403，而是 302 到登录页或直接吐一个登录页面。"""
    if response.status_code in (301, 302, 303, 307, 308):
        location = response.headers.get("Location", "")
        return any(k in location for k in ("passport", "login", "signin", "wappass"))
    if "text/html" not in response.headers.get("Content-Type", ""):
        return False
    head = response.text[:2000]
    return any(k in head for k in ("请登录", "登录后查看", "passport.weibo.com", "安全验证"))


def fetch(url, headers=None, cookies=None, platform=None, mobile=False,
          allow_redirects=True, session=None):
    """发起 GET 请求并返回 requests.Response。

    platform 只用于异常信息，标明是哪个站点要 Cookie。
    """
    merged = default_headers(mobile=mobile)
    if headers:
        merged.update(headers)

    caller = session or requests
    last_error = None

    for attempt in range(1, MAX_RETRY + 1):
        try:
            response = caller.get(
                url, headers=merged, cookies=cookies, proxies=_proxies(),
                timeout=TIMEOUT, verify=False, allow_redirects=allow_redirects,
            )
        except requests.RequestException as exc:
            last_error = exc
            time.sleep(0.5 * attempt)
            continue

        if response.status_code in (401, 403):
            raise AuthRequired(platform or url, f"HTTP {response.status_code}")
        if _looks_like_login_page(response):
            raise AuthRequired(platform or url, f"被重定向到登录页 HTTP {response.status_code}")
        if response.status_code >= 500:
            last_error = FetchError(f"HTTP {response.status_code}")
            time.sleep(0.5 * attempt)
            continue
        if response.status_code != 200:
            raise FetchError(f"[{platform or url}] 意外状态码 HTTP {response.status_code}")

        response.encoding = response.apparent_encoding or "utf-8"
        return response

    raise FetchError(f"[{platform or url}] 重试 {MAX_RETRY} 次仍失败：{last_error}")


def fetch_text(url, **kwargs):
    return fetch(url, **kwargs).text


def fetch_json(url, **kwargs):
    response = fetch(url, **kwargs)
    try:
        return response.json()
    except ValueError as exc:
        raise FetchError(f"[{kwargs.get('platform') or url}] 响应不是合法 JSON：{exc}") from exc
