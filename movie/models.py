# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class Movie(models.Model):
    """
    电影的数据库表格
    """
    movie_name = models.CharField(max_length=64, blank=True)
    # 豆瓣链接,值可以是null,也可以不填这个字段.
    douban_link = models.CharField(max_length=256, null=True, blank=True)
    # 豆瓣评分.
    douban_score = models.CharField(max_length=64, null=True, blank=True)
    # 豆瓣评分人数.
    douban_counter = models.PositiveIntegerField(default=0, blank=True)
    # Imdb链接.
    imdb_link = models.CharField(max_length=256, null=True, blank=True)
    # Imdb评分.
    imdb_score = models.CharField(max_length=64, null=True, blank=True)
    # Imdb评分人数.
    imdb_counter = models.PositiveIntegerField(default=0, blank=True)
    # 网站中的链接.
    nomovie_link = models.CharField(max_length=256, null=True, blank=True)
    # 网站中评分.
    nomovie_score = models.CharField(max_length=64, null=True, blank=True)
    # 网站中评分人数.
    nomovie_counter = models.PositiveIntegerField(default=0, blank=True)
    # 上映国家.
    country = models.CharField(max_length=64, null=True, blank=True)
    # 上映日期.
    dateyear = models.CharField(max_length=64, null=True, blank=True)
    # 主演.
    actor = models.CharField(max_length=256, null=True, blank=True)
    # 导演.
    director = models.CharField(max_length=256, null=True, blank=True)
    # 电影类型.
    style = models.CharField(max_length=64, null=True, blank=True)
    # 电影播放地址.
    movie_address = models.CharField(max_length=256, null=True, blank=True)
    # 电影下载链接.
    download_link = models.CharField(max_length=256, null=True, blank=True)
    # 电影在本网站的播放次数.
    counter = models.PositiveIntegerField(default=0, blank=True)
    # 电影来源,
    # 0:表示豆瓣top250 1:表示imdbtop250 2:表示普通豆瓣 3：表示普通imdb  
    # 4:表示在豆瓣和imdb中都存在 5表示：用户自添加
    original = models.CharField(max_length=256, null=True, blank=True)
    # 1:表示通过 0:表示未通过 2:表示审核中
    status = models.IntegerField(null=True, blank=True)
    # 图片保存地址
    image = models.CharField(max_length=256, null=True, blank=True)
    # 爬取电影入库时间
    spidertime = models.DateTimeField(auto_now_add=True, null=True)
    # 关于电影
    aboutmovie = models.CharField(max_length=256, null=True, blank=True)
    # 电影语言
    language = models.CharField(max_length=64, null=True, blank=True)
    # 电影天堂搜索地址
    dyttsearch = models.CharField(max_length=256, null=True, blank=True)
    # 电影天堂搜索电影详情页面
    dyttdetail = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.movie_name

    # def get_comments(self):

class MovieHistory(models.Model):
    # 观看的用户.
    # 用户一对多MovieHistory,可以看多个电影.
    user = models.ForeignKey(User)
    # 观看的电影.
    movie = models.ForeignKey(Movie)
    # 观看的时间.
    date = models.DateTimeField(auto_now_add=True)
    # 0表示用户观看了该电影,1表示收藏,2表示推荐.
    marked = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return "{%s}--{%s}" % (self.user.username, self.movie.movie_name)


