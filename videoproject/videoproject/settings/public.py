# -*- coding: utf-8 -*-
"""
__author__ = 'peter'
__mtime__ = '2019-03-28'
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
AUTH_USER_MODEL = 'users.User'
SITE_URL = 'your website'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# 邮件配置
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'peterpz0428@163.com'  # 邮箱名称
EMAIL_HOST_PASSWORD = 'your pwd'  # 邮箱密码
