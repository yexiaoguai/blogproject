# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown

class Category(models.Model):
    """
    分类的数据库表格
    """
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Tag(models.Model):
    """
    标签的数据库表格
    """
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Post(models.Model):
    """
    文章的数据库表格
    """
    # 文章标题.
    title = models.CharField(max_length=70)
    # 文章正文,TextField大段文本.
    content = models.TextField()
    # 文章创建时间.
    create_time = models.DateTimeField()
    # 文章最后一次修改的时间.
    modified_time = models.DateTimeField()
    # 阅读数量,PositiveIntegerField正整数字段.
    views = models.PositiveIntegerField(default=0)
    # 文章摘要,可以为空.
    excerpt = models.CharField(max_length=200, blank=True)
    # 一篇文章只能对应一个分类,但是一个分类下可以有多篇文章,所以使用的是ForeignKey,即一对多的关联关系.
    # 而对于标签来说,一篇文章可以有多个标签,同一个标签下也可能有多篇文章,所以使用ManyToManyField,表明这是多对多的关联关系.
    # 同时规定文章可以没有标签,因此为标签tags指定了 blank=True.
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    # 文章作者,这里User是从django.contrib.auth.models导入的.
    # django.contrib.auth是Django内置的应用,专门用于处理网站用户的注册,登录等流程,User是Django为我们已经写好的用户模型.
    # 这里通过ForeignKey把文章和User关联了起来.
    # 因为规定一篇文章只能有一个作者,而一个作者可能会写多篇文章,因此这是一对多的关联关系,和Category类似.
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    # reverse函数会去解析detail视图函数对应的URL.
    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

    # 调用save方法将更改后的值保存到数据库.
    # 注意这里使用了update_fields参数来告诉Django只更新数据库中views字段的值,以提高效率.
    def increase_views(self):
        """
        view字段加1,可以在调取界面的时候调用该方法.
        用于计算阅读该文章的阅读数量.
        """
        self.views += 1
        self.save(update_fields=["views"])
    
    # 文章根据创作时间倒序进行排序.
    class Meta:
        ordering = ["-create_time"]