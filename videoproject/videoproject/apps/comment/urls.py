# -*- coding: utf-8 -*-
"""
__author__ = 'peter'
__mtime__ = '2019-04-12'
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

app_name = 'comment'
urlpatterns = [
    path('submit_comment/<int:pk>',views.submit_comment, name='submit_comment'),
    path('get_comments/', views.get_comments, name='get_comments'),
]