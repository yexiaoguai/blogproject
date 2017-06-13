# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.models import User

from models import Movie, MovieHistory

# 获得推荐电影列表和默认
def get_movie_list(request):
    type = "suggest"
    after_range_num = 5
    before_range_num = 4
    # 获取用户请求页的页码,例如:?page=12.
    page = request.GET.get("page")
    if page is None:
        page = 1
    filtertype = request.GET.get("filtertype")
    filterparam = request.GET.get("filterparam")
    # 过滤条件为有播放地址,豆瓣分数大于7.5,豆瓣评分人数大于2000人的电影.
    # __gte大于的含义
    moviequery = Movie.objects.filter(movie_address__isnull=False, douban_score__gte=7.5,
                                      douban_counter__gte=2000)
    # 通过验证
    if request.user.is_authenticated():
        # 排除条件为:电影id为,观看过的电影id
        moviequery = moviequery.exclude(id__in=MovieHistory.objects.filter(user=request.user).values_list("movie_id", flat=True))
        movie_list = moviequery
        # 如果用户选择了style,在电影队列中进行过滤style的字段
        if filtertype == "style":
            movie_list = moviequery.filter(style__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "area":
            movie_list = moviequery.filter(country__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "year":
            # 过滤上映日期
            if filterparam == "20":
                movie_list = moviequery.filter(dateyear__lte="2001-12-20").order_by("-douban_score", "-douban_counter")
            else:
                movie_list = moviequery.filter(dateyear__contains=filterparam).order_by("-douban_score", "-douban_counter")
    else:
        movie_list = moviequery
        if filtertype == "style":
            movie_list = moviequery.filter(style__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "area":
            movie_list = moviequery.filter(country__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "year":
            # 过滤上映日期
            if filterparam == "20":
                movie_list = moviequery.filter(dateyear__lte="2001-12-20").order_by("-douban_score", "-douban_counter")
            else:
                movie_list = moviequery.filter(dateyear__contains=filterparam).order_by("-douban_score", "-douban_counter")
    random_num = random.randint(0, 99)
    imdbmovie_list = Movie.objects.order_by("douban_score")[random_num:random_num+6]
    usamovie_list = Movie.objects.filter(country__contains="美").order_by("douban_score")[random_num:random_num+6]
    # 进行分页,每页12个Movie实例
    paginator = Paginator(movie_list, 12)
    try:
        movie_list = paginator.page(page)
    # 页面号码是无效的还是超过最大页码的情况,默认都是第一页.
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        movie_list = paginator.page(1)
    # 
    #if page >= after_range_num:
        # 获取到整个分页页码列表,比如分了4页,那么就是[1,2,3,4].
    #    page_range = paginator.page_range[page-after_range_num:page+before_range_num]
    #else:
    #    page_range = paginator.page_range[0:int(page)+before_range_num]
    #  locals()返回一个包含当前作用域里面的所有变量和它们的值的字典.
    return render(request, "movie/allfilms.html", locals())

        
    
    






    

