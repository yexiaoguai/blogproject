# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import markdown

class Tag(models.Model):
    """
    问题的标签.
    """
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __unicode__(self):
        return self.name

class Question(models.Model):
    """
    问题的数据库表格.
    """
    # 问题只能有一个user,一对多的情况.
    user = models.ForeignKey(User)
    tag = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    # 关注数
    favorites = models.IntegerField(default=0)
    # 问题答案是否被采纳
    has_accepted_answer = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        # 排序按照更新时间
        ordering = ("-update_date",)
    
    def __unicode__(self):
        return self.title

    def get_description_preview(self):
        if len(self.description) > 255:
            return u"{0}......".format(self.description[:255])
        else:
            return self.description
            
    def get_description_preview_as_markdown(self):
        """
        返回问题的描述,如果是markdown格式的也可以正常显示.
        """
        return markdown.markdown(self.get_description_preview(), safe_mode="escape")

    @staticmethod
    def get_unanswered():
        """
        返回未采纳的问题列表.
        """
        return Question.objects.filter(has_accepted_answer=False)

    @staticmethod
    def get_answered():
        """
        返回采纳的问题列表.
        """
        return Question.objects.filter(has_accepted_answer=True)
