#!encoding:utf-8
__author__ = 'wangfei'
__date__ = '2017/12/24 0024 15:10'

from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True,max_length=50)
    password = forms.CharField(required=True,min_length=6)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误！"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误！"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=6)
    password2 = forms.CharField(required=True,min_length=6)