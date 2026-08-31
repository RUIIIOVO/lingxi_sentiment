import pymysql
import json
from django.http import HttpResponse, JsonResponse

from db_config import db
# 连接数据库
def connect_database(function_name, limit=50):
    connect = pymysql.connect(
        host=db["host"],
        port=db["port"],  # 端口号
        user=db["user"],  # 数据库用户
        password=db["password"],  # 数据库密码
        database=db["database"]  # 要连接的数据库名称
    )
    cursor = connect.cursor()
    try:
        functions = {
            "get_weibo_day_data": get_weibo_day_data,
            "get_weibo_week_data": get_weibo_week_data,
            "get_weibo_month_data": get_weibo_month_data,
            "get_chart_data": get_chart_data,
            "get_baidu_data": get_baidu_data,
            "get_rank_data": get_rank_data
        }
        if function_name in functions:
            return functions[function_name](cursor, connect)
    except Exception as e:
        print("连接数据库出错:", str(e))
    finally:
        cursor.close()  # 关闭游标
        connect.close()  # 关闭数据库连接


# 数据库获取：获取当天微博热搜第一
def get_weibo_day_data(cursor, connect):
    sql = "select `title`,`hot_value`,`datetime` from weibo_hot_search_rank where `rank` = 0;"
    cursor.execute(sql)
    res = cursor.fetchall()
    my_dict = {
        "title": res[0][0],
        "hot_value": res[0][1],
        "datetime": res[0][2],
    }
    connect.commit()
    return my_dict


# 后端接口：获取当天微博热搜第一
def api_get_weibo_day_data(request):
    if request.method == 'GET':
        res = connect_database("get_weibo_day_data")
        return JsonResponse(res, safe=False)


# 数据库获取：获取微博一周内不同时间段最高热度数据
def get_weibo_week_data(cursor, connect):
    week_data = []
    for hour in range(24):
        sql = f"""
            SELECT `title`, `t{hour}`
            FROM weibo_hot_search_values
            WHERE DATE_FORMAT(`datetime`, "%%Y-%%m-%%d") BETWEEN DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 7 DAY), "%%Y-%%m-%%d") AND DATE_FORMAT(NOW(), "%%Y-%%m-%%d")
            ORDER BY (`t{hour}`+0) DESC
            LIMIT 1;
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        my_dict = {
            "title": res[0][0],
            "hot_value": res[0][1],
        }
        week_data.append(my_dict)
    if week_data:
        max_hot_value = max(week_data, key=lambda x: x['hot_value'])
    else:
        print("No data found")
    connect.commit()
    return max_hot_value if week_data else None


# 后端接口：获取本周微博热搜第一
def api_get_weibo_week_data(request):
    if request.method == 'GET':
        res = connect_database("get_weibo_week_data")
        return JsonResponse(res, safe=False)


# 数据库获取：获取微博本月内不同时间段最高热度数据
def get_weibo_month_data(cursor, connect):
    month_data = []
    for hour in range(24):
        sql = f"""
            SELECT `title`, `t{hour}`
            FROM weibo_hot_search_values
            WHERE DATE_FORMAT(`datetime`, "%%Y-%%m") BETWEEN DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 1 MONTH), "%%Y-%%m") AND DATE_FORMAT(NOW(), "%%Y-%%m")
            ORDER BY (`t{hour}`+0) DESC
            LIMIT 1;
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        my_dict = {
            "title": res[0][0],
            "hot_value": res[0][1],
        }
        month_data.append(my_dict)
    if month_data:
        max_hot_value = max(month_data, key=lambda x: x['hot_value'])
        print(max_hot_value)
    else:
        print("No data found")
    connect.commit()
    return max_hot_value if month_data else None


# 后端接口：获取本月微博热搜第一
def api_get_weibo_month_data(request):
    if request.method == 'GET':
        res = connect_database("get_weibo_month_data")
        return JsonResponse(res, safe=False)


# 数据库获取：获取当前热榜前十最近12小时的数据
def get_chart_data(cursor, connect):
    # for rank in range(10):
    # sql = f"""
    #     select *
    #     from weibo_hot_search_values
    #     where `title` = (select `title` from weibo_hot_search_rank where `rank` = {rank})
    #     and
    #     DATE_FORMAT(`datetime`, '%Y-%m-%d') BETWEEN DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 2 DAY), '%Y-%m-%d') AND DATE_FORMAT(NOW(), '%Y-%m-%d');
    # """
    sql = f"""
                select *
                from weibo_hot_search_values 
                where 
                DATE_FORMAT(`datetime`, '%Y-%m-%d') BETWEEN DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 30 DAY), '%Y-%m-%d') AND DATE_FORMAT(NOW(), '%Y-%m-%d');
            """
    cursor.execute(sql)
    res = cursor.fetchall()
    # 在数据库中获取数据并转为json
    initial_data = []
    for r in res:
        my_dict = {}
        for i, key in enumerate(
                ["title", "datetime", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11", "t12",
                 "t13", "t14", "t15", "t16", "t17", "t18", "t19", "t20", "t21", "t22", "t23"]):
            if r[i + 1] is None:
                my_dict[key] = 0
            else:
                my_dict[key] = r[i + 1]
        initial_data.append(my_dict)

    # 定义排序键函数，按照t0到t23不为0的数量进行排序
    def sort_key(obj):
        count = sum(1 for val in obj.values() if val != 0)
        return -count  # 使用负数表示逆序排序

    # 使用排序键函数进行排序，取前十条t0-t2不为0数量最少的数据
    sorted_data = sorted(initial_data, key=sort_key)[:10]
    # 将排序好的数据转化为前端折线图需要的数据格式
    final_data = []
    for data in sorted_data:
        for item in data:
            if item == "title" or item == "datetime":
                continue
            time = int(item[1:])
            final_dict = {
                "title": data["title"],
                "datetime": data["datetime"].replace(hour=time),
                "value": data[f"t{time}"]
            }
            final_data.append(final_dict)
    connect.commit()
    return final_data


# 后端接口：获取近期热门事件24小时变化折线图数据
def api_get_chart_data(request):
    if request.method == 'GET':
        res = connect_database("get_chart_data")
        return JsonResponse(res, safe=False)


# 数据库获取：获取当前排行榜
def get_rank_data(cursor, connect):
    sql = "select `rank`,`title`,`hot_value` from `weibo_hot_search_rank`;"
    cursor.execute(sql)
    res = cursor.fetchall()
    my_list = []
    for i, v1 in enumerate(res):
        for j, v2 in enumerate(v1):
            my_dict = {
                "rank": str(int(v1[0])+1),
                "title": v1[1],
                # "value": v1[2],
            }
        my_list.append(my_dict)
    json_data = json.loads(json.dumps(my_list, ensure_ascii=False).replace("'", '"'))
    connect.commit()
    return json_data


# 后端接口：获取本月微博热搜第一
def api_get_rank_data(request):
    if request.method == 'GET':
        res = connect_database("get_rank_data")
        return JsonResponse(res, safe=False)


# 数据库获取：获取百度热搜榜前三十
def get_baidu_data(cursor, connect):
    sql = "select title,hot_value,url from baidu_hot_search limit 30;"
    cursor.execute(sql)
    res = cursor.fetchall()
    my_list = []
    for i, v1 in enumerate(res):
        for j, v2 in enumerate(v1):
            my_dict = {
                "title": v1[0],
                "hot_value": v1[1],
                "url": v1[2],
            }
        my_list.append(my_dict)
    json_data = json.loads(json.dumps(my_list, ensure_ascii=False).replace("'", '"'))
    connect.commit()
    return json_data


# 后端接口：获取百度热搜榜前三十
def api_get_baidu_hot_search(request):
    if request.method == 'GET':
        limit = request.GET.get('limit')
        res = connect_database("get_baidu_data", limit)
        return JsonResponse(res, safe=False)
    # elif request.method == 'POST':
    #     limit = request.POST.get('limit')
    #     res = connect_database(limit)
    #     return JsonResponse(res, safe=False)
