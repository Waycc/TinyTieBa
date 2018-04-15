from django import forms
from tieba import models
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
import re


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=32,error_messages={
        'required': '标题不能为空'
    })
    content = forms.CharField(min_length=10, widget=forms.Textarea, error_messages={
        'required': '内容不能为空',
        'min_length': '内容不能少于10个字'
    })


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=700, error_messages={
        'required': '邮箱不能为空',
        'invalid':'请输入正确格式的邮箱'
    })
    password = forms.CharField(max_length=700,error_messages={
        'required': '密码不能为空',
    })


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(max_length=700, error_messages={
        'required': '邮箱不能为空',
        'invalid': '请输入正确格式的邮箱',
    })
    name = forms.CharField(max_length=11,error_messages={
        'required': '用户名不能为空',
        'invalid': '名字不能超过11个字'
    })
    password = forms.CharField(min_length=6, error_messages={
        'required': '密码不能为空',
        'min_length': '密码不能少于6位',
    })
    def clean_email(self):
        email = self.cleaned_data['email']
        is_exist = models.UserProfile.objects.filter(email=email)
        if is_exist:
            raise ValidationError('邮箱已被注册','exist')
        else:
            return email

    def clean_name(self):
        name = self.cleaned_data['name']
        is_exist = models.UserProfile.objects.filter(name=name)
        if is_exist:
            raise ValidationError('用户名已被注册','exist')
        else:
            return name
