import pymysql
import json
import datetime
from django.http import HttpResponse, JsonResponse

from db_config import db
# 后端接口:用户登录
def api_login(request):
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
            username = form["username"]
            password = form["password"]

            sql_search = f"select * from users where username = '{username}' and password = '{password}';"
            cursor.execute(sql_search)
            res = cursor.fetchall()
            if len(res) != 0:
                my_dict = {
                    "user_id": res[0][0],
                    "username": res[0][1],
                    "password": res[0][2],
                }
                return JsonResponse({"code": 200, "data": my_dict}, safe=False)
            else:
                return JsonResponse({"code": 210, "data": "用户名或密码错误"}, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 后端接口:用户注册
def api_register(request):
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
            username = form["username"]
            password = form["password"]

            # 查询数据库，若关键词已存在则不能重复插入
            sql_search = f"select * from users where username = '{username}';"
            cursor.execute(sql_search)
            res = cursor.fetchall()
            if len(res) == 0:
                sql_insert = "INSERT INTO users (username, password) VALUES (%s, %s);"
                insert_values = [(username, password)]
                cursor.executemany(sql_insert, insert_values)
                connect.commit()
                return JsonResponse({"code": 200, "data": "注册成功"}, safe=False)
            else:
                return JsonResponse({"code": 210, "data": "该用户名已占用"}, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接
