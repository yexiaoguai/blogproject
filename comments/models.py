# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    # 个人网站,允许为空
    url = models.URLField(blank=True)
    text = models.TextField()
    # 自动生成创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 评论对应一个文章,文章可以有多个评论,一对多的关系.
    post = models.ForeignKey("blog.Post")

    def __unicode__(self):
        return self.text[:20]





