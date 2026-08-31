import pymysql
from django.http import JsonResponse
from datetime import datetime, timedelta
from db_config import db


# 后端接口：查询事件库
def api_search_events(request):
    if request.method == 'POST':
        connect = pymysql.connect(
            host=db["host"],
            port=db["port"],  # 端口号
            user=db["user"],  # 数据库用户
            password=db["password"],  # 数据库密码
            database=db["database"],  # 要连接的数据库名称
            cursorclass=pymysql.cursors.DictCursor  # 使用字典游标
        )
        cursor = connect.cursor()
        try:
            search_form = request.POST
            print(search_form)
            # 构建基本的 SQL 查询语句
            sql = "SELECT * FROM events"
            sql_count = "SELECT COUNT(*) as total_count FROM events"  # 计数查询
            # 根据前端传入的查询条件构建相应的 SQL 查询语句
            conditions = []
            parameters = []

            if 'database_choose' in search_form:
                database_choose = search_form['database_choose'][0]
                if database_choose == '1':
                    sql = "SELECT * FROM own_events"
                    sql_count = "SELECT COUNT(*) as total_count FROM own_events"  # 计数查询

            if 'search_value' in search_form:
                search_value = search_form['search_value']
                print(search_value)
                if search_value:  # 检查搜索值是否非空
                    search_value = search_value  # 获取第一个搜索值
                    conditions.append("title LIKE %s")  # 假设你想在标题中进行模糊搜索
                    parameters.append(f"%{search_value}%")

            # if 'time_value[]' in search_form:
            #     time_values = search_form.getlist('time_value[]')
            #     if len(time_values) == 2:
            #         start_date = time_values[0].split('T')[0]  # 获取开始日期，忽略时、分、秒
            #         end_date = time_values[1].split('T')[0]  # 获取结束日期，忽略时、分、秒
            #         print(time_values[0],time_values[1],start_date, end_date)
            #         conditions.append("(DATE(datetime) BETWEEN %s AND %s)")  # 使用DATE()函数比较日期部分
            #         parameters.extend([start_date, end_date])

            import pytz  # 导入pytz模块处理时区
            if 'time_value[]' in search_form:
                time_values = search_form.getlist('time_value[]')
                if len(time_values) == 2:
                    # 中国时区
                    china_tz = pytz.timezone('Asia/Shanghai')

                    # 去除时间字符串末尾的 'Z' 并转换为 datetime 对象
                    start_datetime = datetime.strptime(time_values[0][:-1], '%Y-%m-%dT%H:%M:%S.%f')
                    end_datetime = datetime.strptime(time_values[1][:-1], '%Y-%m-%dT%H:%M:%S.%f')

                    # 将时间转换为中国时区
                    start_datetime = start_datetime.replace(tzinfo=pytz.utc).astimezone(china_tz)
                    end_datetime = end_datetime.replace(tzinfo=pytz.utc).astimezone(china_tz)

                    start_date = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    end_date = end_datetime.strftime('%Y-%m-%d %H:%M:%S')

                    # print(start_datetime, end_datetime, start_date, end_date)

                    conditions.append("(datetime BETWEEN %s AND %s)")
                    parameters.extend([start_date, end_date])

            if 'check_all' in search_form:
                check_all = search_form.getlist('check_all')
                isIndeterminate = search_form.getlist('isIndeterminate')
                checked_tags = search_form.getlist('checked_tags[]')
                if check_all[0] == 'false' and isIndeterminate[0] == 'false':
                    return JsonResponse({'code': 200, 'data': [], 'total_count': 0}, safe=False)
                elif check_all[0] == 'true':
                    # 标签全选则不作筛选
                    pass
                elif checked_tags:
                    tag_conditions = " OR ".join(["tag=%s"] * len(checked_tags))
                    conditions.append(f"({tag_conditions})")
                    parameters.extend(checked_tags)

            # if 'checked_tags[]' in search_form:
            #     checked_tags = search_form.getlist('checked_tags[]')
            #     if checked_tags:
            #         tag_conditions = " OR ".join(["tag=%s"] * len(checked_tags))
            #         conditions.append(f"({tag_conditions})")
            #         parameters.extend(checked_tags)

            # 执行查询
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            if conditions:
                sql_count += " WHERE " + " AND ".join(conditions)

            if 'sort_value' in search_form:
                sort_value = search_form['sort_value']
                if sort_value == 'hot_down':
                    sql += " ORDER BY hot_value DESC"
                elif sort_value == 'hot_up':
                    sql += " ORDER BY hot_value ASC"
                elif sort_value == 'time_down':
                    sql += " ORDER BY datetime DESC"
                elif sort_value == 'time_up':
                    sql += " ORDER BY datetime ASC"

            # 分页功能
            if 'pageSize' in search_form and 'current' in search_form:
                page_size = int(search_form['pageSize'])
                current_page = int(search_form['current'])
                offset = (current_page - 1) * page_size
                sql += f" LIMIT {offset}, {page_size}"

            # 计算符合条件的总行数
            count_parameters = parameters[:]  # 复制参数列表

            cursor.execute(sql_count, count_parameters)
            total_count_result = cursor.fetchone()
            total_count = total_count_result['total_count'] if total_count_result else 0

            cursor.execute(sql, parameters)
            # 获取查询结果
            results = cursor.fetchall()
            events = []
            for result in results:
                event = {
                    'title': result['title'],
                    'text': result['text'],
                    'tags': result['tag'].split(','),  # 假设标签以逗号分隔存储在数据库中
                    'hot_value': result['hot_value'],
                    'time': result['datetime'].strftime('%Y-%m-%d')  # 格式化时间
                }
                events.append(event)
            return JsonResponse({'code': 200, 'data': events, 'total_count': total_count}, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 后端接口:获取事件库细节
def api_get_events_detail(request):
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
            title = request.GET.get('title')
            sql = f"SELECT title, tag, hot_value, datetime, location, source, media, text FROM events WHERE title = '{title}'"
            cursor.execute(sql)
            res = cursor.fetchone()  # 使用fetchone()获取单条结果
            if res:
                event_detail = {
                    'title': res[0],
                    'tags': res[1].split(', '),  # 假设tags字段以逗号分隔
                    'hot_value': res[2],
                    'time': res[3].strftime('%Y-%m-%d'),  # 格式化时间
                    'location': res[4],
                    'source': res[5],
                    'media': res[6],
                    'text': res[7],
                }
                return JsonResponse(event_detail, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 后端接口：获取指定事件24小时热度值变化折线图数据
def api_get_hot_values_trend(request):
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
            title = request.GET.get('title')
            range_value = int(request.GET.get('range_value', 1))
            data_count = 99999
            if range_value == 1:
                # 当range_value为1时返回全部数据
                sql = f"""
                            SELECT *
                            FROM weibo_hot_search_values 
                            WHERE title = '{title}'
                            ORDER BY datetime ASC;
                        """
            elif range_value == 12:
                time_range = timedelta(hours=12)
                data_count = 12
                end_time = datetime.now()
                start_time = end_time - time_range

                sql = f"""
                        SELECT *
                        FROM weibo_hot_search_values 
                        WHERE title = '{title}' AND datetime BETWEEN '{start_time}' AND '{end_time}'
                        ORDER BY datetime ASC;
                    """
            elif range_value == 24:
                time_range = timedelta(hours=24)
                data_count = 24
                end_time = datetime.now()
                start_time = end_time - time_range

                sql = f"""
                        SELECT *
                        FROM weibo_hot_search_values 
                        WHERE title = '{title}' AND datetime BETWEEN '{start_time}' AND '{end_time}'
                        ORDER BY datetime ASC;
                    """
            else:
                raise ValueError("输入错误")

            cursor.execute(sql)
            res = cursor.fetchall()
            # 在数据库中获取数据并转为json
            initial_data = []

            for r in res:
                my_dict = {}
                for i, key in enumerate(
                        ["title", "datetime", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11",
                         "t12",
                         "t13", "t14", "t15", "t16", "t17", "t18", "t19", "t20", "t21", "t22", "t23"]):
                    if r[i + 1] is None:
                        my_dict[key] = 0
                    else:
                        my_dict[key] = r[i + 1]
                initial_data.append(my_dict)

            # 将排序好的数据转化为前端折线图需要的数据格式
            final_data = []
            for data in initial_data:
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
                    if len(final_data) >= data_count and range_value != 1:  # 限制数据数量
                        break

            connect.commit()
            return JsonResponse(final_data, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 后端接口：获取事件评论情感分析
def api_get_review_emotion(request):
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
            title = request.GET.get('title')
            sql = f"select title,positive,passive from emotions where title = '{title}';"
            cursor.execute(sql)
            res = cursor.fetchone()
            if res:  # 检查是否有结果
                # 将结果转换为字典格式
                response_data = {
                    'total': int(res[1]) + int(res[2]),
                    'positive': int(res[1]),
                    'passive': int(res[2])
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'No data found for the given title'})
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 后端接口：事件脉络
def api_get_timeline(request):
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
            title = request.GET.get('title')
            print(title)
            sql = f"SELECT title, comment, happen_time FROM timeline WHERE title = '{title}' ORDER BY happen_time DESC;"
            print(sql)
            cursor.execute(sql)
            res = cursor.fetchall()

            print(res)
            return JsonResponse(res, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# ip地址统计
def api_get_people_ip(request):
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
            title = request.GET.get('title')
            sql = f"SELECT ip, COUNT(*) AS count FROM people WHERE title = '{title}' GROUP BY ip ORDER BY count DESC;"
            cursor.execute(sql)
            ip_counts = cursor.fetchall()
            ip_data = [{"name": ip[0], "value": ip[1]} for ip in ip_counts]
            return JsonResponse(ip_data, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 年龄统计
def execute_age_query(cursor, condition, title):
    sql = f"SELECT COUNT(*) FROM people WHERE age {condition} AND title = '{title}';"
    cursor.execute(sql)
    return cursor.fetchone()[0]


def api_get_people_age(request):
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
            title = request.GET.get('title')
            # age_distribution = {
            #     '≤19': execute_age_query(cursor, "<= 19", title),
            #     '20~29': execute_age_query(cursor, "BETWEEN 20 AND 29", title),
            #     '30~39': execute_age_query(cursor, "BETWEEN 30 AND 39", title),
            #     '40~49': execute_age_query(cursor, "BETWEEN 40 AND 49", title),
            #     '≥50': execute_age_query(cursor, ">= 50", title),
            # }
            age_distribution = [
                execute_age_query(cursor, "<= 19", title),
                execute_age_query(cursor, "BETWEEN 20 AND 29", title),
                execute_age_query(cursor, "BETWEEN 30 AND 39", title),
                execute_age_query(cursor, "BETWEEN 40 AND 49", title),
                execute_age_query(cursor, ">= 50", title),
            ]
            return JsonResponse(age_distribution, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接


# 性别统计
def api_get_people_sex(request):
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
            title = request.GET.get('title')
            sql = f"SELECT sex, COUNT(*) AS count FROM people WHERE title = '{title}' GROUP BY sex;"
            cursor.execute(sql)
            gender_counts = cursor.fetchall()
            gender_data = [{"value": gender[1], "name": gender[0]} for gender in gender_counts]
            return JsonResponse(gender_data, safe=False)
        except Exception as e:
            print("连接数据库出错:", str(e))
        finally:
            cursor.close()  # 关闭游标
            connect.close()  # 关闭数据库连接
