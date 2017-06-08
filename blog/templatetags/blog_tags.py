#coding:utf-8
"""
模板标签
"""
from django import template
from ..models import Post, Category

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    """
    最新文章模板标签
    这个函数的功能是获取数据库中前num篇文章,这里num默认为5.
    Django在模板中还不知道该如何使用它.为了能够通过{% get_recent_posts %} 
    的语法在模板中调用这个函数,必须按照Django的规定注册这个函数为模板标签
    """
    return Post.objects.all().order_by("-create_time")[:num]

@register.simple_tag
def archives():
    """
    归档模板标签
    这个函数会返回一个列表,列表中的元素为每一篇文章的创建时间,
    并且是python的date对象,精确到月份,降序排列.
    三个参数,分别为:一个是create_time,即Post的创建时间,
    month是精度,order='DESC'表明降序排列
    """
    return Post.objects.dates("create_time", "month", order="DESC")

@register.simple_tag
def get_categories():
    """
    分类模板标签
    """
    return Category.objects.all()
    
