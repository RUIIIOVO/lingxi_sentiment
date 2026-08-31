# -*- coding: utf-8 -*-
# 封装公共方法 requests库中的get请求，传入url 返回content
# 使用方法：
# 引入： from common.requests_get import requests_get
# 使用： content = requests_get(url)
import os
import requests
import random
import urllib3
urllib3.disable_warnings()

# headers_obj = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
#                   'Safari/537.36 Edg/112.0.1722.64 ',
#     'Content-Type': 'text/html; charset=utf-8',
#     'Connection': 'close',
# }
headers_obj = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Cookie': os.getenv("WEIBO_COOKIE", ""),
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}


def requests_get(url, headers=None):
    if headers is None:
        headers = headers_obj
    # 代理池随机切换ip
    proxies_pool = [
        {'http': '117.94.126.227:9000'},
        {'http': '183.236.232.160:8080'},
        {'http': '117.68.194.137:9999'},
        {'http': '58.20.184.187:9091'},
        {'http': '113.121.23.38:9999'},
        {'http': '114.231.46.103:8888'},
        {'http': '27.192.171.53:9000'},
        {'http': '114.231.41.226:8888'},
        {'http': '114.232.110.10:8888'},
        {'http': '58.20.184.187:9091'},
        {'http': '223.241.119.217:1133'},
        {'http': '60.167.20.92:1133'},
        {'http': '222.66.202.6:80'},
        {'http': '114.232.110.204:8888'},
        {'http': '223.241.119.15:1133'},
        {'http': '114.232.110.204:8888'},
        {'http': '61.216.185.88:60808'},
        {'http': '36.134.91.82:8888'},
        {'http': '58.20.184.187:9091'},
        {'http': '182.34.37.173:9999'},
        {'http': '123.169.35.63:9999'},
        {'http': '113.121.20.68:9999'},
    ]
    proxies = random.choice(proxies_pool)
    response = requests.get(url=url, headers=headers, proxies=proxies, verify=False)
    response.encoding = 'utf-8'
    # print(response.text)
    return response.text


# print(requests_get("https://www.baidu.com"))
