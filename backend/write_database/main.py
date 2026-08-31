# linux中无法读取上一级目录时在import前添加
import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

import pymysql
from db_config import db
from write_database.update_rank import update_rank
from write_database.update_weibo import save_data_weibo
from word_cloud.main import generate_word_cloud

# 4.监测任务查询keyword是否存在在排名表的title中
def search_keyword_in_sources(keyword, sources, cursor):
    results = {}
    for source in sources:
        # 此时我们已经假设 source 是一个没有任何非法字符的有效表名
        table_name = f"{source}_hot_search_rank"  # 删除了 lower() 调用，因为表名应该在之前正确设置
        sql_search_keyword = f"SELECT title, `rank`, hot_value, url FROM `{table_name}` WHERE title LIKE %s;"  # `table_name` 已经得到了保证是合法的
        keyword_pattern = f"%{keyword}%"
        cursor.execute(sql_search_keyword, (keyword_pattern,))
        matched_records = cursor.fetchall()
        results[source] = matched_records
    return results


# 监测任务主体
def main_monitor():
    # 1.更新排名表
    update_rank()
    # 连接数据库
    connect = pymysql.connect(
        host=db["host"],
        port=db["port"],  # 端口号
        user=db["user"],  # 数据库用户
        password=db["password"],  # 数据库密码
        database=db["database"]  # 要连接的数据库名称
    )
    cursor = connect.cursor()
    # 2.更新status，失效的监测更改为已结束
    sql_update_status = "UPDATE monitor SET status = 0 WHERE status = 1 AND end_time < CURRENT_TIMESTAMP;"
    cursor.execute(sql_update_status)
    connect.commit()
    # 3.获取有效的所有任务
    sql_get_monitor = "SELECT `keyword`,`source`,`start_time`,`end_time`,`user_id` FROM monitor WHERE status = 1 AND start_time < CURRENT_TIMESTAMP AND end_time > CURRENT_TIMESTAMP;"
    cursor.execute(sql_get_monitor)
    monitors = cursor.fetchall()
    connect.commit()

    for monitor in monitors:
        keyword, source_str, start_time, end_time, user_id = monitor
        sources = source_str.split(' ')

        source_mapping = {
            '新浪微博': 'weibo',
            '百度': 'baidu',
            '抖音': 'douyin',
            '今日头条': 'toutiao',
            '知乎': 'zhihu',
            '微信': 'weixin'
        }

        mapped_sources = [source_mapping[source] for source in sources]
        keyword_search_results = search_keyword_in_sources(keyword, mapped_sources, cursor)
        for source, results in keyword_search_results.items():
            if results:
                for result in results:
                    title, rank, hot_value, url = result
                    # 将source从字典中映射回原始形式
                    source_name = next(key for key, value in source_mapping.items() if value == source)
                    # 5.防止重复插入
                    sql_select = "select * from alarm_msg where `keyword` = %s and `content` = %s and `user_id` = %s"
                    cursor.execute(sql_select, (keyword, title, user_id))
                    res = cursor.fetchall()
                    connect.commit()
                    if len(res) == 0:
                        # 6.插入alarm_msg
                        sql_insert = "INSERT INTO alarm_msg(`keyword`, `content`, `source`,`user_id`) VALUES (%s, %s, %s, %s)"
                        insert_values = [(keyword, title, source_name, user_id)]
                        cursor.executemany(sql_insert, insert_values)
                        connect.commit()
                        print(insert_values)


from paddlenlp import Taskflow


# 7.对alarm_msg做情感分析
def emotion():
    connect = pymysql.connect(
        host=db["host"],
        port=db["port"],  # 端口号
        user=db["user"],  # 数据库用户
        password=db["password"],  # 数据库密码
        database=db["database"]  # 要连接的数据库名称
    )
    cursor = connect.cursor()
    sql_select = "select `id`,`content` from alarm_msg where emotion is null;"
    cursor.execute(sql_select)
    result = cursor.fetchall()
    connect.commit()
    for res in result:
        print(res[1])
        senta = Taskflow("sentiment_analysis")
        item = senta(res[1])
        if item[0]["label"] == "positive":
            emotion = '积极'
        else:
            emotion = '消极'
        print(emotion)
        sql_update = f"update alarm_msg set `emotion` = '{emotion}' where `id` = '{res[0]}'"
        cursor.execute(sql_update)
        connect.commit()


from apscheduler.schedulers.blocking import BlockingScheduler


# 定时任务：
def scheduler(): 
    try:
        scheduler = BlockingScheduler()
        # scheduler.add_job(main_monitor, 'interval', max_instances=1, minutes=1)
        scheduler.add_job(main_monitor, 'interval', max_instances=1, seconds=30)
        scheduler.add_job(emotion, 'interval', max_instances=1, minutes=1)
        scheduler.add_job(generate_word_cloud, 'interval', max_instances=1, minutes=1)
        scheduler.add_job(save_data_weibo, 'interval', max_instances=1, minutes=20)
        # scheduler.add_job(save_data_weibo, 'interval', max_instances=1, hours=1)
        # scheduler.add_job(save_data_weibo, 'interval', max_instances=1, minutes=1)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    # main_monitor()
    # emotion()
    scheduler()
