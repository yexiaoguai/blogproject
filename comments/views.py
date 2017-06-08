# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from models import Comment
from forms import CommentForm

def post_comment(request, post_pk):
    # 获取评论的文章
    post = get_object_or_404(Post, pk=post_pk)
    #
    if request.method == "POST":
        # 用户提交的数据存在request.POST中,这是一个类字典对象.
        # 我们利用这些数据构造了CommentForm的实例,这样Django的表单就生成了.
        form = CommentForm(request.POST)
        # 当调用form.is_valid()方法时,Django自动帮我们检查表单的数据是否符合格式要求.
        if form.is_valid():
            # 检查到数据是合法的,调用表单的save方法保存数据到数据库,
            # commit=False的作用是仅仅利用表单的数据生成Comment模型类的实例,但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            # 将评论和被评论的文章关联起来
            # 因为在这个Comment类的实例里,post字段是空的.
            comment.post = post
            # 将评论数据保存到数据库
            comment.save()
            # 重定向到post的详情页,实际上当redirect函数接收一个模型的实例时,
            # 它会调用这个模型实例的get_absolute_url方法,
            # 然后重定向到get_absolute_url方法返回的URL.
            return redirect(post)
        # 检查到数据不合法,重新渲染详情页,并且渲染表单的错误.
        else:
            # post.comment_set.all()方法,
            # 这个用法有点类似于Post.objects.all()
            # 其作用是获取这篇post下的的全部评论.
            comment_list = post.comment_set.all()
            post.content = markdown.markdown(post.content, 
                                     extensions=[
                                         "markdown.extensions.extra",
                                         "markdown.extensions.codehilite",
                                         "markdown.extensions.toc",
                                     ])
            # 传了三个模板变量给detail.html,
            # 一个是文章(Post),一个是评论列表,一个是表单(form)
            context = {"post":post,
                       "form":form,
                       "comment_list":comment_list
                       }
            return render(request, "blog/detail.html", context=context)
    # 不是post请求,重定向到文章详情页面
    return redirect(post)
            

            

