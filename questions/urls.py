#coding:utf-8

from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views

# app_name是为了reverse函数准备的
app_name = "questions"
# ^$代表了空字符串
urlpatterns = [
    url(r'^questions/$', views.questions, name="questions"),
    url(r'^questions/unanswered_questions$', views.unanswered_questions, name="unanswered_questions"),
    url(r'^questions/answered_questions$', views.answered_questions, name="answered_questions"),
    url(r'^questions/(?P<questionid>[0-9]+)/$', views.question, name="question"),
    url(r'^questions/ask/$', views.ask, name="ask"),
    url(r'^questions/answer/(?P<questionid>[0-9]+)/$', views.answer, name="answer"),
    url(r'^questions/answer/accept/$', views.accept, name="accept"),
    url(r'^questions/answer/vote/$', views.vote, name="vote"),
]