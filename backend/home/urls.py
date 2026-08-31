from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    # 告警信息
    path('api_get_alarm_msg/', views.api_get_alarm_msg, name='api_get_alarm_msg'),
    # 当前微博热搜排行榜
    path('api_get_hot_search/', views.api_get_hot_search, name='api_get_hot_search'),
    # 事件库事件来源平台
    path('api_get_events_source/', views.api_get_events_source, name='api_get_events_source'),
    # 情感分析
    path('api_get_events_emotion/', views.api_get_events_emotion, name='api_get_events_emotion'),
    # 事件标签分类
    path('api_get_events_kinds/', views.api_get_events_kinds, name='api_get_events_kinds'),
    # 事件发生地点
    path('api_get_events_location/', views.api_get_events_location, name='api_get_events_location'),
    # 各地媒体数量
    path('api_get_medias_location/', views.api_get_medias_location, name='api_get_medias_location'),
    # 获取近期舆情数量变化
    path('api_get_events_time/', views.api_get_events_time, name='api_get_events_time'),
    # 更新词云
    path('api_update_word_cloud/', views.api_update_word_cloud, name='api_update_word_cloud'),
]
