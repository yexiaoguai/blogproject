# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings as django_settings

from questions.models import Notification

import urllib, os

class Webuser(models.Model):
    """
    该数据库表格保存了用户个人的信息以及是否在线等数据
    """
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    likesstyle = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    registerday = models.DateTimeField(auto_now=True, blank=True)
    sex = models.IntegerField(default=1)
    friends = models.ManyToManyField("self")
    online = models.IntegerField(default=False)

    def __unicode__(self):
        return self.user.username

    def get_picture(self):
        """
        获取到该用户的头像
        """
        # 默认头像
        no_picture = django_settings.MEDIA_URL+"webuser_pictures/user.png"
        try:
            # 获取到头像的路径以及文件名
            filename = django_settings.MEDIA_ROOT+"/webuser_pictures/"+self.user.username+".jpg"
            # 获取到头像的url
            picture_url = django_settings.MEDIA_URL+"webuser_pictures/"+self.user.username+".jpg"
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture
        except Exception as e:
            return no_picture

    def notify_answered(self, question):
        """
        """
        if self.user != question.user:
            Notification(
                notification_type=Notification.ANSWERED,
                from_user=self.user,
                to_user=question.user,
                question=question
            ).save()
