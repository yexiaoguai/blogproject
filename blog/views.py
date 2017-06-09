# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView

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
        # 还有一种情况就是http://zmrenwu.com这种访问,是抛出这个异常,page=None
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
    归档的视图函数
    """
    post_list = models.Post.objects.filter(create_time__year=year,
                                           create_time__month=month
                                           ).order_by("-create_time")
    return render(request, "blog/index.html", context={"post_list":post_list})

def category(request, pk):
    """
    分类的视图函数
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
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        # 将分页导航条的模板变量更新到context中,注意pagination_data方法返回的也是一个字典
        context.update(pagination_data)
        # 将更新后的context返回,以便ListView使用这个字典中的模板变量去渲染模板。
        # 此时context字典中已有了显示分页导航条所需的数据.
        return context

    def pagination_data(self, paginator, page, is_paginated):
        """
        分页的规则如下:
        1.第1页页码,这一页需要始终显示.
        2.第1页页码后面的省略号部分.但要注意如果第1页的页码号后面紧跟着页码号2,那么省略号就不应该显示.
        3.当前页码的左边部分,比如5-6.
        4.当前页码,假设是7.
        5.当前页码的右边部分,比如8-9.
        6.最后一页页码前面的省略号部分.但要注意如果最后一页的页码号前面跟着的页码号是连续的,那么省略号就不应该显示.
        7.最后一页的页码号。
        """
        if not is_paginated:
            # 不需要分页,则无需显示分页导航条,不用任何分页导航条的数据,因此返回一个空的字典
            return {}
        # 当前页面左边连续的页码号,初始值为空
        left = []
        # 当前页面右边连续的页码号,初始值为空
        right = []
        # 标示第一页页码后是否需要显示省略号
        left_has_more = False
        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False
        # 标示是否需要显示第1页的页码号.
        # 因为如果当前页左边的连续页码号中已经含有第1页的页码号,此时就无需再显示第1页的页码号.
        # 其它情况下第一页的页码是始终需要显示的.
        # 初始值为False
        # 举例子:假设当前页面为3,左边显示4个页面,第1,2,3页都会在左边的连续页码号中,
        # 这个情况下第1页包含进去了,因此无需显示第1页的页码号.
        first = False
        # 标示是否需要显示最后一页的页码号
        last = False
        # 获取用户当前请求的页码号
        page_number = page.number
        # 获取分页后的总页数
        total_pages = paginator.num_pages
        # 获取到整个分页页码列表,比如分了4页,那么就是[1,2,3,4]
        page_range = paginator.page_range
        if page_number == 1:
            if total_pages == 2:
                right.append(page_range[1])
            else:     
                # 用户请求的是第一页的数据
                # 页码的右边部分为[2,3],左边和右边的连续页码都是加2
                right.append(page_range[1])
                right.append(page_range[2])
            # 最右边的页码号比最后一页的页码号减去1还要小,说明需要显示省略号
            if right[-1] < total_pages-1:
                right_has_more = True
            # 如果最右边的页码号比最后一页的页码号小,说明当前页右边的连续页码号中不包含最后一页的页码
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            if total_pages == 2:
                left.append(page_range[-2])
            else:
                # 用户请求的是最后一页的数据
                left.append(page_range[-3])
                left.append(page_range[-2])
            if left[0] > 2:
                left_has_more = True
            # 如果最左边的页码号比第一页码号大,说明当前页左边的连续页码号中不包含第一页的页码
            if left[0] > 1:
                first = True
        else:
            #获取到左边的连续两个页面码号
            if page_number-3 < 0:
                left.append(page_range[0])
            else:
                left.append(page_range[page_number-3])
                left.append(page_range[page_number-2])
            if page_number+2 > total_pages:
                right.append(page_range[-1])
            else:
                right.append(page_range[page_number])
                right.append(page_range[page_number+1])
            #判断是否要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages-1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            #判断是否要显示第一页和第一页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            "left":left,
            "right":right,
            "left_has_more":left_has_more,
            "right_has_more":right_has_more,
            "first":first,
            "last":last
        }
        return data