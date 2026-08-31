# 获取微博热搜榜前50
import urllib.request
import urllib.parse
import json
import time
import datetime
from hot_search.reptile.common.requests_get import requests_get


# # 日期补零
# def fill_zero(time):
#     return f"{time:02d}"
#
#
# # 获取url
# def weibo_hot_search_url(year, month, day, hour):
#     # 微博官网接口
#     # url = 'https://weibo.com/ajax/side/hotSearch'
#     # 第三方接口 可查询历史记录
#     # https://getwb.weibolsrs.top/wbHistory?creation_time=2023-07-28%2018
#     # https://getwb.weibolsrs.top/searchTerms?table=2023-07-28%2018&option=default&keyword=%E5%BC%A0
#     # https://getwb.weibolsrs.top/searchTerms?table=2023-07-28%2018&option=default&keyword=张
#     base_url = 'https://getwb.weibolsrs.top/wbHistory?creation_time='
#     now_data = datetime.date.today()
#     give_data = datetime.date(year, month, day)
#     if give_data != now_data:
#         hour = 0
#     creation_time = f"{fill_zero(year)}-{fill_zero(month)}-{fill_zero(day)} {fill_zero(hour)}"
#     # urllib.parse.quote 用于转义请求中的空格，将空格转为%20
#     url = base_url + urllib.parse.quote(creation_time)
#     return url
#
#
# # 获取当前时间
# def get_time(type=None):
#     t = time.localtime()
#     year = t.tm_year
#     month = t.tm_mon
#     day = t.tm_mday
#     hour = t.tm_hour
#     time_obj = {
#         "year": year,
#         "month": month,
#         "day": day,
#         "hour": hour,
#     }
#     if type is not None:
#         return time_obj[type]
#     else:
#         return time_obj
#
#
# # 获取微博热搜榜单
# def weibo_hot_search(limit=50, year=get_time("year"), month=get_time("month"), day=get_time("day"),
#                      hour=get_time("hour")):
#     if limit <= 0:
#         limit = 1
#     elif limit > 50:
#         limit = 50
#     url = weibo_hot_search_url(year, month, day, hour)
#     print(url)
#     content = json.loads(requests_get(url))[:limit]
#     content = str(content).replace("'", '"')
#     # 数据第一条为置顶数据
#     # 写入文件/后期可更改为存入数据库，或注释掉写入文件的代码，由后端调取接口。得到content
#     # with open('../reptile_static/weibo_hot_search.json', 'w', encoding='utf-8') as fs:
#     #     fs.write(content)
#     return content
#
#
# if __name__ == '__main__':
#     print(weibo_hot_search(limit=1))
# #     print(weibo_hot_search(1, day=20, hour=2))


def weibo_hot_search(limit=50):
    url = "https://weibo.com/ajax/side/hotSearch"
    # content = json.loads(requests_get(url))["data"]["realtime"][:limit]
    # content = str(content).replace(' ', '').replace("'", '"')
    content = requests_get(url)
    # print(content[2])
    # del content[2]
    # content = content[:limit]
    return content


if __name__ == '__main__':
    print(weibo_hot_search())
