# 开启定时任务，每5分钟调用一次 rep_main_save_data 方法，调用爬虫方法，更新数据库
from main_hot_search import rep_main_save_data
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == '__main__':
    try:
        scheduler = BlockingScheduler()
        # hours=1
        scheduler.add_job(rep_main_save_data, 'interval', args=(50, "weibo"), max_instances=100, minutes=10)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
