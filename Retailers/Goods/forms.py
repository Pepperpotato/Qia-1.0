import re

from django import forms


from django.core.exceptions import ValidationError

# 验证单个字段
from User.models import User


def check_password(value):
    if re.match(r'\d+$', value):
        raise ValidationError("密码不能是纯数字")

# 验证邮箱是否存在
def clean_email(value):
    # print(value)
    res = User.objects.filter(email=value).exists()
    # print(res)
    # print('*'*100)
    if res:
        raise ValidationError("对不起邮箱已存在")

# 验证手机号是否存在
def clean_phone(value):
    # if re.match(r'^1[3456789]\d{9}$',value):
    #     raise ValidationError('对不起手机格式有误')
    res = User.objects.filter(phone=value).exists()
    if res:
        raise ValidationError("对不起手机号已存在")

class UserForm1(forms.Form):
    email = forms.EmailField(label='邮箱', validators=[clean_email], required=False, error_messages={
        # 'invalid': '邮箱格式无效'
    })
    password_1 = forms.CharField(label='密码', validators=[check_password], min_length=6, max_length=128,
                                 widget=forms.PasswordInput(),
                                 error_messages={
                                     'requirde': '必填',
                                     'max_lenth': '最多128个字符',
                                     'min_lenth': '最少6个字符',
                                 })
    password_2 = forms.CharField(label='确认密码', validators=[check_password], min_length=6, max_length=128,
                                 widget=forms.PasswordInput(),
                                 error_messages={
                                     'requirde': '必填',
                                     'max_lenth': '最多128个字符',
                                     'min_lenth': '最少6个字符',
                                 })
    phone = forms.CharField(label='手机号', validators=[clean_phone], required=False, error_messages={

    })
    # 验证两次密码不一致
    def clean(self):
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        # print(password_1, password_2)
        if password_1 != password_2:
            raise ValidationError({'password_2':"两次密码不一致"})
        else:
            return self.cleaned_data




class UserForm2(forms.Form):
    phone = forms.CharField(label='手机号',validators=[clean_phone], required=False, error_messages={

    })
    auth_code=forms.CharField()
    passwordph = forms.CharField(label='密码', validators=[check_password], min_length=6, max_length=128,
                                 widget=forms.PasswordInput(),
                                 error_messages={
                                     'requirde': '必填',
                                     'max_lenth': '最多128个字符',
                                     'min_lenth': '最少6个字符',
                                 })
    passwordRepeatph = forms.CharField(label='确认密码', validators=[check_password], min_length=6, max_length=128,
                                 widget=forms.PasswordInput(),
                                 error_messages={
                                     'requirde': '必填',
                                     'max_lenth': '最多128个字符',
                                     'min_lenth': '最少6个字符',
                                 })
    # 验证两次密码不一致
    def clean(self):
        passwordph = self.cleaned_data.get("passwordph")
        passwordRepeatph = self.cleaned_data.get("passwordRepeatph")
        # print(passwordph, passwordRepeatph)
        if passwordph != passwordRepeatph:
            raise ValidationError({'passwordRepeatph': "两次密码不一致"})
        else:
            return self.cleaned_data




