#coding:utf-8

from django.conf.urls import url
import views

# app_name是为了reverse函数准备的
app_name = "movie"
# ^$代表了空字符串
urlpatterns = [
    url(r'^getmovielist/$', views.get_movie_list, name="getmovielist"),
]