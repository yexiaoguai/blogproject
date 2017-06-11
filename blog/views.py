# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView

from comments.forms import CommentForm
import utils
import models

def index(request):
    """
    博客首页,该视图函数暂停使用,目前相关代码和业务逻辑已经切换IndexView视图类上.
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
        # 还有一种情况就是http://zmrenwu.com这种访问,是抛出这个异常,page=None
        post_list = paginator.page(1)
    except EmptyPage:
        # page的数目超过了最大页数,遇到这种情况会返回最后一页的数据给用户
        post_list = paginator.page(paginator.num_pages)
    return render(request, "blog/index.html", context={"post_list":post_list})

def detail(request, pk):
    """
    文章详情页面视图函数.
    该视图函数暂停使用,目前相关代码和业务逻辑已经切换PostDetailView视图类上.
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
    文章存档的视图函数.
    该视图函数暂停使用,目前相关代码和业务逻辑已经切换ArchivesView视图类上.
    """
    post_list = models.Post.objects.filter(create_time__year=year,
                                           create_time__month=month
                                           ).order_by("-create_time")
    return render(request, "blog/index.html", context={"post_list":post_list})

def category(request, pk):
    """
    文章分类的视图函数.
    该视图函数暂停使用,目前相关代码和业务逻辑已经切换CategoryView视图类上.
    """
    cate = get_object_or_404(models.Category, pk=pk)
    # 过滤post的所有对象,过滤条件就是分类是cate
    post_list = models.Post.objects.filter(category=cate).order_by("-create_time")
    return render(request, "blog/index.html", context={"post_list":post_list})

class IndexView(ListView):
    """
    首页的类视图,类似与首页的视图函数
    """
    model = models.Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给render函数的context参数传递一个字典实现的,
        例如render(request, 'blog/index.html', context={'post_list': post_list}),
        这里传递了一个{'post_list': post_list}字典给模板.
        在类视图中,这个需要传递的模板变量字典是通过get_context_data获得的,
        所以我们复写该方法,以便我们能够自己再插入一些我们自定义的模板变量进去.
        """
        # 获取到父类生成的传递给模板的字典
        context = super(IndexView, self).get_context_data(**kwargs)
        # 父类生成的字典中已有paginator,page_obj,is_paginated这三个模板变量.
        # paginator是Paginator的一个实例.
        # page_obj是Page的一个实例.
        # is_paginated是一个布尔变量,用于指示是否已分页.
        # 例如如果规定每页5个数据,而本身只有2个数据,其实就用不着分页,此时is_paginated=False.
        # 由于context是一个字典,所以调用get方法从中取出某个键对应的值.
        paginator = context.get("paginator")
        page = context.get("page_obj")
        is_paginated = context.get("is_paginated")
        # 获取分页后的总页数
        total_pages = paginator.num_pages
        # 获取到整个分页页码列表,比如分了4页,那么就是[1,2,3,4]
        page_range = paginator.page_range
        # 获取用户当前请求的页码号
        page_number = page.number

        pagination_data = utils.pagination_data(page_number, page_range, total_pages, is_paginated)
        # 将分页导航条的模板变量更新到context中,注意pagination_data方法返回的也是一个字典
        context.update(pagination_data)
        # 将更新后的context返回,以便ListView使用这个字典中的模板变量去渲染模板。
        # 此时context字典中已有了显示分页导航条所需的数据.
        return context

class CategoryView(IndexView):
    """
    文章分类的类视图,继承IndexView,唯一不同的地方是获取到的post_list的条件,
    需要根据category来过滤post_list.
    """
    # get_queryset方法默认获取指定模型的全部列表数据.
    # 为了获取到指定分类下的文章列表数据,覆盖该方法,改写了它的默认行为
    def get_queryset(self):
        category = get_object_or_404(models.Category, pk=self.kwargs.get("pk"))
        return super(CategoryView, self).get_queryset().filter(category=category)

class ArchivesView(IndexView):
    """
    文章存档的视图类
    """
    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year,
                                                               create_time__month=month)

class TagViews(IndexView):
    """
    标签的视图类
    """
    def get_queryset(self):
        tag = get_object_or_404(models.Tag, pk=self.kwargs.get("pk"))
        return super(TagViews, self).get_queryset().filter(tags=tag)

class PostDetailView(DetailView):
    """
    文章详情的视图类
    """
    model = models.Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        # 先调用父类的get方法,是因为只有当get方法被调用后,才能有self.object属性.
        # self.object是Post模型的实例,即被访问的文章post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 被访问的文章的阅读量(get次数)加一
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        """
        get_object方法会返回被访问post对象
        """
        # 获取到父类返回的post对象
        post = super(PostDetailView, self).get_object(queryset=None)
        # 修改下post.content
        md = markdown.Markdown(extensions=["markdown.extensions.extra",
                                           "markdown.extensions.codehilite",
                                           TocExtension(slugify=slugify),
                                      ])
        post.content = md.convert(post.content)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 覆写get_context_data的目的是因为除了将post传递给模板外(DetailView已经帮我们完成),
        # 还要把md.toc(自动生成目录),评论表单,post下的评论列表传递给模板.
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        # 将参数更新.
        context.update({
                        "form":form,
                        "comment_list":comment_list,
                        })
        return context