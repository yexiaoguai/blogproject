#coding:utf-8

from django.conf.urls import url
import views

# app_name是为了reverse函数准备的
app_name = "webuser"
# ^$代表了空字符串
urlpatterns = [
    url(r'^webuser/$', views.index, name="webuser_index"),
]