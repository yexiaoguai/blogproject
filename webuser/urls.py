#coding:utf-8

from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views

# app_name是为了reverse函数准备的
app_name = "webuser"
# ^$代表了空字符串
urlpatterns = [
    url(r'^webuser/$', views.index, name="webuser_index"),
    url(r'^weblogin/$', views.web_login, name="webuser_login"),
    url(r'^register/$', views.register, name="webuser_register"),
    url(r'^settings/$', views.settings, name="webuser_settings"),
    url(r'^weblogout/$', auth_views.logout, {"next_page":"/webuser"}, name="webuser_logout"),
]