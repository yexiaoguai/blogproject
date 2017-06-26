#coding:utf-8

from django import forms

from models import Question, Tag, Answer

class QuestionForm(forms.ModelForm):
    """
    提问题的表单.
    """
    choices=[(t.id, t.name) for t in Tag.objects.all()]
    tag = forms.MultipleChoiceField(choices=choices,
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