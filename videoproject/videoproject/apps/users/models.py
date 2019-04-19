from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    nickname = models.CharField(blank=True, null=True, max_length=20)
    avatar = models.FileField(upload_to='avatar/')  # 头像
    mobile = models.CharField(blank=True, null=True, max_length=13)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  # 性别
    subscribe = models.BooleanField(default=False)  # 是否订阅

    class Meta:
        db_table = "v_user"


class Feedback(models.Model):
    """
    反馈建议
    """
    contact = models.CharField(blank=True, null=True, max_length=20)  # 联系方式
    content = models.CharField(blank=True, null=True, max_length=200)  # 内容
    timestamp = models.DateTimeField(auto_now_add=True, null=True)  # 时间

    class Meta:
        db_table = "v_feedback"
