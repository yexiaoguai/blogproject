#coding:utf-8

from django import forms
from models import Comment

class CommentForm(forms.ModelForm):
    """
    在表单的内部类Meta里指定一些和表单相关的东西.model=Comment表明这个表单对应的数据库模型是Comment类.
    fields = ['name', 'email', 'url', 'text'] 指定了表单需要显示的字段,
    这里我们指定了 name,email,url,text需要显示
    """
    class Meta:
        model = Comment
        fields = ["name", "email", "url", "text"]