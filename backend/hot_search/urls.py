from django.urls import path

from hot_search import views

urlpatterns = [
    # 获取百度热搜榜前30
    path('get_baidu_hot_search/', views.api_get_baidu_hot_search, name='api_get_baidu_hot_search'),
    # 获取微博今日热搜第一
    path('get_weibo_day_data/', views.api_get_weibo_day_data, name='api_get_weibo_day_data'),
    # 获取微博本周热搜第一
    path('get_weibo_week_data/', views.api_get_weibo_week_data, name='api_get_weibo_week_data'),
    # 获取微博本周热搜第一
    path('get_weibo_month_data/', views.api_get_weibo_month_data, name='api_get_weibo_month_data'),
    # 获取近期热门事件24小时变化折线图数据
    path('get_chart_data/', views.api_get_chart_data, name='api_get_chart_data'),
    # 获取当前排行榜数据
    path('get_rank_data/', views.api_get_rank_data, name='api_get_rank_data'),
]
