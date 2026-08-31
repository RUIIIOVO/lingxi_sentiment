import pymysql
import json
import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, JsonResponse

from db_config import db
# 后端接口:用户登录
# 密码以 PBKDF2 哈希存储，建表时 users.password 需至少 VARCHAR(128)
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

            # 密码已哈希，无法在 SQL 里比对，先按用户名取出再验证
            sql_search = "select * from users where username = %s;"
            cursor.execute(sql_search, (username,))
            res = cursor.fetchall()
            if res and check_password(password, res[0][2]):
                my_dict = {
                    "user_id": res[0][0],
                    "username": res[0][1],
                }
                return JsonResponse({"code": 200, "data": my_dict}, safe=False)
            else:
                return JsonResponse({"code": 210, "data": "用户名或密码错误"}, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
            return JsonResponse({"code": 500, "data": "服务器内部错误"}, status=500, safe=False)
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
            sql_search = "select * from users where username = %s;"
            cursor.execute(sql_search, (username,))
            res = cursor.fetchall()
            if len(res) == 0:
                sql_insert = "INSERT INTO users (username, password) VALUES (%s, %s);"
                cursor.execute(sql_insert, (username, make_password(password)))
                connect.commit()
                return JsonResponse({"code": 200, "data": "注册成功"}, safe=False)
            else:
                return JsonResponse({"code": 210, "data": "该用户名已占用"}, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
            return JsonResponse({"code": 500, "data": "服务器内部错误"}, status=500, safe=False)
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接
