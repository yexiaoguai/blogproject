# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from forms import LoginForm, SignUpForm, ProfileForm
from models import Webuser

def index(request):
    """
    首页的视图函数.
    """
    user = request.user
    action = "webuser"
    print "user:",user
    return render(request, "webuser/index.html", locals())

def web_login(request):
    """
    用户登录的视图函数.
    """
    # 如果用户认证过,重定向到首页
    if request.user.is_authenticated():
        return redirect("/")
    if request.method == "POST":
        # 用户提交的数据存在request.POST中,这是一个类字典对象.
        # 我们利用这些数据构造了LoginForm的实例,这样Django的表单就生成了.
        form = LoginForm(request.POST)
        print "form is :", form
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, "webuser/personal.html")
        else:
            return render(request, "webuser/login.html", {"form":form})
    # 如果不是提交数据的request,就需要转到登录界面
    else:
        return render(request, "webuser/login.html", {"form":LoginForm()})

def register(request):
    """
    用户注册的视图函数.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, "webuser/register.html", {"form":form})
        else:
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # 创建用户
            User.objects.create_user(username=username, password=password, email=email)
            # 获取到刚刚创建的用户
            user = authenticate(username=username, password=password)
            # 为新用户创建一个该用户的设置表
            webuser = Webuser(user=user)
            webuser.save()
            # 用户登录
            login(request, user)
            return redirect("/webuser")
    else:
        return render(request, "webuser/register.html", {"form":SignUpForm()})

@login_required
def settings(request):
    # 获取用户
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            # 为wenuser对象属性添加数据
            webuser = Webuser.objects.get(user=user)
            webuser.job_title = form.cleaned_data.get("job_title")
            webuser.location = form.cleaned_data.get("location")
            webuser.url = form.cleaned_data.get("url")
            webuser.likesstyle = form.cleaned_data.get("likestyle")
            webuser.sex = form.cleaned_data.get("sex")
            # 保存数据
            webuser.save()
            # 直接为该页面发送消息
            messages.add_message(request, messages.SUCCESS, "您的资料已经编辑成功.")
    else:
        form = ProfileForm(instance=user,
                           initial={
                               "job_title":user.webuser.job_title,
                               "url":user.webuser.url,
                               "location":user.webuser.location,
                               "sex":user.webuser.sex,
                               "likestyle":user.webuser.likesstyle
                           })
    return render(request, "webuser/person_home_page_info.html", {"form":form})
