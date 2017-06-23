# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Question

def questions(request):
    """
    展现所有问题的视图函数
    """
    return all(request)

def all(request):
    # 获取到所有问题列表
    questions = Question.objects.all()
    return _questions(request, questions, "all")

def _questions(request, questions, active):
    paginator = Paginator(questions, 10)
    page = request.GET.get("page")
    if page is not None:
        page = int(page)
    else:
        page = 1
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # 用户可能请求http://zmrenwu.com/?page=xyz这样的URL,就将第一页数据返回给用户.
        # 还有一种情况就是http://zmrenwu.com这种访问,是抛出这个异常,page=None
        questions = paginator.page(1)
    except EmptyPage:
        # page的数目超过了最大页数,遇到这种情况会返回最后一页的数据给用户
        questions = paginator.page(paginator.num_pages)
    context = {"questions":questions,
               "active":active} 
    return render(request, "questions/questions.html", context=context)

