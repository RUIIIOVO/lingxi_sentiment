# linux中无法读取上一级目录时在import前添加
import gzip
import sys
import os
from io import BytesIO

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

from lxml import etree
import re
import json
from datetime import datetime
from hot_search.reptile.common.requests_get import requests_get
from paddlenlp import Taskflow

# https://weibo.cn/
headers = {
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

# https://m.weibo.cn/
m_headers = {
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


# 获取评论和评论用户个人信息
def get_weibo_comments(mid):
    url = f"https://m.weibo.cn/comments/hotflow?id={mid}&mid={mid}&max_id_type=0&display=0&retcode=6102"
    content = json.loads(requests_get(url, m_headers))
    data = content["data"]["data"]

    arr = []
    for i in data:
        if i["user"]["gender"] == 'f':
            sex = '女'
        else:
            sex = '男'
        person_url = f"https://weibo.cn/{i['user']['id']}/info"
        person_content = requests_get(person_url, headers).encode('utf-8')  # 将内容转换为bytes类型
        tree = etree.HTML(person_content)
        birthday_info = tree.xpath("//div[@class='c'][3]//text()")
        birthday_info = ''.join(birthday_info)  # 将列表转换为字符串
        # 使用正则表达式提取生日信息
        birthday_match = re.search(r'生日:(\d{4}-\d{2}-\d{2})', birthday_info)
        if birthday_match:
            birthday = birthday_match.group(1)
            # 若出现1000年之前的生日，则设置年龄为0
            if int(birthday[:4]) < 1000:
                age = 0
            else:
                # 计算年龄
                today = datetime.today()
                birth_date = datetime.strptime(birthday, '%Y-%m-%d')
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        else:
            birthday = "未知"
            birth_date = datetime(1900, 1, 1)  # 设置一个默认日期
            age = 0

        # 去除HTML标签和表情
        clean_data = re.sub(r'<[^>]+>', '', i["text"])  # 去除HTML标签
        clean_data = re.sub(r'\[.*?\]', '', clean_data)  # 去除表情

        # print(clean_data)

        # 提取评论的汉字部分
        chinese_comment = re.findall(r'[\u4e00-\u9fa5]+', clean_data)
        chinese_comment = ','.join(chinese_comment)
        # print(chinese_comment)
        # 情感分析
        if chinese_comment != '':
            # senta = Taskflow("sentiment_analysis")
            # item = senta(chinese_comment)
            if item[0]["label"] == "positive":
                emotion = '积极'
            else:
                emotion = '消极'
        else:
            break
        my_dict = {
            "nickname": i["user"]["screen_name"],
            "sex": sex,
            "ip": i["source"][2:],
            # "birthday": birthday,
            "age": age,
            "emotion": emotion,
            "text": chinese_comment,
        }
        # print(my_dict["text"])
        arr.append(my_dict)
    return arr


from bs4 import BeautifulSoup


def clean_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找包含 JSON 数据的所有 <script> 标签
    script_tags = soup.find_all('script')

    for script in script_tags:
        if 'var $render_data' in script.text:
            js_code = script.text
            # 将js转为json
            start_index = js_code.find("[{") + 1
            end_index = js_code.find("}][0] || {}") + 1
            json_str = js_code[start_index:end_index]
            # 获取text
            json_data = json.loads(json_str)["status"]["text"]
            # 去除html标签
            text = BeautifulSoup(json_data, "html.parser").get_text()
            return text


# 获取媒体信息
def get_weibo_media(mid):
    url = f"https://m.weibo.cn/detail/{mid}"
    html_content = requests_get(url, m_headers)
    # 定义正则表达式模式
    user_id_pattern = r'"id":\s*(\d+)'
    screen_name_pattern = r'"screen_name":\s*"([^"]+)"'

    # 使用正则表达式进行匹配
    user_id_match = re.search(user_id_pattern, html_content)
    screen_name_match = re.search(screen_name_pattern, html_content)

    text = clean_text(html_content)
    # 如果找到了匹配结果
    if user_id_match and screen_name_match:
        # 提取用户id和screen_name
        user_id = user_id_match.group(1)
        screen_name = screen_name_match.group(1)
        person_url = f"https://weibo.cn/{user_id}/info"
        person_content = requests_get(person_url, headers).encode('utf-8')  # 将内容转换为bytes类型
        tree = etree.HTML(person_content)
        person_info = tree.xpath("//div[@class='c'][3]//text()")
        person_info = ''.join(person_info)  # 将列表转换为字符串
        # # 使用正则表达式匹配地区信息
        location_pattern = r'地区:(.*?)(?:生日:|认证信息:|微博简介:|$)'
        location_match = re.search(location_pattern, person_info)
        location = location_match.group(1).strip() if location_match else '其他'
        # 二次过滤
        # location = location.replace(' ', '')[:3]
        # if location in ['内蒙古', '黑龙江', '其他']:
        #     province = location
        # else:
        #     province = location[:-1]

        # 打印用户id和screen_name
        my_dict = {
            "user_id": user_id,
            "media": screen_name,
            "location": location,
            "text": text,
        }
    else:
        my_dict = {
            "user_id": None,
            "media": None,
            "location": '其他',
            "text": None,
        }
    return my_dict


# 获取事件脉络链接
import urllib.request
import urllib.parse
import random


# 百度指数获取
def get_baidu_process(title):
    title = urllib.parse.quote(title)

    url = f"https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=5&tn=25017023_2_dg&wd={title}&oq=%25E5%25A8%2583%25E5%2593%2588%25E5%2593%2588%25E5%2588%259B%25E5%25A7%258B%25E4%25BA%25BA%25E5%25AE%2597%25E5%25BA%2586%25E5%2590%258E%25E5%258E%25BB%25E4%25B8%2596&rsv_pq=b2dd7758003bc46f&rsv_t=92103N7p091dB9cikK17yKheQIEfbXyynPUSYIj227xG1e4Di5jTUyGM3y8B5fyQff2QIQ&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t"

    baidu_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cookie': os.getenv("BAIDU_COOKIE", "")
    }

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
    request = urllib.request.Request(url=url, headers=baidu_headers)
    handler = urllib.request.ProxyHandler(proxies=proxies)
    opener = urllib.request.build_opener(handler)
    response = opener.open(request)
    content = response.read().decode('utf8')
    tree = etree.HTML(content)
    try:
        link = tree.xpath('//a[@class="jump_2zuOQ"]/@href')[0]
        # 获取真实链接
        import requests
        from html.parser import HTMLParser
        response = requests.get(url=link, allow_redirects=False)
        real_link = response.headers.get('Location')

        # 获取事件脉络信息
        event_content = requests_get(real_link)
        event_tree = etree.HTML(event_content)
        time_arr = event_tree.xpath('//div[@class="item"]//span[@class="time c-gap-left-small"]//text()')
        text_arr = event_tree.xpath('//a[@class="content-link  c-line-clamp1"]//text()')
        # 去除空格项
        text_arr = list(filter(lambda x: x.strip(), text_arr))
        # 去除每一项多余的空格
        text_arr = [x.strip() for x in text_arr]

        from datetime import datetime, timedelta

        # 将时间字符串转换成指定格式
        def format_time(time_str):
            if "小时前" in time_str:
                hours_ago = int(time_str.split("小时前")[0])
                time = datetime.now() - timedelta(hours=hours_ago)
                return time.strftime('%Y-%m-%d %H:%M:%S')
            elif "昨天" in time_str:
                time = datetime.now() - timedelta(days=1)
                time = time.replace(hour=int(time_str.split(' ')[1].split(':')[0]),
                                    minute=int(time_str.split(' ')[1].split(':')[1]))
                return time.strftime('%Y-%m-%d %H:%M:%S')
            elif "今天" in time_str:
                time = datetime.now()
                time = time.replace(hour=int(time_str.split(' ')[1].split(':')[0]),
                                    minute=int(time_str.split(' ')[1].split(':')[1]))
                return time.strftime('%Y-%m-%d %H:%M:%S')
            elif "年" in time_str:
                time = datetime.strptime(time_str, '%Y年%m月%d日')
                return time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                time = datetime.strptime(time_str, '%m月%d日 %H:%M')
                current_year = datetime.now().year
                time = time.replace(year=current_year)  # 替换为当前年份
                return time.strftime('%Y-%m-%d %H:%M:%S')

        # 将时间格式化
        formatted_time_arr = [format_time(time) for time in time_arr]

        result = [{"time": time, "text": text} for time, text in zip(formatted_time_arr, text_arr)]

        return result
    except:
        pass


# 微博榜单存入数据库
"""
存入逻辑：
1.首先拿到爬虫获取的数据，遍历每一条新数据
2.提取title（标题）、rank（排名）、hot_value（热度值）等信息
3.更新排名表，排名表不新增数据，始终展示最新榜单前50数据  
4.插入总表，判断要插入的数据是否已经存在，不存在则存入总表
5.插入热度值表，一共有三种情况：
    a.总表无数据，则热度值表也一定没有数据（新数据第一次操作） => 插入总表、热度值表
    b.热度值表存在当天数据，根据当天时间，更新当天数据即可
    c.热度值表不存在当天数据，新增当天数据，后续重复b操作
"""

import time


# 获取当前时间
def get_time(type=None):
    t = time.localtime()
    year = t.tm_year
    month = t.tm_mon
    day = t.tm_mday
    hour = t.tm_hour
    time_obj = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
    }
    if type is not None:
        return time_obj[type]
    else:
        return time_obj


import pymysql


def get_weibo_data():
    url = "https://weibo.com/ajax/side/hotSearch"
    content = requests_get(url, headers)
    return content


from db_config import db


# 获取mid
def get_mid(title):
    print(title)

    url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26t%3D10%26q%3D" + title + "&page_type=searchall"
    content = json.loads(requests_get(url, m_headers))
    card = str(content["data"]["cards"])
    # 定义正则表达式模式
    mid_pattern = r'mid=(\d+)'
    # 使用正则表达式进行匹配
    mid_match = re.search(mid_pattern, card)
    mid = mid_match.group(1)

    # card = content["data"]["cards"][0]
    # if "mblog" in card:
    #     mblog = card["mblog"]
    #     mid = mblog["ads_material_info"]["mid"] if "ads_material_info" in mblog else mblog["mid"]
    # elif "card_group" in card:
    #     mid = card["card_group"][0]["mblog"]["mid"]
    # else:
    #     mid =
    print(mid)
    return mid


# 获取事件标签
def get_tag(title):
    try:
        title = urllib.parse.quote(title)

        url = "https://s.weibo.com/weibo?q=%23" + title + "%23&t=547&band_rank=1&Refer=top"
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

        s_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cookie": os.getenv("SINA_COOKIE", ""),
            "priority": "u=1, i",
            "referer": "https://s.weibo.com/weibo?q=%23%E6%A8%8A%E6%8C%AF%E4%B8%9C%E5%9B%9E%E5%BA%94%E9%80%80%E5%BD%B9%E4%BC%A0%E9%97%BB%23&t=547&band_rank=1&Refer=top",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        proxies = random.choice(proxies_pool)
        request = urllib.request.Request(url=url, headers=s_headers)
        handler = urllib.request.ProxyHandler(proxies=proxies)
        opener = urllib.request.build_opener(handler)
        response = opener.open(request)
        htmls = response.read()
        buff = BytesIO(htmls)
        f = gzip.GzipFile(fileobj=buff)
        content = f.read().decode('utf-8')
        tree = etree.HTML(content)
        tag_text = tree.xpath("//a[@class='tag']/text()")[0]
        tag = tuple(map(str.strip, tag_text.split('-')))
        print(tag)
        return tag if tag else "其他"
    except Exception as e:
        print("无标签", Exception, str(e))
        return "其他"


def save_data_weibo():
    try:
        connect = pymysql.connect(
            host=db["host"],
            port=db["port"],  # 端口号
            user=db["user"],  # 数据库用户
            password=db["password"],  # 数据库密码
            database=db["database"]  # 要连接的数据库名称
        )
        cursor = connect.cursor()
        data = json.loads(get_weibo_data())["data"]["realtime"]
        if data:
            # print(data)
            # sql_get_msg = "select mid,title from weibo_hot_search_msg where `datetime` like '2023-08-09 17%';"
            # # 插入总榜信息
            # sql_insert_msg = "insert into weibo_hot_search_msg(`title`)values(%s)"
            # 更新排名
            sql_update_rank = "UPDATE weibo_hot_search_rank SET `title` = %s ,`hot_value` = %s WHERE `rank` = %s LIMIT 50"
            # sql_update_rank = "insert into weibo_hot_search_rank(`title`,`hot_value` ,`rank`)values(%s,%s,%s)"
            # 插入热度值
            now_hour = get_time("hour")
            sql_insert_hotvalue = f"insert into weibo_hot_search_values(`title`,`t{now_hour}`)values(%s,%s)"
            # 更新当天热度值
            sql_update_hotvalue = f"UPDATE weibo_hot_search_values SET `t{now_hour}` = %s WHERE `title` = %s " + 'and DATE_FORMAT(`datetime`,"%%Y-%%m-%%d")=DATE_FORMAT(NOW(),"%%Y-%%m-%%d")'

            for index, d in enumerate(data):
                # 去除广告数据
                if 'ad_type' in d.keys():
                    continue

                title = d["note"]
                rank = d["rank"]
                hot_value = d["num"]
                # if "flag_desc" in d:
                #     tag = d["flag_desc"]
                # else:
                #     tag = get_tag(title)
                tag = get_tag(title)
                mid = get_mid(title)
                # tag = d["category"]
                # tag = d["flag_desc"] if "flag_desc" in d else ""
                # mid = d["mid"]

                source_arr = ['新浪微博', '百度', '抖音', '今日头条', '知乎', '微信']
                weights = [0.3, 0.2, 0.2, 0.1, 0.1, 0.1]

                import random

                source = random.choices(source_arr, weights=weights, k=1)[0]

                # url = f"https://s.weibo.com/weibo?q=%23{d['note']}%23&t=31&band_rank=1&Refer=top"

                # 更新排名
                rank_values = [(title, hot_value, rank)]
                cursor.executemany(sql_update_rank, rank_values)
                connect.commit()

                # 判断要插入的数据是否已经存在，不存在则存入总榜
                sql_get_msg = f"select title from events where `title` = '{title}'"
                cursor.execute(sql_get_msg)
                get_msg_result = cursor.fetchall()
                # 插入总榜信息
                sql_insert_msg = "insert into events(`title`,`hot_value`,`tag`,`emotion`,`source`,`media`,`location`,`text`)values(%s,%s,%s,%s,%s,%s,%s,%s)"
                # 总表里没有该热点，则插入总榜
                if len(get_msg_result) == 0:
                    # 插入用户信息表
                    sql_insert_people = "INSERT INTO people (`title`, `nickname`, `sex`, `ip`, `age`) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = VALUES(title), sex = VALUES(sex), ip = VALUES(ip), age = VALUES(age)"
                    comments_data = get_weibo_comments(mid)
                    emotion_arr = []
                    for d in comments_data:
                        people_values = (title, d["nickname"], d["sex"], d["ip"], d["age"])
                        cursor.execute(sql_insert_people, people_values)
                        connect.commit()
                        emotion_arr.append(d["emotion"])

                    from collections import Counter
                    # 使用Counter统计数组中每个元素出现的次数,找到出现次数最多的元素
                    emotion_count = Counter(emotion_arr)
                    if emotion_count:
                        most_common_emotion = emotion_count.most_common(1)[0][0]
                    else:
                        # 处理列表为空的情况，可以选择给 most_common_emotion 赋予一个默认值或者执行其他操作
                        most_common_emotion = "积极"
                    emotion = most_common_emotion
                    emotion_count_dict = {
                        "positive": emotion_count["积极"],
                        "passive": emotion_count["消极"]
                    }
                    sql_insert_emotions = "insert into emotions(`title`,`positive`,`passive`)values(%s,%s,%s)"
                    emotion_values = [(title, emotion_count_dict["positive"], emotion_count_dict["passive"])]
                    cursor.executemany(sql_insert_emotions, emotion_values)
                    connect.commit()

                    # 获取media, location, text
                    media_data = get_weibo_media(mid)
                    media = media_data["media"]
                    location = media_data["location"]
                    text = media_data["text"]
                    msg_values = [(title, hot_value, tag, emotion, source, media, location, text)]
                    cursor.executemany(sql_insert_msg, msg_values)
                    connect.commit()
                    print(msg_values)

                    # 插入百度事件脉络(后续改为对比数据库中数据，只存入新的数据)
                    sql_insert_process = "insert into timeline(`title`,`comment`,`happen_time`)values(%s,%s,%s)"
                    baidu_process = get_baidu_process(title)

                    if baidu_process:
                        for p in baidu_process:
                            process_values = [(title, p["text"], p["time"])]
                            cursor.executemany(sql_insert_process, process_values)
                            connect.commit()

                # sql_get_msg = f"select title from weibo_hot_search_msg where `title` = '{title}'"
                # cursor.execute(sql_get_msg)
                # get_msg_result = cursor.fetchall()
                # # 总表里没有该热点，则插入总榜
                # if len(get_msg_result) == 0:
                #     msg_values = [title]
                #     cursor.executemany(sql_insert_msg, msg_values)
                #     connect.commit()

                # 判断该热点是否有当天记录
                sql_get_hotvalue = f"select title from weibo_hot_search_values where `title` = '{title}' and DATE_FORMAT(`datetime`,'%Y-%m-%d')=DATE_FORMAT(NOW(),'%Y-%m-%d')"
                cursor.execute(sql_get_hotvalue)
                get_hotvalue_result = cursor.fetchall()
                # 该热点没有当天的记录则新增
                if len(get_hotvalue_result) == 0:
                    # 插入热度值
                    hotvalue_insert_values = [(title, hot_value)]
                    cursor.executemany(sql_insert_hotvalue, hotvalue_insert_values)
                    connect.commit()
                else:
                    # 更新当前时间的热度值
                    hotvalue_update_values = [(hot_value, title)]
                    cursor.executemany(sql_update_hotvalue, hotvalue_update_values)
                    connect.commit()

    except Exception as e:
        print("error!", Exception, str(e))
        pass


if __name__ == '__main__':
    save_data_weibo()
    # get_tag("李佳琦在自己直播间办了披哥1.5公")
