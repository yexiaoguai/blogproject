# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Tag
from .forms import QuestionForm

import sys

def questions(request):
    """
    展现所有问题的视图函数.
    """
    return all(request)

def question(request, questionid):
    """
    单个问题的视图函数.
    """
    question = get_object_or_404(Question, pk=questionid)
    
def all(request):
    """
    所有问题列表视图函数.
    """
    questions = Question.objects.all()
    return _questions(request, questions, "all")

def unanswered_questions(request):
    """
    未采纳问题列表的视图函数.
    """
    questions = Question.get_unanswered()
    return _questions(request, questions, "unanswered")

def answered_questions(request):
    """
    采纳问题列表的视图函数.
    """
    questions = Question.get_answered()
    return _questions(request, questions, "answered")

def _questions(request, questions, active):
    action = "questions"
    paginator = Paginator(questions, 10)
    page = request.GET.get("page")
    if page is not None:
        page = int(page)
    else:
        page = 1
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        # page的数目超过了最大页数,遇到这种情况会返回最后一页的数据给用户
        questions = paginator.page(paginator.num_pages)
    context = {"questions":questions,
               "active":active,
               "action":action} 
    return render(request, "questions/questions.html", context=context)

@login_required
def ask(request):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    action = "questions"
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question()
            question.user = request.user
            question.title = form.cleaned_data.get("title")
            question.description = form.cleaned_data.get("description")
            tag_id_list = form.cleaned_data.get("tag")
            # 只有先保存了question对象,才能关联tag
            question.save()
            print "type and tag:", type(tag_id_list),tag_id_list
            for tag_id in tag_id_list:
                tag = Tag.objects.get(id=int(tag_id))
                question.tag.add(tag)
            return redirect("/questions/")
        else:
            return render(request, "questions/ask.html", {"form":form, "action":action})
    else:
        form = QuestionForm()
    return render(request, "questions/ask.html", {"form":form, "action":action})
