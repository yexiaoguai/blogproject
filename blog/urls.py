#coding:utf-8

from django.conf.urls import url
import views

# app_name是为了reverse函数准备的
app_name = "blog"
# ^$代表了空字符串
urlpatterns = [
    url(r'^blog/$', views.IndexView.as_view(), name="index"),
    url(r'^blog/post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name="detail"),
    url(r'^blog/archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name="archives"),
    url(r'^blog/category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name="category"),
    url(r'^blog/tag/(?P<pk>[0-9]+)/$', views.TagViews.as_view(), name="tag"),
]