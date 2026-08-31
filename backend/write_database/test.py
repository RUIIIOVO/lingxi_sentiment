import pymysql
from db_config import db

connect = pymysql.connect(
        host=db["host"],
        port=db["port"],  # 端口号
        user=db["user"],  # 数据库用户
        password=db["password"],  # 数据库密码
        database=db["database"]  # 要连接的数据库名称
    )
cursor = connect.cursor()
try:
    sql = "select text from events where id = '67';"
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)
    with open('result.txt', 'w', encoding='utf-8') as file:
        for row in res:
            file.write(row[0] + '\n')
    connect.commit()
except Exception as e:
    print("存入数据库出错:", str(e))
finally:
    cursor.close()  # 关闭游标
    connect.close()  # 关闭数据库连接