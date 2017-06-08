# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comments.forms import CommentForm
import models

def index(request):
    """
    博客首页
    """
    # 排序依据的字段是created_time,即文章的创建时间,'-'号表示逆序.
    post_list = models.Post.objects.all().order_by("-create_time")
    # 对post_list进行分页,每页5篇文章
    paginator = Paginator(post_list, 5)
    # 获取用户请求页的页码.给页码设置的URL类似于http://www.baidu.com/?page=2
    # 其中?号后面的page=2表示用户请求的页码数.
    # Django会将问号后面的请求参数保存到request.GET属性里,这是一个类字典的属性.
    # 例如这里page作为键被保存,其值为2.
    page = request.GET.get("page")
    try:
        # 获取用户请求页面的文章列表,比如说page=2,就获取第二页的文章列表
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # 用户可能请求http://zmrenwu.com/?page=xyz这样的URL,就将第一页数据返回给用户.
        # 还有一种情况就是http://zmrenwu.com这种访问页是抛出这个异常
        post_list = paginator.page(1)
    except EmptyPage:
        # page的数目超过了最大页数,遇到这种情况会返回最后一页的数据给用户
        post_list = paginator.page(paginator.num_pages)
    return render(request, "blog/index.html", context={"post_list":post_list})

def detail(request, pk):
    """
    文章详情页面相应函数
    """
    # get_object_or_404方法,其作用就是当传入的pk对应的Post在数据库存在时,
    # 就返回对应的post,如果不存在,就给用户返回一个404错误,表明用户请求的文章不存在.
    post = get_object_or_404(models.Post, pk=pk)
    # markdown.extensions.codehilite代码高亮的拓展
    # TocExtension(slugify=slugify)Toc自动生成目录,还美化了URL
    md = markdown.Markdown(extensions=[
                                         "markdown.extensions.extra",
                                         "markdown.extensions.codehilite",
                                         TocExtension(slugify=slugify),
                                      ])
    post.content = md.convert(post.content)
    # 获取评论表单的实例
    form = CommentForm()
    # 获取这篇post下的全部评论
    comment_list = post.comment_set.all()
    # 将文章,表单,以及文章下的评论列表作为模板变量传给detail.html模板,以便渲染相应数据
    # 添加了一个toc参数,该参数是生成目录的拓展
    context = {"post":post,
               "toc":md.toc,
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



