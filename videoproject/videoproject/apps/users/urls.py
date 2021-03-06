# -*- coding: utf-8 -*-
"""
__author__ = 'peter'
__mtime__ = '2019-03-26'
# Follow the master,become a master.
             ┏┓       ┏┓
            ┏┛┻━━━━━━━┛┻┓
            ┃    ☃      ┃
            ┃  ┳┛   ┗┳  ┃
            ┃     ┻     ┃
            ┗━┓       ┏━┛
              ┃       ┗━━━━┓
              ┃ 神兽保佑     ┣┓
              ┃　永无BUG！   ┏┛
              ┗┓┓┏━━━┳┓┏━━━┛
               ┃┫┫   ┃┫┫
               ┗┻┛   ┗┻┛
"""
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),  # 更新个人中心
    path('change_password/', views.change_password, name='change_password'),  # 更改密码
    path('subscribe/<int:pk>/', views.SubscribeView.as_view(), name='subscribe'),  # 订阅设置功能
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),  # 反馈建议
    path('<int:pk>/collect_videos/', views.CollectListView.as_view(), name='collect_videos'),  # 我的收藏
    path('<int:pk>/like_videos/', views.LikeListView.as_view(), name='like_videos'),  # 我的喜欢
]
