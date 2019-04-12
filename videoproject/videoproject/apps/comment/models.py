from django.db import models

from videoproject.settings import public
from django.db import models

from video.models import Video


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(public.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.CharField(max_length=100, blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "v_comment"
