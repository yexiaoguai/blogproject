# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import urllib

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