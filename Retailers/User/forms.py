import hashlib
import re

from django import forms
from django.core.exceptions import ValidationError

from User.models import User


class ChangeForm(forms.Form):
    username = forms.CharField(min_length=3, required=False ,error_messages={
        'required': '用户名不可为空',
        'min_length': '用户名不能少于三位'
    })
    oldpassword = forms.CharField(min_length=6, required=False, error_messages={
        'required': '密码不可为空',
        'min_length': '密码不能少于三位'
    })
    newpassword = forms.CharField(min_length=6, required=False, error_messages={
        'required': '新密码不可为空',
        'min_length': '密码不能少于三位'
    })
    renewpassword = forms.CharField(min_length=6, required=False, error_messages={
        'required': '新密码不可为空',
        'min_length': '密码不能少于三位'
    })

    phonenumber = forms.CharField(max_length=11, required=False, error_messages={
        'min_length': '手机号不能于11位'
    })
    email = forms.EmailField(min_length=5, required=False, error_messages={
        'min_length': '邮箱格式错误'
    })

    # def clean_username(self):
    #     res = User.objects.filter(username=self.cleaned_data.get('username')).exists()
    #     if res:
    #         raise ValidationError('用户名已存在')
    #     return self.cleaned_data.get('username')

    def clean_oldpassword(self):
        db_password = User.objects.values('password').filter(username=self.cleaned_data.get('username'))
        input_pasword = self.cleaned_data.get('oldpassword')
        print(1234567,input_pasword)
        input_pasword = hashlib.sha1(input_pasword.encode('utf8')).hexdigest()
        if db_password[0].get('password') != input_pasword:
            raise ValidationError('密码错误')
        return self.cleaned_data.get('oldpassword')

    def clean_newpassword(self):
        pwd = self.cleaned_data.get('newpassword')

        if re.match(r'\d+$', pwd):
            raise ValidationError('密码不能为纯数字')
        return pwd

    def clean_renewpassword(self):
        pwd1 = self.cleaned_data.get('newpassword')
        pwd2 = self.cleaned_data.get('renewpassword')
        if pwd1 != pwd2 :
            raise ValidationError('两次密码不一致')
        return pwd2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'\w+@\w+.com$', email):
            raise ValidationError('邮箱格式不正确')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phonenumber')
        if not re.match(r'1[35678]\d{9}', phone):
            raise ValidationError('手机号不存在')
        return phone




