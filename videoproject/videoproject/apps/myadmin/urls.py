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
    path('video_edit/<int:pk>/', views.VideoEditView.as_view(), name='video_edit'),  # 编辑视频
    path('video_delete/', views.video_delete, name='video_delete'),  # 删除视频

    # ----------------------分类管理----------------------------
    path('classification_add/', views.ClassificationAddView.as_view(), name='classification_add'),  # 增加视频分类
    path('classification_list/', views.ClassificationListView.as_view(), name='classification_list'),  # 视频分类列表
    path('classification_edit/<int:pk>/', views.ClassificationEditView.as_view(), name='classification_edit'),  # 编辑视频分类
    path('classification_delete/', views.classification_delete, name='classification_delete'),  # 删除视频分类

    # ----------------------评论管理----------------------------
    path('comment_list/', views.CommentListView.as_view(), name='comment_list'),  # 评论列表
    path('comment_delete/', views.comment_delete, name='comment_delete'),  # 删除评论

    # ----------------------用户管理-------------------------
    path('user_add/', views.UserAddView.as_view(), name='user_add'),  # 添加用户
    path('user_list/', views.UserListView.as_view(), name='user_list'),  # 用户列表
    path('user_edit/<int:pk>', views.UserEditView.as_view(), name='user_edit'),  # 用户编辑
    path('user_delete/', views.user_delete, name='user_delete'),  # 删除用户

    # -----------------------订阅通知---------------------------
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),  # 视频订阅

    # -----------------------用户反馈-------------------------
    path('feedback_list/', views.FeedbackListView.as_view(), name='feedback_list'),  # 反馈列表
    path('feedback_delete/', views.feedback_delete, name='feedback_delete'),  # 删除反馈信息
]
