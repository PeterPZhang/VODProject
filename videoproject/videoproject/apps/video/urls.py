# -*- coding: utf-8 -*-
"""
__author__ = 'peter'
__mtime__ = '2019-03-27'
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

app_name = 'video'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchListView.as_view(), name='search'),
    # 表示详情信息，注意每条视频都是有自己的主键的，所以设置路径匹配为detail/<int:pk>/,其中<int:pk>表示主键，这是django中表示主键的一种方法。这样我们就可以在浏览器输入127.0.0.1:8000/video/detail/xxx来访问详情了。
    path('detail/<int:pk>/', views.VideoDetailView.as_view(), name='detail'),
]
