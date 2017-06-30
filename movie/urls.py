#coding:utf-8

from django.conf.urls import url
import views

# app_name是为了reverse函数准备的
app_name = "movie"
# ^$代表了空字符串
urlpatterns = [
    url(r'^getmovielist/$', views.get_movie_list, name="getmovielist"),
    url(r'^getlatestmovielist/$', views.get_latest_movielist, name="getlatestmovielist"),
    url(r'^getfilmfestlist/$', views.get_filmfest_list, name="getfilmfestlist"),
    url(r'^searchmovie/$', views.search_movie, name="searchmovie"),
    url(r'^movie/(?P<movie_id>[0-9]+)/$', views.movie, name="movie"),
    url(r'^ranking_list/playmostmovies/$', views.get_playmostmovies, name="playmostmovies"),
    url(r'^ranking_list/box_officemovies/$', views.get_box_officemovies, name="box_officemovies"),
    url(r'^ranking_list/good_evaluationmovies/$', views.get_good_evaluationmovies, name="good_evaluationmovies"),
]