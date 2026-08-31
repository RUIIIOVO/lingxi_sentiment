from django.urls import path, include
from database import views

urlpatterns = [
    # 查询事件库
    path('api_search_events/', views.api_search_events, name='api_search_events'),
    # 获取事件详情
    path('api_get_events_detail/', views.api_get_events_detail, name='api_get_events_detail'),
    # 获取指定事件24小时热度值变化折线图数据
    path('api_get_hot_values_trend/', views.api_get_hot_values_trend, name='api_get_hot_values_trend'),
    # 获取指定事件24小时热度值变化折线图数据
    path('api_get_review_emotion/', views.api_get_review_emotion, name='api_get_review_emotion'),
    # 获取事件脉络
    path('api_get_timeline/', views.api_get_timeline, name='api_get_timeline'),
    # ip地址统计
    path('api_get_people_ip/', views.api_get_people_ip, name='api_get_people_ip'),
    # 年龄统计
    path('api_get_people_age/', views.api_get_people_age, name='api_get_people_age'),
    # 性别统计
    path('api_get_people_sex/', views.api_get_people_sex, name='api_get_people_sex'),
    #


]
