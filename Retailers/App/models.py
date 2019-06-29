from datetime import datetime

from django.db import models


# Create your models here.


# 用户表
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    realname = models.CharField(max_length=20, null=True)   # 真名
    username = models.CharField(max_length=20)    # 昵称
    password = models.CharField(max_length=128)     # 密码
    pay_password = models.CharField(max_length=128)     # 支付密码
    user_type = models.IntegerField(default=0, null=True)   # 用户类型 0为普通用户 1为管理员
    certificate = models.CharField(max_length=20)   # 证件类型
    certificate_id = models.CharField(max_length=20)    # 证件号码
    phone_number = models.CharField(max_length=20)  # 手机号码
    email = models.CharField(max_length=50)     # 邮箱
    sex = models.CharField(choices=((1, "男"), (2, "女"), (0, "保密")), default=1, null=True, max_length=5)   # 性别
    shopping_grade = models.IntegerField(default=0, null=True)      # 购物积分
    reg_time = models.DateTimeField(default=datetime.now, null=True)   # 注册时间
    birthday = models.CharField(max_length=20, null=True)   # 生日
    user_status = models.IntegerField(default=0, null=True)     # 用户状态 0为正常,1为锁定
    vip_level = models.IntegerField(default=0, null=True)   # 会员等级
    safety_grade = models.IntegerField(default=0, null=True)     # 安全积分
    question1 = models.CharField(max_length=50, null=True)  # 安全问题1
    answer1 = models.CharField(max_length=50, null=True)    # 答案1
    question2 = models.CharField(max_length=50, null=True)  # 安全问题2
    answer2 = models.CharField(max_length=50, null=True)    # 答案2

    class Meta:

        db_table = 'user'
