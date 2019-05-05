# -*- coding: utf-8 -*-
"""
__author__ = 'peter'
__mtime__ = '2019-04-11'
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
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import *
from django.utils.html import strip_tags
from django.views.generic import View

from videoproject.settings.public import *


# @ajax_required验证request必须是ajax
def ajax_required(f):
    """Not a mixin, but a nice decorator to validate than a request is AJAX"""

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


class AuthorRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class SuperUserRequiredMixin(View):
    """
    超级用户拦截器
    """

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponse('无权限')

        return super().dispatch(request, *args, **kwargs)


class AdminUserRequiredMixin(View):
    """
    管理员拦截器
    """

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('myadmin:login')

        return super().dispatch(request, *args, **kwargs)


def send_html_email(subject, html_message, to_list):
    """
    发送网页邮件
    :param subject:
    :param html_message:
    :param to_list:
    :return:
    """
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, to_list, html_message=html_message)
