#coding:utf-8

from django import forms

from models import Question, Tag, Answer

class QuestionForm(forms.ModelForm):
    """
    提问题的表单.
    """
    STYLE_CHOICE = ((u"1", u"动作"), (u"2", u"悬疑"), (u"3", u"爱情"), (u"4", u"科幻"), 
                    (u"5", "恐怖"), (u"6", "喜剧"), (u"7", u"其它"))
    tag = forms.MultipleChoiceField(choices=STYLE_CHOICE,
                                    widget=forms.CheckboxSelectMultiple(),
                                    required=False,
                                    label="标签")

    class Meta:
        model = Question
        fields = ["title", "description", "tag"]
        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"})
        }
        labels = {
            "title":"问题简述",
            "description":"问题详细描述"
        }

class AnswerForm(forms.ModelForm):
    """
    回答问题的表单
    """ 
    answercontent = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "rows":"4"}),
                                    max_length=3000)
    
    class Meta:
        model = Answer
        fields = ["answercontent"]