from django.urls import path, include
from user import views

urlpatterns = [
    # 注册
    path('api_register/', views.api_register, name='api_register'),
    # 登录
    path('api_login/', views.api_login, name='api_login'),

]
