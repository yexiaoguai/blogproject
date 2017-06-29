#coding:utf-8

from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views

# app_name是为了reverse函数准备的
app_name = "webchat"
# ^$代表了空字符串
urlpatterns = [
    url(r'^webchat/$', views.webchat, name="webchat"),
    url(r'^webchat/contacts/$', views.contacts, name="load_contact_list"),
    url(r'^webchat/newmessage/$', views.newmessage, name="send_msg"),
    url(r'^webchat/newmessage/$', views.newmessage, name="get_new_msgs"),
]