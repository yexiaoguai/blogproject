# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.db.models.query import QuerySet
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView

from webuser.models import Webuser
from blog.utils import pagination_data
from models import Movie, MovieHistory
from templatetags.movie_tags import get_play_most_movies, get_good_evaluation_movies, get_box_office_movies

movie_area = ["阿根廷","巴西","澳大利亚","西班牙","南非","爱尔兰","伊朗","不丹","奥地利",
              "卢森堡","比利时","丹麦"]

def get_movie_list(request):
    """
    获得推荐电影列表和默认电影列表
    """
    LIKE_STYLE_CHOICE = {0:"动作", 1:"悬疑", 2:"爱情", 3:"科幻", 4:"恐怖", 5:"犯罪", 6:"其他"}
    OTHER_LIKE_STYLE = ["剧情", "喜剧", "动画", "纪录片", "情色", "战争", "历史", "惊悚"]

    # 为了区别网页上用户选择的选项块.
    action = "getmovielist"
    choice_type = "suggest"
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
    # moviequery = Movie.objects.filter(movie_address__isnull=False, 
    #                                   douban_score__gte=7.5,
    #                                   douban_counter__gte=2000)
    user = request.user
    # 通过验证
    if user.is_authenticated(): 
        # 如果用户没有设置自己喜爱的电影偏好,就给出全部电影.
        if user.webuser.likesstyle == None:
            movie_list = Movie.objects.all().order_by("-douban_score", "-douban_counter")
        else:
            # 给用户推荐的电影列表.
            likestyle_list = []
            # 空的集合
            movie_list = Movie.objects.none()
            for likestyle in user.webuser.likesstyle[1:-1].split(","):
                likestyle_list.append(LIKE_STYLE_CHOICE[int(likestyle.strip()[2])])
            for likestyle in likestyle_list:
                if likestyle == "其他":
                    for other in OTHER_LIKE_STYLE:
                        movie_list_other = Movie.objects.filter(style__contains=other)
                        # 合并集合
                        movie_list = movie_list | movie_list_other                       
                movie_list_style = Movie.objects.filter(style__contains=likestyle)
                # 合并集合
                movie_list = movie_list | movie_list_style
            movie_list = movie_list.order_by("-douban_score", "-douban_counter")

        # 如果用户选择了style,在电影队列中进行过滤style的字段
        if filtertype == "style":
            movie_list = Movie.objects.filter(style__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "area":
            if filterparam == "其它":
                # 空的集合
                movie_list = Movie.objects.none()
                for area in movie_area:
                    movie_list_area = Movie.objects.filter(country__contains=area)
                    # 合并集合
                    movie_list = movie_list | movie_list_area
                movie_list = movie_list.order_by("-douban_score", "-douban_counter")
            else:
                movie_list = Movie.objects.filter(country__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "year":
            # 过滤上映日期
            if filterparam == "20":
                movie_list = Movie.objects.filter(dateyear__lte="2002-12-30").order_by("-douban_score", "-douban_counter")
            else:
                movie_list = Movie.objects.filter(dateyear__contains=filterparam).order_by("-douban_score", "-douban_counter")
    # 没有登录用户
    else:
        movie_list = Movie.objects.all().order_by("-douban_score", "-douban_counter")
        if filtertype == "style":
            movie_list = Movie.objects.filter(style__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "area":
            if filterparam == "其它":
                # 空的集合
                movie_list = Movie.objects.none()
                for area in movie_area:
                    movie_list_area = Movie.objects.filter(country__contains=area)
                    # 合并集合
                    movie_list = movie_list | movie_list_area
                movie_list = movie_list.order_by("-douban_score", "-douban_counter")
            else:
                movie_list = Movie.objects.filter(country__contains=filterparam).order_by("-douban_score", "-douban_counter")
        elif filtertype == "year":
            # 过滤上映日期
            if filterparam == "20":
                movie_list = Movie.objects.filter(dateyear__lte="2002-12-30").order_by("-douban_score", "-douban_counter")
            else:
                movie_list = Movie.objects.filter(dateyear__contains=filterparam).order_by("-douban_score", "-douban_counter")

    # 进行分页,每页12个Movie实例
    paginator = Paginator(movie_list, 12)
    try:
        movielist = paginator.page(page)
    # 页面号码是无效的还是超过最大页码的情况,默认都是第一页.
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        movielist = paginator.page(1)

    context = {"movielist":movielist,
               "type":choice_type,
               "action":action,
               "filtertype":filtertype,
               "filterparam":filterparam,}
    
    # 默认不分页.
    is_paginated = False
    # 总页码数量大于2的情况下,需要分页.
    if paginator.num_pages > 1:
        is_paginated = True
    # 当前页码.
    page_number = movielist.number
    # 获取到整个分页页码列表,比如分了4页,那么就是[1,2,3,4]
    page_range = paginator.page_range
    total_pages = paginator.num_pages
    # 获取了各种参数.
    data = pagination_data(page_number, page_range, total_pages, is_paginated)
    # 更新参数字典. 
    context.update(data)
    return render(request, "movie/allfilms.html", context=context)

def get_latest_movielist(request):
    """
    获取最新的电影列表
    """
    # 为了区别网页上用户选择的选项块.
    action = "getmovielist"
    choice_type = "latest"
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
            # 空的集合
            movie_list = Movie.objects.none()
            for area in movie_area:
                movie_list_area = Movie.objects.filter(country__contains=area)
                # 合并集合
                movie_list = movie_list | movie_list_area
            movie_list = movie_list.order_by("-dateyear")
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
    
    # 进行分页,每页12个Movie实例
    paginator = Paginator(movie_list, 12)
    try:
        movielist = paginator.page(page)
    # 页面号码是无效的还是超过最大页码的情况,默认都是第一页.
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        movielist = paginator.page(1)

    context = {"movielist":movielist,
               "type":choice_type,
               "action":action,
               "filtertype":filtertype,
               "filterparam":filterparam,}
    
    # 默认不分页.
    is_paginated = False
    # 总页码数量大于2的情况下,需要分页.
    if paginator.num_pages > 1:
        is_paginated = True
    # 当前页码.
    page_number = movielist.number
    # 获取到整个分页页码列表,比如分了4页,那么就是[1,2,3,4]
    page_range = paginator.page_range
    total_pages = paginator.num_pages
    # 获取了各种参数.
    data = pagination_data(page_number, page_range, total_pages, is_paginated)
    # 更新参数字典. 
    context.update(data)
    return render(request, "movie/allfilms.html", context=context)

def get_filmfest_list(request):
    """
    获取参加电影节的电影列表
    """
    # 为了区别网页上用户选择的选项块.
    action = "getmovielist"
    choice_type = "festival"
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
            # 空的集合
            movie_list = Movie.objects.none()
            for area in movie_area:
                movie_list_area = Movie.objects.filter(country__contains=area)
                # 合并集合
                movie_list = movie_list | movie_list_area
            movie_list = movie_list.filter(dateyear__contains="节").order_by("-douban_score", "-douban_counter")
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
    
    # 进行分页,每页12个Movie实例
    paginator = Paginator(movie_list, 12)
    try:
        movielist = paginator.page(page)
    # 页面号码是无效的还是超过最大页码的情况,默认都是第一页.
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        movielist = paginator.page(1)

    context = {"movielist":movielist,
               "type":choice_type,
               "action":action,
               "filtertype":filtertype,
               "filterparam":filterparam,}
    
    # 默认不分页.
    is_paginated = False
    # 总页码数量大于2的情况下,需要分页.
    if paginator.num_pages > 1:
        is_paginated = True
    # 当前页码.
    page_number = movielist.number
    # 获取到整个分页页码列表,比如分了4页,那么就是[1,2,3,4]
    page_range = paginator.page_range
    total_pages = paginator.num_pages
    # 获取了各种参数.
    data = pagination_data(page_number, page_range, total_pages, is_paginated)
    # 更新参数字典. 
    context.update(data)
    return render(request, "movie/allfilms.html", context=context)

def search_movie(request):
    """
    搜索电影.
    """
    # /webuser/?q=aaaa
    if "q" in request.GET:
        # 去除左右空格,有的时候用户会添加空格
        query_string = request.GET.get("q").strip()
        if len(query_string) == 0:
            return redirect("/getmovielist")
        else:
            movielist = Movie.objects.filter(movie_name__contains=query_string)
    return render(request, "movie/allfilms.html", locals())

def movie(request, movie_id):
    """
    电影视图函数.
    """
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, "movie/movie.html", locals())

def get_playmostmovies(request):
    """
    热播电影的视图函数.
    """
    action = "rankinglist"
    type = "playmostmovies"
    movielist = get_play_most_movies()
    return render(request, "movie/ranking_list.html", locals())

def get_good_evaluationmovies(request):
    """
    口碑榜电影的视图函数.
    """
    action = "rankinglist"
    type = "good_evaluationmovies"
    movielist = get_good_evaluation_movies()
    return render(request, "movie/ranking_list.html", locals())

def get_box_officemovies(request):
    """
    北美票房电影的视图函数.
    """
    action = "rankinglist"
    type = "box_officemovies"
    movielist = get_box_office_movies()
    return render(request, "movie/ranking_list.html", locals())