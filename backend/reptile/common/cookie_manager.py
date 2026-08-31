# -*- coding: utf-8 -*-
"""各平台 Cookie 的统一读取。

Cookie 一律从环境变量取，见 backend/.env.example。

关于"自动更新 token"：几个目标站点实测下来都没有可自动化的空间——
- 微博热搜榜只校验 Referer，压根不看 Cookie；
- 微博的用户/评论/搜索接口一律要求真实登录态，官方游客身份（passport 的
  genvisitor）换来的 SUB 只能让响应从 432 变成 `ok:-100` 跳登录页，拿不到数据；
- 百度热榜免 Cookie，百度搜索页无论带不带游客 BAIDUID 都跳验证码；
- 知乎接口需要 x-zse-96 签名，游客身份直接 401。

所以这里不做游客身份申请，只做两件事：读取环境变量，以及在必需的 Cookie
缺失时明确报错，让上层跳过该平台并留下日志，而不是静默返回空数据。
"""
import os

from reptile.common.http_client import AuthRequired

# 平台 -> 存放登录态 Cookie 的环境变量名
ENV_KEYS = {
    "weibo": "WEIBO_COOKIE",
    "zhihu": "ZHIHU_COOKIE",
    "baidu": "BAIDU_COOKIE",
    "sina": "SINA_COOKIE",
}

# 这些平台没有登录 Cookie 就完全拿不到数据
REQUIRED = {"zhihu"}


def get_cookie(platform, required=None):
    """返回可直接塞进 headers 的 Cookie 字符串，未配置时返回空串。

    required 为 True，或平台在 REQUIRED 里，缺 Cookie 时抛 AuthRequired。
    """
    env_key = ENV_KEYS.get(platform, "")
    value = os.getenv(env_key, "").strip() if env_key else ""
    if value:
        return value

    if required or platform in REQUIRED:
        raise AuthRequired(
            platform,
            f"该平台不接受游客身份，请在环境变量 {env_key} 中提供登录后的 Cookie",
        )
    return ""


def has_cookie(platform):
    """内容抓取前先问一句：这个平台的登录态配了没有。"""
    env_key = ENV_KEYS.get(platform, "")
    return bool(env_key and os.getenv(env_key, "").strip())
