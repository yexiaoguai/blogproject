# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings as django_settings

from forms import LoginForm, SignUpForm, ProfileForm, ChangePasswordForm, ChangeEmailForm
from models import Webuser
from PIL import Image
import os, json

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
    """
    个人资料视图函数.
    """
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

@login_required
def change_password(request):
    """
    用户修改密码的视图函数
    """
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            # 设置新密码
            user.set_password(new_password)
            user.save()
            # 更改密码后,需要用户再次登录
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "您的密码修改成功.")
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, "webuser/change_password.html", {"form":form})

@login_required
def change_email(request):
    """
    用户修改邮箱的视图函数.
    """
    user = request.user
    if request.method == "POST":
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data.get("new_email")
            # 设置新邮箱
            user.email = new_email
            # 只更新email字段
            user.save(update_fields=["email"])
            messages.add_message(request, messages.SUCCESS, "您的邮箱修改成功.")
    else:
        form = ChangeEmailForm(instance=user)
    return render(request, "webuser/change_email.html", {"form":form})

@login_required
def picture(request):
    uploaded_picture= False
    # 说明头像已经上传到了服务器
    if request.GET.get("upload_picture") == "uploaded":
        uploaded_picture= True
    context = {"uploaded_picture":uploaded_picture,
               "MEDIA_URL":django_settings.MEDIA_URL}
    return render(request, "webuser/picture.html", context=context)

@login_required
def upload_picture(request):
    """
    上传头像的视图函数
    """
    try:
        # 获取到头像存放目录的路径
        webuser_picture = django_settings.MEDIA_ROOT+"/webuser_pictures/"
        # 上传的文件
        f = request.FILES["picture"]
        # 文件名
        filename = webuser_picture+request.user.username+"_tmp.jpg"
        # 写入到filename,把上传的文件用二进制的方式写入
        with open(filename, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        # 打开图片
        im = Image.open(filename)
        width,height = im.size
        if width > 350:
            new_width = 350
            new_height = (height*350)/width
            new_size = new_width,new_height
            # 重新设定号新的头像(抗锯齿)
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)
        # 最后重定向到头像页面,给一个参数说明头像已经上传.
        return redirect("/settings/picture/?upload_picture=uploaded")
    except Exception as e:
        return redirect("/settings/picture/")

@login_required
def save_uploaded_picture(request):
    """
    保存用户上传的头像,用户可以根据上传的头像裁剪自己想要的头像.
    """
    try:
        # 获取宽高参数
        x = int(request.POST.get("x"))
        y = int(request.POST.get("y"))
        w = int(request.POST.get("w"))
        h = int(request.POST.get("h"))
        tmp_filename = django_settings.MEDIA_ROOT+"/webuser_pictures/"+request.user.username+"_tmp.jpg"
        filename = django_settings.MEDIA_ROOT+"/webuser_pictures/"+request.user.username+".jpg"
        im = Image.open(tmp_filename)
        # 根据参数裁剪头像
        cropped_im = im.crop((x, y, w+x, h+y))
        # 缩放头像
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        # 删除临时头像文件
        os.remove(tmp_filename)
    except Exception as e:
        pass
    return redirect("/settings/picture")

@login_required
def getuserinfo(request, userid):
    JOB_CHOICE = {0:"学生", 1:"工程师", 2:"个体户", 3:"公务员", 4:"其他"}

    user = User.objects.get(pk=userid)
    job = JOB_CHOICE[int(user.webuser.job_title)]
    print "朋友数据:",user.webuser.friends.all()
    for friend in user.webuser.friends.all():
        print "姓名:",friend.user
        print "图片",friend.get_picture
    friends = user.webuser.friends.all()
    return render(request, "webuser/userinfo.html", {"user":user, "job":job, "friends":friends})

@login_required
def addfriends(request):
    """
    添加好友
    """
    if request.method == "POST":
        data = json.loads(request.POST.get("data"))
        friendid = data["friendid"]
        actiontype = data["actiontype"]
        print "添加好友的数据:", data
        if actiontype == "friend":
            # 获取当前用户的webuser
            webuser = request.user.webuser
            if webuser.id == int(friendid):
                return HttpResponse("error")
            # 根据friendid获取到用户webuser
            friend = Webuser.objects.get(pk=friendid)
            # 将friend添加到该用户的好友里
            webuser.friends.add(friend)
        return HttpResponse("success")
    else:
        return HttpResponse("error")