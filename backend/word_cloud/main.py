# linux中无法读取上一级目录时在import前添加
import sys
import os

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

import pymysql
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random
from db_config import db


# 存入数据库主体函数
def generate_word_cloud():
    # 连接数据库
    connect = pymysql.connect(
        host=db["host"],
        port=db["port"],  # 端口号
        user=db["user"],  # 数据库用户
        password=db["password"],  # 数据库密码
        database=db["database"]  # 要连接的数据库名称
    )
    cursor = connect.cursor()
    try:
        sql = "select title from weibo_hot_search_rank;"
        cursor.execute(sql)
        res = cursor.fetchall()
        connect.commit()
        text = str(res)
        jieba.setLogLevel(jieba.logging.INFO)
        seg_list = jieba.lcut(text, cut_all=False)
        print(seg_list)
        # 过滤无用词
        stop_words = [
            "我", "自己", "的", "了", "和", "是", "就", "都", "而", "及", "与", "以",
            "在", "了", "着", "是", "就", "都", "而", "及", "于", "著",
            "把", "一个", "一个", "这", "这", "那", "哪", "个", "等", "等等"
        ]
        seg_list_filtered = [word for word in seg_list if word not in stop_words]
        seg_list_join = " ".join(seg_list_filtered)
        # 服务器中没有中文字体，需要下载上传至服务器
        # wordcloud = WordCloud(font_path="/usr/share/fonts/dejavu/simsun.ttf", background_color="#212121", width=620, height=400).generate(
        #     seg_list_join)
        wordcloud = WordCloud(font_path="simsun.ttc", background_color="#212121", width=620, height=400).generate(
            seg_list_join)

        # 定义颜色函数来随机选择颜色
        def random_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            colors = ["#004578", "#005a9e", "#106ebe", "#0078d4", "#2b88d8", "#71afe5"]
            return random.choice(colors)

        # 重新着色
        wordcloud = wordcloud.recolor(color_func=random_color_func)
        # 保存词云图片
        wordcloud.to_file('D:/Asentiment/shows/src/assets/img/word_cloud.png')
        # wordcloud.to_file('/www/lingxi/control/static/img/word_cloud.d5ccd1b1.png')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        # plt.show()
    except Exception as e:
        print("错误:", str(e))
    finally:
        cursor.close()  # 关闭游标
        connect.close()  # 关闭数据库连接


if __name__ == '__main__':
    generate_word_cloud()
