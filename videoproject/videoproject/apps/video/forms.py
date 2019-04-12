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
from django import forms
from comment.models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(error_messages={'required': '不能为空', },
                              widget=forms.Textarea(attrs={'placeholder': '请输入评论内容'})
                              )

    class Meta:
        model = Comment
        fields = ['content']
