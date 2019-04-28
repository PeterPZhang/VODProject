# -*- coding: utf-8 -*-
"""
__author__ = 'peter'
__mtime__ = '2019-04-28'
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

app_name = 'myadmin'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # ----------------------视频管理------------------------
    path('video_add/', views.AddVideoView.as_view(), name='video_add'),  # 展示上传视频页面
    path('chunked_upload/', views.MyChunkedUploadView.as_view(), name='api_chunked_upload'),  # 视频上传
    path('chunked_upload_complete/', views.MyChunkedUploadCompleteView.as_view(),
         name='api_chunked_upload_complete'),  # 上传完毕回调页面
    path('video_publish/<int:pk>/', views.VideoPublishView.as_view(), name='video_publish'),  # 发布视频
    path('video_publish_success/', views.VideoPublishSuccessView.as_view(), name='video_publish_success'),  # 视频发布成功
    path('video_list/', views.VideoListView.as_view(), name='video_list'),  # 视频列表

]
