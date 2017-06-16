# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView

from models import Movie, MovieHistory

movie_area = ["阿根廷","巴西","澳大利亚","西班牙",]

def get_movie_list(request):
    """
    获得推荐电影列表和默认电影列表
    """
    # 为了区别网页上用户选择的选项块.
    action = "getmovielist"
    type = "suggest"
    after_range_num = 5
    before_range_num = 4
    # 获取用户请求页的页码,例如:?page=12.
    page = request.GET.get("page")
    if page is not None:
        page = int(page)
    else:
        page = 1
    filtertype = request.GET.get("filtertype")
    filterparam = request.GET.get("filterparam")
    # 过滤条件为有播放地址,豆瓣分数大于7.5,豆瓣评分人数大于2000人的电影.
    # __gte大于的含义
    moviequery = Movie.objects.filter(movie_address__isnull=False, 
                                      douban_score__gte=7.5,
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
            if filterparam == "其它":
                movie_list = moviequery.filter(country__in=movie_area).order_by("-douban_score", "-douban_counter")
            else:
                movie_list = moviequery.filter(country__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "year":
            # 过滤上映日期
            if filterparam == "20":
                movie_list = moviequery.filter(dateyear__lte="2002-12-30").order_by("-douban_score", "-douban_counter")
            else:
                movie_list = moviequery.filter(dateyear__contains=filterparam).order_by("-douban_score", "-douban_counter")
    else:
        movie_list = moviequery
        if filtertype == "style":
            movie_list = moviequery.filter(style__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "area":
            if filterparam == "其它":
                movie_list = moviequery.filter(country__in=movie_area).order_by("-douban_score", "-douban_counter")
            else:
                movie_list = moviequery.filter(country__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "year":
            # 过滤上映日期
            if filterparam == "20":
                movie_list = moviequery.filter(dateyear__lte="2002-12-30").order_by("-douban_score", "-douban_counter")
            else:
                movie_list = moviequery.filter(dateyear__contains=filterparam).order_by("-douban_score", "-douban_counter")
    random_num = random.randint(0, 99)
    imdbmovie_list = Movie.objects.order_by("douban_score")[random_num:random_num+6]
    usamovie_list = Movie.objects.filter(country__contains="美").order_by("douban_score")[random_num:random_num+6]
    # 进行分页,每页12个Movie实例
    paginator = Paginator(movie_list, 12)
    try:
        movielist = paginator.page(page)
    # 页面号码是无效的还是超过最大页码的情况,默认都是第一页.
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        movielist = paginator.page(1)

    page_range = []
    for p in paginator.page_range:
            page_range.append(p)
    if page >= after_range_num:
        # 获取到整个分页页码列表,比如分了4页,那么就是[1,2,3,4].
        page_range = page_range[page-after_range_num:page+before_range_num]
    else:
        page_range = page_range[0:page+before_range_num]
    #  locals()返回一个包含当前作用域里面的所有变量和它们的值的字典.
    return render(request, "movie/allfilms.html", locals())

def get_latest_movielist(request):
    """
    获取最新的电影列表
    """
    # 为了区别网页上用户选择的选项块.
    action = "getmovielist"
    type = "latest"
    after_range_num = 5
    before_range_num = 4
    # 获取用户请求页的页码,例如:?page=12.
    page = request.GET.get("page")
    if page is not None:
        page = int(page)
    else:
        page = 1
    filtertype = request.GET.get("filtertype")
    filterparam = request.GET.get("filterparam")
    # 根据时间排序,排除了不能播放的电影
    if filtertype == "style":
        movie_list = Movie.objects.filter(style__contains=filterparam,
                                          movie_address__isnull=False).order_by("-dateyear")
    elif filtertype == "area":
        if filterparam == "其它":
            movie_list = Movie.objects.filter(country__in=movie_area, 
                                              movie_address__isnull=False).order_by("-dateyear")
        else:
            movie_list = Movie.objects.filter(country__contains=filterparam, 
                                              movie_address__isnull=False).order_by("-dateyear")
    elif filtertype == "year":
        if filterparam == "20":
            movie_list = Movie.objects.filter(dateyear__lte="2002-12-30", 
                                              movie_address__isnull=False).order_by("-dateyear")
        else:
            movie_list = Movie.objects.filter(dateyear__contains=filterparam, 
                                              movie_address__isnull=False).order_by("-dateyear")
    else:
        # 默认什么选项都没有的情况下,电影列表就是按照时间排序
        movie_list = Movie.objects.filter(movie_address__isnull=False).order_by("-dateyear")
    random_num = random.randint(0, 99)
    imdbmovie_list = Movie.objects.order_by("douban_score")[random_num:random_num+6]
    usamovie_list = Movie.objects.filter(country__contains="美").order_by("douban_score")[random_num:random_num+6]
    # 进行分页,每页12个Movie实例
    paginator = Paginator(movie_list, 12)
    try:
        movielist = paginator.page(page)
    # 页面号码是无效的还是超过最大页码的情况,默认都是第一页.
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        movielist = paginator.page(1)

    page_range = []
    for p in paginator.page_range:
        page_range.append(p)
    if page >= after_range_num:
        # 获取到整个分页页码列表,比如分了4页,那么就是[1,2,3,4].
        page_range = page_range[page-after_range_num:page+before_range_num]
    else:
        page_range = page_range[0:page+before_range_num]
    #  locals()返回一个包含当前作用域里面的所有变量和它们的值的字典.
    return render(request, "movie/allfilms.html", locals())

def get_filmfest_list(request):
    """
    获取参加电影节的电影列表
    """
    # 为了区别网页上用户选择的选项块.
    action = "getmovielist"
    type = "festival"
    after_range_num = 5
    before_range_num = 4
    # 获取用户请求页的页码,例如:?page=12.
    page = request.GET.get("page")
    if page is not None:
        page = int(page)
    else:
        page = 1
    filtertype = request.GET.get("filtertype")
    filterparam = request.GET.get("filterparam")
    # 过滤有带'节'的字段电影列表,并且能播放
    moviequery = Movie.objects.filter(movie_address__isnull=False, dateyear__contains="节")
    if filtertype == "style":
        movie_list = moviequery.filter(style__contains=filterparam).order_by("-douban_score", "-douban_counter")
    elif filtertype == "area":
        if filterparam == "其它":
            movie_list = moviequery.filter(country__in=movie_area).order_by("-douban_score", "-douban_counter")
        else:
            movie_list = moviequery.filter(country__contains=filterparam).order_by("-douban_score", "-douban_counter")
    elif filtertype == "year":
        if filterparam == "20":
            movie_list = moviequery.filter(dateyear__lte="2002-12-30").order_by("-douban_score", "-douban_counter")
        else:
            movie_list = moviequery.filter(dateyear__contains=filterparam).order_by("-douban_score", "-douban_counter")
    else:
        # 默认什么选项都没有的情况下,电影列表就是按照字段带有'节'的电影列表
        movie_list = moviequery.order_by("-douban_score", "-douban_counter")
    random_num = random.randint(0, 99)
    imdbmovie_list = Movie.objects.order_by("douban_score")[random_num:random_num+6]
    usamovie_list = Movie.objects.filter(country__contains="美").order_by("douban_score")[random_num:random_num+6]
    # 进行分页,每页12个Movie实例
    paginator = Paginator(movie_list, 12)
    try:
        movielist = paginator.page(page)
    # 页面号码是无效的还是超过最大页码的情况,默认都是第一页.
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        movielist = paginator.page(1)

    page_range = []
    for p in paginator.page_range:
        page_range.append(p)
    if page >= after_range_num:
        # 获取到整个分页页码列表,比如分了4页,那么就是[1,2,3,4].
        page_range = page_range[page-after_range_num:page+before_range_num]
    else:
        page_range = page_range[0:page+before_range_num]
    #  locals()返回一个包含当前作用域里面的所有变量和它们的值的字典.
    return render(request, "movie/allfilms.html", locals())

        
        
        

        
    
    






    

