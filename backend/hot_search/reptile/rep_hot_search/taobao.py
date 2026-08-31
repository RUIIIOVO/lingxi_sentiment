# coding=gb2312
# 获取百度热搜榜前50
from lxml import etree
# from hot_search.reptile.common.requests_get import requests_get

import requests
import random
import urllib3
urllib3.disable_warnings()

headers_obj = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
                  'Safari/537.36 Edg/112.0.1722.64 ',
    'Content-Type': 'text/html; charset=utf-8',
    'Connection': 'close'
}

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
# print(proxies)


def requests_get(url, headers=None):
    if headers is None:
        headers = headers_obj
    response = requests.get(url=url, headers=headers, proxies=proxies, verify=False)
    response.encoding = 'utf-8'
    # print(response.text)
    return response.text

def get_data(limit=50):
    if limit <= 0:
        limit = 1
    url = "https://s.taobao.com/search?q=&spm=a21bo.jianhua.201867-main.1.6ae12a8954SMfI"
    content = requests_get(url)
    print(content)
    with open('../reptile_static/1.html', 'w', encoding='utf-8') as fs:
        fs.write(content)
    tree = etree.HTML(content)
    data = tree.xpath('//div[@class="Price--priceWrapper--Q0Dn7pN"]')[:limit]
    print(data)
    hot_list_value = tree.xpath("//div[@class='hot-index_1Bl1a']/text()")[:limit]
    # # print(hot_list_value)
    # hot_list = [{
    #     "title": a.replace(' ', ''),
    #     "hot_value": b.replace(' ', ''),
    #     "url": f"https://www.baidu.com/s?wd={a.replace(' ', '')}&sa=fyb_news&rsv_dl=fyb_news"}
    #     for a, b in zip(hot_list_title, hot_list_value)]
    # # print(hot_list)
    # hot_list = str(hot_list).replace("'", '"')
    # # with open('../reptile_static/baidu_hot_search.json', 'w', encoding='utf-8') as fs:
    # #     fs.write(hot_list)
    # return hot_list


if __name__ == '__main__':
    get_data()

