# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from comments.forms import CommentForm
import models

def index(request):
    """
    博客首页
    """
    # 排序依据的字段是created_time,即文章的创建时间,'-'号表示逆序.
    post_list = models.Post.objects.all().order_by("-create_time")
    return render(request, "blog/index.html", context={"post_list":post_list})

def detail(request, pk):
    """
    文章详情页面相应函数
    """
    # get_object_or_404方法,其作用就是当传入的pk对应的Post在数据库存在时,
    # 就返回对应的post,如果不存在,就给用户返回一个404错误,表明用户请求的文章不存在.
    post = get_object_or_404(models.Post, pk=pk)
    post.content = markdown.markdown(post.content, 
                                     extensions=[
                                         "markdown.extensions.extra",
                                         "markdown.extensions.codehilite",
                                         "markdown.extensions.toc",
                                     ])
    # 获取评论表单的实例
    form = CommentForm()
    # 获取这篇post下的全部评论
    comment_list = post.comment_set.all()
    # 将文章,表单,以及文章下的评论列表作为模板变量传给detail.html模板,以便渲染相应数据
    context = {"post":post,
               "form":form,
               "comment_list":comment_list}
    return render(request, "blog/detail.html", context=context)

def archives(request, year, month):
    """
    归档的相应函数
    """
    post_list = models.Post.objects.filter(create_time__year=year,
                                           create_time__month=month
                                           ).order_by("-create_time")
    return render(request, "blog/index.html", context={"post_list":post_list})

def category(request, pk):
    """
    分类的相应函数
    """
    cate = get_object_or_404(models.Category, pk=pk)
    # 过滤post的所有对象,过滤条件就是分类是cate
    post_list = models.Post.objects.filter(category=cate).order_by("-create_time")
    return render(request, "blog/index.html", context={"post_list":post_list})



