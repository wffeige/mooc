#!encoding:utf-8
__author__ = 'wangfei'
__date__ = '2017/12/25 0025 20:04'

from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail

from mooc.settings import EMAIL_FROM

def generate_random_str(randomlength=8):
    str = ''
    chars = 'ADAdada1213ADAdada1213ADA'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return  str

def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    code = generate_random_str(6)
    print "random_str:{}".format(code)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''
    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的连接激活你的账号:http://10.0.0.2:8080/active/{0}".format(code)
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            print "邮件发送成功"
        else:
            print "邮件发送失败"

    if send_type == "forget":
        email_title = "慕学在线网密码重置连接"
        email_body = "请点击下面的连接重置你的密码:http://10.0.0.2:8080/reset/{0}".format(code)
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            print "邮件发送成功"
        else:
            print "邮件发送失败"