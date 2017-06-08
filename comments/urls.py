#coding:utf-8

from django.conf.urls import url
import views

# app_name是为了reverse函数准备的
app_name = "comments"
# ^$代表了空字符串
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name="post_comment"),
]