#coding:utf-8

from django import forms

from models import Question, Tag

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

# class ChangeEmailForm_1(forms.ModelForm):
#     """
#     修改用户邮箱表单
#     """
#     id = forms.CharField(widget=forms.HiddenInput())
#     old_email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control"}),
#                                 required=True,
#                                 label="旧邮箱")
#     new_email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control"}),
#                                 required=True,
#                                 label="新邮箱")
    
#     class Meta:
#         model = User
#         fields = ["id", "old_email", "new_email"]

#     def clean(self):
#         super(ChangeEmailForm, self).clean()
#         old_email = self.cleaned_data.get("old_email")
#         new_email = self.cleaned_data.get("new_email")
#         id = self.cleaned_data.get("id")
#         user = User.objects.get(pk=id)
#         # 检查旧邮箱是否是用户的邮箱,不是用户邮箱则提示错误.
#         if old_email != user.email:
#             self._errors["old_email"] = self.error_class(["旧邮箱错误,请输入您原有的邮箱."])
#         return self.cleaned_data