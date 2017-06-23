#coding:utf-8

from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views

# app_name是为了reverse函数准备的
app_name = "questions"
# ^$代表了空字符串
urlpatterns = [
    url(r'^questions/$', views.questions, name="questions"),
]