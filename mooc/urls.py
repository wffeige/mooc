#!encoding:utf-8
"""mooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
import  xadmin
from django.views.generic import TemplateView
from users.views import LoginView,RegisterView,Active_User,ForgetPwdView,ResetView,ModifyPwd,Test
from organization.views import OrgView
from django.views.static import  serve
from mooc.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html"),name="index"),
    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^register/$',RegisterView.as_view(),name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*$)',Active_User.as_view(),name="active"),
    url(r'^forget/$',ForgetPwdView.as_view(),name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*$)',ResetView.as_view(),name="reset_pws"),
    url(r'^modify/$',ModifyPwd.as_view(),name="modify_pwd"),

    #课程机构首页
    url(r'^org_list/$',OrgView.as_view(),name="org_list"),
    #配置上传文件的处理
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
]
