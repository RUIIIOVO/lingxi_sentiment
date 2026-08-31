from django.shortcuts import render
import pymysql
import json
import datetime
from django.http import HttpResponse, JsonResponse

from db_config import db

# 连接数据库
def connect_database(function_name):
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
            # "sql_get_alarm_msg": sql_get_alarm_msg,
            # "sql_get_hot_search": sql_get_hot_search,
            "sql_get_events_source": sql_get_events_source,
            "sql_get_events_emotion": sql_get_events_emotion,
            "sql_get_events_kinds": sql_get_events_kinds,
            "sql_get_events_location": sql_get_events_location,
            "sql_get_medias_location": sql_get_medias_location,
        }
        if function_name in functions:
            return functions[function_name](cursor, connect)
    except Exception as e:
        print("连接数据库出错:", str(e))
    finally:
        cursor.close()  # 关闭游标
        connect.close()  # 关闭数据库连接


# 数据库获取：获取告警信息
# def sql_get_alarm_msg(cursor, connect):
#     sql = "select content,source,datetime from alarm_msg;"
#     cursor.execute(sql)
#     res = cursor.fetchall()
#     connect.commit()
#     return res


# # 后端接口：传递告警信息
# def api_get_alarm_msg(request):
#     if request.method == 'GET':
#         res = connect_database("sql_get_alarm_msg")
#         return JsonResponse(res, safe=False)

# 后端接口：传递告警信息
def api_get_alarm_msg(request):
    if request.method == 'GET':
        connect = pymysql.connect(
            host=db["host"],
            port=db["port"],  # 端口号
            user=db["user"],  # 数据库用户
            password=db["password"],  # 数据库密码
            database=db["database"]  # 要连接的数据库名称
        )
        cursor = connect.cursor()
        try:
            user_id = request.GET.get('user_id', '0')
            sql = f"""SELECT a.content, a.source, a.datetime, a.keyword, a.emotion,m.status
                        FROM alarm_msg a
                        JOIN monitor m ON a.keyword = m.keyword
                        WHERE a.user_id = '{user_id}' AND m.status = '1';"""
            cursor.execute(sql)
            res = cursor.fetchall()
            connect.commit()
            return JsonResponse(res, safe=False)
        except Exception as e:
            print(str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 后端接口：当前微博排行榜
def api_get_hot_search(request):
    if request.method == 'GET':
        connect = pymysql.connect(
            host=db["host"],
            port=db["port"],  # 端口号
            user=db["user"],  # 数据库用户
            password=db["password"],  # 数据库密码
            database=db["database"]  # 要连接的数据库名称
        )
        cursor = connect.cursor()
        try:
            platform = request.GET.get('platform', 'weibo')
            sql = f"select `rank`,`title`,`hot_value`,`url` from `{platform}_hot_search_rank`;"
            cursor.execute(sql)
            res = cursor.fetchall()
            connect.commit()
            my_list = []
            for i, v1 in enumerate(res):
                for j, v2 in enumerate(v1):
                    my_dict = {
                        "rank": str(int(v1[0]) + 1),
                        "title": v1[1],
                        "hot_value": v1[2],
                        "url": v1[3],
                    }
                my_list.append(my_dict)
            json_data = json.loads(json.dumps(my_list, ensure_ascii=False).replace("'", '"'))
            return JsonResponse(json_data, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# # 数据库获取：当前微博排行榜
# def sql_get_hot_search(cursor, connect):
#     sql = "select `rank`,`title`,`hot_value` from `weibo_hot_search_rank`;"
#     cursor.execute(sql)
#     res = cursor.fetchall()
#     connect.commit()
#     return res
#
#
# # 后端接口：当前微博排行榜
# def api_get_hot_search(request):
#     if request.method == 'GET':
#         platform = request.GET.get('platform', 'weibo')
#         print(platform)
#         res = connect_database("sql_get_hot_search")
#         my_list = []
#         for i, v1 in enumerate(res):
#             for j, v2 in enumerate(v1):
#                 my_dict = {
#                     "rank": str(int(v1[0]) + 1),
#                     "title": v1[1],
#                     "hot_value": v1[2],
#                 }
#             my_list.append(my_dict)
#         json_data = json.loads(json.dumps(my_list, ensure_ascii=False).replace("'", '"'))
#         return JsonResponse(json_data, safe=False)


# 数据库获取：事件库事件来源平台
def sql_get_events_source(cursor, connect):
    sql = """SELECT source, COUNT(*) as total_count
            FROM events
            GROUP BY source
            ORDER BY total_count DESC;"""
    cursor.execute(sql)
    res = cursor.fetchall()
    connect.commit()
    return res


# 后端接口：事件库事件来源平台
def api_get_events_source(request):
    if request.method == 'GET':
        res = connect_database("sql_get_events_source")
        my_list = []
        for i, v1 in enumerate(res):
            my_dict = {
                "title": v1[0],
                "num": v1[1],
            }
            my_list.append(my_dict)
        json_data = json.loads(json.dumps(my_list, ensure_ascii=False).replace("'", '"'))
        return JsonResponse(json_data, safe=False)


# 数据库获取：情感分析
def sql_get_events_emotion(cursor, connect):
    my_dict = {
        "total": 0,
        "positive": 0,
        "passive": 0,
    }
    sql = "select COUNT(*) from events where emotion = '积极';"
    cursor.execute(sql)
    res = cursor.fetchall()
    my_dict["positive"] = res[0][0]
    sql = "select COUNT(*) from events where emotion = '消极';"
    cursor.execute(sql)
    res = cursor.fetchall()
    my_dict["passive"] = res[0][0]
    sql = "select COUNT(*) from events;"
    cursor.execute(sql)
    res = cursor.fetchall()
    my_dict["total"] = res[0][0]
    connect.commit()
    return my_dict


# 后端接口：情感分析
def api_get_events_emotion(request):
    if request.method == 'GET':
        res = connect_database("sql_get_events_emotion")
        return JsonResponse(res, safe=False)


# 数据库获取：事件标签分类
def sql_get_events_kinds(cursor, connect):
    sql = """SELECT tag, COUNT(*) as total_count
            FROM events
            GROUP BY tag
            ORDER BY total_count DESC;"""
    cursor.execute(sql)
    res = cursor.fetchall()
    connect.commit()
    return res


# 后端接口：事件标签分类
def api_get_events_kinds(request):
    if request.method == 'GET':
        res = connect_database("sql_get_events_kinds")
        my_list = []
        for i, v1 in enumerate(res):
            my_dict = {
                "name": v1[0],
                "value": v1[1],
            }
            my_list.append(my_dict)
        json_data = json.loads(json.dumps(my_list, ensure_ascii=False).replace("'", '"'))
        return JsonResponse(json_data, safe=False)


# 数据库获取：事件发生地点
def sql_get_events_location(cursor, connect):
    sql = """SELECT location, COUNT(*) as total_count
            FROM events
            GROUP BY location
            ORDER BY total_count DESC;"""
    cursor.execute(sql)
    res = cursor.fetchall()
    res = [list(sublist) if isinstance(sublist, tuple) else sublist for sublist in res]
    res[0][1] = int(res[0][1] / 4)
    connect.commit()
    return res


# 后端接口：事件发生地点
def api_get_events_location(request):
    if request.method == 'GET':
        res = connect_database("sql_get_events_location")
        my_list = []
        for i, v1 in enumerate(res):
            my_dict = {
                "name": v1[0],
                "value": v1[1],
            }
            my_list.append(my_dict)
        json_data = json.loads(json.dumps(my_list, ensure_ascii=False).replace("'", '"'))
        return JsonResponse(json_data, safe=False)


# 数据库获取：各地媒体数量
def sql_get_medias_location(cursor, connect):
    sql = """SELECT location, COUNT(*) as total_count
            FROM medias
            GROUP BY location
            ORDER BY total_count DESC;"""
    cursor.execute(sql)
    res = cursor.fetchall()
    connect.commit()
    return res


# 后端接口：各地媒体数量
def api_get_medias_location(request):
    if request.method == 'GET':
        res = connect_database("sql_get_medias_location")
        my_list = []
        for i, v1 in enumerate(res):
            my_dict = {
                "name": v1[0],
                "value": v1[1],
            }
            my_list.append(my_dict)
        json_data = json.loads(json.dumps(my_list, ensure_ascii=False).replace("'", '"'))
        return JsonResponse(json_data, safe=False)


# 数据库获取：获取舆情数量变化
def sql_get_events_time(cursor, connect, select_time=datetime.datetime.now()):
    select_time_str = select_time.strftime('%Y-%m-%d %H:%M:%S')
    sql = f"select count(*) from events where datetime <= '{select_time_str}';"
    cursor.execute(sql)
    res = cursor.fetchall()
    connect.commit()
    return res


# 后端接口：获取近期舆情数量变化
def api_get_events_time(request):
    if request.method == 'GET':
        connect = pymysql.connect(
            host=db["host"],
            port=db["port"],  # 端口号
            user=db["user"],  # 数据库用户
            password=db["password"],  # 数据库密码
            database=db["database"]  # 要连接的数据库名称
        )
        cursor = connect.cursor()
        try:
            my_list = []
            # 获取当前时间
            select_time = datetime.datetime.now()
            range_value = int(request.GET.get('range_value', 12))
            if range_value == 7:
                hour_option = 24
            else:
                hour_option = 1
            for t in range(range_value):
                res = sql_get_events_time(cursor, connect, select_time)
                for i, v1 in enumerate(res):
                    my_dict = {
                        "select_time": select_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "value": v1[0],
                    }
                    my_list.append(my_dict)
                select_time -= datetime.timedelta(hours=hour_option)
            json_data = json.loads(json.dumps(my_list, ensure_ascii=False).replace("'", '"'))
            return JsonResponse(json_data, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 后端接口：更新词云
from word_cloud.main import generate_word_cloud


def api_update_word_cloud(request):
    if request.method == 'GET':
        generate_word_cloud()
        return JsonResponse({"code": 200, "msg": "更新成功"}, safe=False)
