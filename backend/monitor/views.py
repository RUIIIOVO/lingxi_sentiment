import pymysql
import json
import datetime
from django.http import HttpResponse, JsonResponse
from db_config import db

# def connect_database(function_name):
#     connect = pymysql.connect(
#         host="127.0.0.1",
#         port=3306,  # 端口号
#         user="root",  # 数据库用户
#         password="123456",  # 数据库密码
#         database="sentiment"  # 要连接的数据库名称
#     )
#     cursor = connect.cursor()
#     try:
#         functions = {
#             # "sql_get_total_monitor": sql_get_total_monitor,
#         }
#         if function_name in functions:
#             return functions[function_name](cursor, connect)
#     except Exception as e:
#         print("连接数据库出错:", str(e))
#     finally:
#         cursor.close()  # 关闭游标
#         connect.close()  # 关闭数据库连接
#
#
# # 数据库获取：获取所有预警数据
# def sql_get_total_monitor(cursor, connect):
#     sql = "SELECT keyword,status,source,start_time,end_time FROM monitor;"
#     cursor.execute(sql)
#     res = cursor.fetchall()
#     connect.commit()
#     return res


# 后端接口：传递预警信息
def api_get_total_monitor(request):
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
            sql = f"SELECT keyword,status,source,start_time,end_time FROM monitor WHERE user_id = {user_id};"
            cursor.execute(sql)
            res = cursor.fetchall()
            connect.commit()
            response = []
            for result in res:
                item = {
                    "keyword": result[0],
                    "status": result[1],
                    "source": result[2].split(),
                    "time": f"{result[3]} - {result[4]}",
                }
                response.append(item)
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 后端接口:删除预警
def api_delete_monitor(request):
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
            keyword = request.GET.get('keyword')
            user_id = request.GET.get('user_id', '0')
            sql = f"DELETE FROM monitor WHERE keyword = '{keyword}' AND user_id = {user_id};"
            cursor.execute(sql)
            # 执行删除操作必须提交
            connect.commit()
            sql_delete = f"DELETE FROM alarm_msg WHERE keyword = '{keyword}' AND user_id = {user_id};"
            cursor.execute(sql_delete)
            connect.commit()
            return JsonResponse({"code": 200, "data": "删除成功"}, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 后端接口:获取详情中的预警记录
def api_get_one_alarm_msg(request):
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
            keyword = request.GET.get('keyword')
            user_id = request.GET.get('user_id', '0')
            sql = f"select content,source,datetime,keyword,emotion from alarm_msg WHERE keyword = '{keyword}' AND user_id = {user_id};"
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            connect.commit()
            return JsonResponse(res, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 新增预警
def api_add_monitor(request):
    if request.method == 'POST':
        connect = pymysql.connect(
            host=db["host"],
            port=db["port"],  # 端口号
            user=db["user"],  # 数据库用户
            password=db["password"],  # 数据库密码
            database=db["database"]  # 要连接的数据库名称
        )
        cursor = connect.cursor()
        try:
            form = request.POST
            keyword = form["keyword"]
            user_id = form["user_id"]
            status = 1

            # 获取当前时间
            current_time = datetime.datetime.now().replace(microsecond=0)

            # 处理时间字符串，去除毫秒部分
            time1_str = form["time1"]
            time1_str = time1_str[:-5]  # 去除毫秒部分
            time1 = datetime.datetime.fromisoformat(time1_str).replace(hour=current_time.hour,minute=current_time.minute,second=current_time.second)

            time2_str = form["time2"]
            time2_str = time2_str[:-5]  # 去除毫秒部分
            time2 = datetime.datetime.fromisoformat(time2_str).replace(hour=current_time.hour,minute=current_time.minute,second=current_time.second)

            sources = form.getlist("source[]")  # 获取多个source值

            # 将多个source值组合成字符串
            source = ' '.join(sources)
            # print("===================",keyword,user_id)
            # 查询数据库，若关键词已存在则不能重复插入
            sql_search = f"select * from monitor where keyword = '{keyword}' and user_id = {user_id};"
            cursor.execute(sql_search)
            res = cursor.fetchall()
            print(res)
            if len(res) == 0:
                sql_insert = "insert into monitor(keyword, status, source, start_time, end_time, user_id)values(%s,%s,%s,%s,%s,%s)"
                insert_values = [(keyword, status, source, time1, time2, user_id)]
                cursor.executemany(sql_insert, insert_values)
                connect.commit()
                return JsonResponse({'code': 200, 'data': '新建成功'}, safe=False)
            else:
                return JsonResponse({'code': 500, 'data': '该关键词已存在'}, safe=False)

        except Exception as e:
            print(str(e))
