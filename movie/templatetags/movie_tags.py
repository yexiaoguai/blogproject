#coding:utf-8
"""
模板标签
"""
from django import template
from django.db.models.aggregates import Count

from ..models import MovieRankings, Movie

register = template.Library()

@register.simple_tag
def get_play_most_movies():
    """
    电影排行榜模板标签
    """
    most_movies_tag = MovieRankings.objects.filter(pk = 1)
    return Movie.objects.filter(movierankings = most_movies_tag).order_by("-douban_score", "-douban_counter")

@register.simple_tag
def get_good_evaluation_movies():
    """
    电影排行榜模板标签
    """
    most_movies_tag = MovieRankings.objects.filter(pk = 2)
    return Movie.objects.filter(movierankings = most_movies_tag).order_by("-douban_score", "-douban_counter")

@register.simple_tag
def get_box_office_movies():
    """
    电影排行榜模板标签
    """
    most_movies_tag = MovieRankings.objects.filter(pk = 3)
    return Movie.objects.filter(movierankings = most_movies_tag).order_by("-douban_score", "-douban_counter")