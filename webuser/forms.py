#coding:utf-8

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.safestring import mark_safe

def ForbiddenUsernamesValidator(value):
    """
    注册用户名的时候,被限制的用户名,是一个验证器,通过该方法来验证用户名是否可用.
    """
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup', 
        'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator', 
        'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
        'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs', 
        'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
        'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads', 
        'contact', 'blogs', 'feed', 'feeds', 'faq', 'intranet', 'log', 'registration', 'search', 
        'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
        'follow', 'activity', 'questions', 'articles', 'network']
    if value.lower() in forbidden_usernames:
        raise ValidationError("被限制的用户名,请您重新命名.")

def InvalidUsernameValidator(value):
    """
    验证用户名是否含有一些特殊符号.
    """
    if "@" in value or "+" in value or "-" in value:
        raise ValidationError("请输入正确的用户名.")

def UniqueUsernameIgnoreCaseValidator(value):
    """
    验证该用户是否已经注册过.
    """
    # 名称为value但是不区分大小写,可以找到ABC,Abc,aBC,这些都符合条件
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError("用户名已经存在.")

def UniqueEmailValidator(value):
    """
    验证email是否被注册过
    """
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError("该邮箱已经被注册过.")

def SignupDomainValidator(value):
    """
    该函数暂时不实现
    """

class HorizontalCheckRenderer(forms.CheckboxSelectMultiple):
    def render(self):
        # super(HorizontalCheckRenderer, self).render()
        return mark_safe("\n".join(["&nbsp;&nbsp;&nbsp;%s\n" % w for w in self]))

class HorizontalRadioRenderer(forms.RadioSelect):
    """
    实现水平排列单选按钮.
    """
    def __init__(self, *args, **kwargs):
        super(HorizontalRadioRenderer, self).__init__(*args, **kwargs)
    

    def render(self):
        # super(HorizontalRadioRenderer, self).render()
        return mark_safe("\n".join(["&nbsp;&nbsp;&nbsp;%s\n" % w for w in self]))

class LoginForm(forms.ModelForm):
    """
    用户登录表单.
    在表单的内部类Meta里指定一些和表单相关的东西.model=User表明这个表单对应的数据库模型是Comment类.
    fields = ["username", "password"] 指定了表单需要显示的字段,
    这里我们指定了"username", "password"需要显示
    """
    # Widget:用来渲染成HTML元素的工具,如:forms.Textarea对应HTML中的<textarea>标签
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),
                               max_length=30,
                               required=True,
                               label="用户名",
                               error_messages={"required":"用户名不能为空"})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),
                               required=True,
                               label="密码",
                               error_messages={"required":"密码不能为空"})
    class Meta:
        model = User
        fields = ["username", "password"]
        exclude = ["last_login", "date_joined", "email", "confirm_password"]
    
    # clean方法重写时一定不要忘了return cleaned_data
    def clean(self):
        # 获取username值
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            # 认证用户的密码是否有效,若有效则返回代表该用户的user对象,若无效则返回None.
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                # 如果出现密码错误的情况下,在用户名下面进行提示
                self._errors["username"] = self.error_class(["账户密码不匹配!"])
        return self.cleaned_data

class SignUpForm(forms.ModelForm):
    """
    用户注册表单
    """
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),
                               max_length=30,
                               required=True,
                               label="用户名",
                               help_text="用户名最好包括字母和数字.")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),
                               required=True,
                               label="密码")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),
                                       required=True,
                                       label="确认密码")
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control"}),
                                       required=True,
                                       label="邮箱",
                                       max_length=75)
    
    class Meta:
        model = User
        fields = ["username", "password", "confirm_password", "email"]
        exclude = ["last_login", "date_joined"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # 为username做一些验证,用来判断用户名是否符合标准
        self.fields["username"].validators.append(ForbiddenUsernamesValidator)
        self.fields["username"].validators.append(InvalidUsernameValidator)
        self.fields["username"].validators.append(UniqueUsernameIgnoreCaseValidator)
        self.fields["email"].validators.append(UniqueEmailValidator)
        # self.fields["email"].validators.append(SignupDomainValidator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and password != confirm_password:
            self._errors["password"] = self.error_class(["确认密码不相同!"])
        return self.cleaned_data

class ProfileForm(forms.ModelForm):
    """
    用户资料表单
    """
    LIKE_STYLE_CHOICE = (("0", "动作"), ("1", "悬疑"), ("2", "爱情"), ("3", "科幻"), 
                         ("4", "恐怖"), ("5", "犯罪"), ("6", "其他"))
    JOB_CHOICE = (("0", "学生"), ("1", "工程师"), ("2", "个体户"), ("3", "公务员"), ("4", "其他"))
    url = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),
                          max_length=50,
                          required=False,
                          label="个人主页")
    location = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),
                               max_length=50,
                               required=False,
                               label="省市")
    # job_title = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={"class":"radio-inline"}),
    #                                       choices=JOB_CHOICE,
    #                                       required=False,
    #                                       label="职业")
    job_title = forms.IntegerField(widget=forms.RadioSelect(choices=JOB_CHOICE, attrs={"class":"radio-inline"}),
                                   required=False,
                                   label="职业")
    sex = forms.IntegerField(widget=forms.RadioSelect(choices=((0, "男"), (1, "女")), attrs={"class":"radio-inline"}),
                             label="性别")
    likestyle = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                          choices=LIKE_STYLE_CHOICE,
                                          label="喜欢电影的类型")
    
    class Meta:
        model = User
        fields = ["url", "location", "job_title", "sex", "likestyle"]
