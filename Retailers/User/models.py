from django.db import models

# Create your models here.
from datetime import datetime

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


# 用户积分表
class User_grade(models.Model):
    gid = models.AutoField(primary_key=True)    # 用户积分表id
    uid = models.ForeignKey('User', models.CASCADE)     # 用户id
    change_source = models.CharField(max_length=50)     # 积分变更来源
    change_number = models.IntegerField(null=True)     # 积分变更数值
    change_time = models.DateTimeField(default=datetime.now, null=True)     # 变更时间
    changed_grade = models.IntegerField(null=True)     # 变更后积分
    growth_value = models.IntegerField(null=True)      # 会员成长值

    class Meta:
        db_table = 'user_grade'


# 用户收货地址表
class User_address(models.Model):
    aid = models.AutoField(primary_key=True)    # 地址id
    uid = models.ForeignKey('User', models.CASCADE)     # 用户id
    default_address = models.IntegerField(default=0)    # 是否默认地址,0为否，1为是
    location = models.CharField(max_length=20)  # 所在地
    detail_address = models.CharField(max_length=100, null=True)    # 默认地址
    receiver = models.CharField(max_length=10, null=True)   # 收货人
    phone_number = models.CharField(max_length=11)      # 手机号

    class Meta:
        db_table = 'user_address'


# 用户足迹表
class User_foot(models.Model):
    fid = models.AutoField(primary_key=True)    # 足迹表id
    uid = models.ForeignKey('User', models.CASCADE)     # 用户id
    gid = models.IntegerField(null=False)   # 商品id
    isdisplay = models.IntegerField(default=1)  # 是否显示,1为是,0为否

    class Meta:
        db_table = 'user_foot'


# 用户收藏表
class User_collection(models.Model):
    cid = models.AutoField(primary_key=True)    # 通知表id
    uid = models.ForeignKey('User', models.CASCADE)     # 用户id
    gid = models.IntegerField(null=True)
    collection_time = models.DateTimeField(default=datetime.now, null=True)    # 收藏时间

    class Meta:
        db_table = 'user_collection'


# 用户通知表
class User_notice(models.Model):
    nid = models.AutoField(primary_key=True)    # 通知表id
    picture_path = models.CharField(max_length=200, null=True)    # 活动图片路径
    sendtime = models.DateTimeField(default=datetime.now, null=True)    # 发送时间
    tag_path = models.CharField(max_length=200, null=True)  # 活动内容标签路径

    class Meta:
        db_table = 'user_notice'


# 用户账户信息表
class User_account(models.Model):
    uid = models.ForeignKey('User', models.CASCADE)     # 用户id
    pay_password = models.CharField(max_length=128)     # 支付密码
    bankcard_id = models.CharField(max_length=50)   # 银行卡号
    money = models.IntegerField(default=0)      # 账户余额
    alipay_number = models.CharField(max_length=20, null=True)  # 支付宝账号
    wechat_number = models.CharField(max_length=20, null=True)  # 微信账号
    useroffer_id = models.CharField(max_length=100, null=True)   # 用户优惠券id
    goodoffer_id = models.CharField(max_length=100, null=True)   # 商品优惠券id
    used_userofferid = models.CharField(max_length=100, null=True)  # 已使用用户优惠券id
    used_goodofferid = models.CharField(max_length=100, null=True)  # 已使用商品优惠券id
    integral_id = models.IntegerField(null=True)    # 积分表id

    class Meta:
        db_table = 'user_account'


# 用户优惠券表
class User_offer(models.Model):
    offer_content = models.CharField(max_length=200)    # 优惠内容描述
    offer_time = models.DateTimeField(null=True)    # 优惠时间
    # status = models.IntegerField(default=0)   # 使用状态 0为未使用，1为使用
    offer_door = models.IntegerField(default=100, null=True)   # 优惠门槛
    offer_money = models.IntegerField(default=10)   # 优惠金额

    class Meta:
        db_table = 'user_offer'


# 物流品牌表
class Express_company(models.Model):
    express_name = models.CharField(max_length=10)  # 物流品牌名称
    express_price = models.IntegerField(default=8)  # 物流品牌价格
    express_phonenumber = models.CharField(max_length=20)   # 物流电话
    express_info = models.CharField(max_length=200)     # 物流品牌介绍
    express_photo = models.CharField(max_length=500)    # 物流品牌品牌图片路径

    class Meta:
        db_table = 'express_company'


# 物流信息表
class Express_info(models.Model):
    express_id = models.IntegerField(default=1)     # 物流品牌id
    status = models.IntegerField(default=0)     # 物流状态 0未发货，1已发货，2已签收
    updatetime = models.DateTimeField(default=datetime.now, null=True)  # 更新时间
    update_info = models.CharField(max_length=100, null=True)   # 更新信息
    order_id = models.IntegerField(null=True)   # 订单id

    class Meta:
        db_table = 'express_info'


# 支付方式表
class Pay_way(models.Model):
    pay_name = models.CharField(max_length=50)  # 支付方式名称
    pay_info = models.CharField(max_length=200)     # 支付方式简介
    pay_photo = models.CharField(max_length=500)    # 支付方式图片路径

    class Meta:
        db_table = 'pay_way'
