# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q

from .models import Question, Tag, Answer, Activity
from .forms import QuestionForm, AnswerForm

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
    action = "questions"
    question = get_object_or_404(Question, pk=questionid)
    form = AnswerForm(instance=question)
    context = {"question":question,
               "action":action,
               "form":form}
    return render(request, "questions/question.html", context=context)
    
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

@login_required
def answer(request, questionid):
    """
    发送答案的视图函数.
    """
    question = get_object_or_404(Question, pk=questionid)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer()
            answer.user = request.user
            answer.question = question
            answer.answer_content = form.cleaned_data.get("answercontent")
            print "answer.question:", answer.question
            answer.save()
            #
            answer.user.webuser.notify_answered(answer.question)
            return redirect(u"/questions/{0}".format(answer.question.pk))
        else:
            return render(request, "questions/question.html", {"question":question, "form":form})
    else:
        return redirect("/questions/")

@login_required
def accept(request):
    """
    问题提问者接受答案的视图函数.
    """
    answer_id = request.POST["answer"]
    answer = Answer.objects.get(pk=answer_id)
    user = request.user
    # 通知用户的答案被接受
    #
    # 如果当前的用户是提出该问题的用户,可以将答案设置成接受.
    if user == answer.question.user:
        answer.accept()
        return HttpResponse()
    else:
        return HttpResponseForbidden()

@login_required
def vote(request):
    """
    用户投票的视图函数.
    """
    answer_id = request.POST["answer"]
    answer = Answer.objects.get(pk=answer_id)
    # "R","U","D"
    vote = request.POST["vote"]
    user = request.user
    # 在所有的动作中,获取到该答案的作者,答案id,以及他的vote activity
    activity = Activity.objects.filter(
        Q(activity_type=Activity.UP_VOTE) | Q(activity_type=Activity.DOWN_VOTE),
        user=user, 
        answer=answer_id)
    # 如果该用户有给这个答案投票的行为的话,就进行删除
    if activity:
        activity.delete()
    if vote in [Activity.UP_VOTE, Activity.DOWN_VOTE]:
        # 保存这次的投票行为.
        activity = Activity(activity_type=vote, user=user, answer=answer_id)
        activity.save()
    return HttpResponse(answer.calculate_votes())
