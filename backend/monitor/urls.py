from django.urls import path, include
from monitor import views

urlpatterns = [
    # 获取所有预警设置
    path('api_get_total_monitor/', views.api_get_total_monitor, name='api_get_total_monitor'),
    # 获取详情中的历史告警
    path('api_get_one_alarm_msg/', views.api_get_one_alarm_msg, name='api_get_one_alarm_msg'),
    # 删除预警
    path('api_delete_monitor/', views.api_delete_monitor, name='api_delete_monitor'),
    # 新增预警
    path('api_add_monitor/', views.api_add_monitor, name='api_add_monitor'),


]
