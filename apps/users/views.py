#!encoding:utf-8

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db.models import  Q
from django.views.generic.base import View
from .models import  UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm
from django.contrib.auth.backends import  ModelBackend
from  django.contrib.auth.hashers import make_password

from utils.email_send import send_register_email

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        return render(request,"login.html",{})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name= request.POST.get("username","")
            pass_word= request.POST.get("password","")
            user = authenticate(username=user_name,password=pass_word)
            if user is not  None:
                if user.is_active:
                    login(request,user)
                    return  render(request,"index.html")
                else:
                    return render(request,"login.html",{"msg":"用户名或密码错误!"})
            else:
                print  login_form
                return render(request,"login.html",{"msg":"用户名或密码错误!"})
        else:
            return render(request,"login.html",{"login_form":login_form})


class RegisterView(View):
    def get(self,request):
        register_from = RegisterForm()
        return render(request,"register.html",{"register_form":register_from})

    def post(self,request):
        register_from = RegisterForm(request)
        if  register_from.is_valid():
            email_name= request.POST.get("email","")
            pass_word= request.POST.get("password","")
            if  UserProfile.objects.filter(Q(username=email_name)|Q(email=email_name)):
                print "邮箱已经注册"
                return render(request,"register.html",{"msg":"邮箱已经注册！","register_form":register_from})
            else:
                user_profile = UserProfile()
                user_profile.username = email_name
                user_profile.email = email_name
                user_profile.password = make_password(pass_word)
                user_profile.save()
                send_register_email(email_name,'register')
                return render(request,"login.html")
        else:
            return render(request,"register.html",{"register_form":register_from})


class Active_User(View):
    def get(self,request,active_code):
        print active_code
        all_records = EmailVerifyRecord.objects.filter(code=active_code[0:6])
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.is_staff = True
                user.save()
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")


    def post(self,request):
        register_from = RegisterForm(request.POST)
        if  register_from.is_valid():
            user_name= request.POST.get("email","")
            pass_word= request.POST.get("password","")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name,'register')
            return render(request,"login.html")
        else:
            return render(request,"register.html",{"register_form":register_from})


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return  render(request,"forgetpwd.html",{"forget_form":forget_form})


    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            if UserProfile.objects.filter(Q(email=email)|Q(username=email)):
                send_register_email(email,'forget')
                msg =  "发送验证邮件至{email}".format(email=email)
                return render(request,'send_success.html',{"msg":msg})
            else:
                return  render(request,"forgetpwd.html",{"forget_form":forget_form,"msg":"邮箱不存在！"})
        else:
            print "0"
            return  render(request,"forgetpwd.html",{"forget_form":forget_form})


class ResetView(View):
    def get(self,request,active_code):
        print active_code
        all_records = EmailVerifyRecord.objects.filter(code=active_code[0:6])
        if all_records:
            for record in all_records:
                email = record.email
                return  render(request,"password_reset.html",{"email":email})
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")

class ModifyPwd(View):
    def post(self,request):
        modify_from = ModifyPwdForm(request.POST)
        if  modify_from.is_valid():
            pwd1= request.POST.get("password1","")
            pwd2= request.POST.get("password2","")
            email = request.POST.get("email","")

            if pwd1 != pwd2 :
                return render(request,"password_reset.html",{"msg":"密码不一致！"})

            user = UserProfile.objects.get(Q(email=email)|Q(username=email))
            user.password = make_password(pwd1)
            user.save()
            return render(request,"login.html",{"msg":"重置密码成功"})
        else:
            email = request.POST.get("email","")
            return render(request,"password_reset.html",{"modify_from":modify_from,"email":email})


class Test(View):
    def get(self,request):
        return render(request,"org-list.html")