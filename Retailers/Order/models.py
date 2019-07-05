
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import datetime

from django.db import models

from User.models import User


class ConsultTwentyeight(models.Model):
    questionsort = models.IntegerField() #问题分类
    details = models.CharField(max_length=256) #问题描述

    class Meta:
        db_table = 'consult_twentyeight'




class OrderTwenty(models.Model):
    uid = models.ForeignKey(User,models.CASCADE)

    ordertime = models.DateTimeField(null=True)#下单时间
    addressid = models.IntegerField(null=True)#收货地址id
    expressbrandid = models.IntegerField(default=1,null=True)#物流品牌id
    paywayid = models.IntegerField(null=True)#支付id
    integral = models.IntegerField(null=True)#获得积分
    orderstatus = models.IntegerField(null=True)#订单状态 0~4
    # 0     没付钱
    # 1   已付款未发货
    # 2   已发货未收货
    # 3   已收货未评价
    # 4   评价了，交易完成
    getgoodstime = models.DateTimeField(blank=True, null=True) #收货时间
    remarks= models.CharField(max_length=100, null=True, default='--') #购买备注

    class Meta:

        db_table = 'order_twenty'


class OrderchildTwentyone(models.Model):
    orderid = models.IntegerField(null=True) #订单id
    goodid = models.IntegerField(null=True) #商品id
    goodcount = models.IntegerField(null=True) #商品数量
    goodmoney = models.IntegerField(null=True) #商品单价
    goodmoneycount = models.IntegerField(null=True) #合计

    class Meta:

        db_table = 'orderchild_twentyone'




class ReturnTwentytwo(models.Model):
    orderid = models.IntegerField() #订单id
    clientreturntime = models.DateTimeField() #买家退货时间
    retailersreturntime = models.DateTimeField(blank=True, null=True) #卖家退款时间
    bankdotime = models.DateTimeField(blank=True, null=True) #银行受理时间
    returnoktime = models.DateTimeField(blank=True, null=True) #退款成功实践
    returntype = models.IntegerField(blank=True, null=True) #退款类型
    returnreason = models.CharField(max_length=128, blank=True, null=True) #退款原因
    returnmoney = models.IntegerField(blank=True, null=True) #退款金额
    returndetails = models.CharField(max_length=256, blank=True, null=True) #退款说明
    picturepath1 = models.CharField(max_length=256, blank=True, null=True) #图片路径1/2/3
    picturepath2 = models.CharField(max_length=256, blank=True, null=True)
    picturepath3 = models.CharField(max_length=256, blank=True, null=True)

    class Meta:

        db_table = 'return_twentytwo'


class ShopcartTwentyfour(models.Model):
    uid = models.IntegerField() #用户id
    goodsid = models.IntegerField() #商品id
    goodscount = models.IntegerField() #加入购物车商品数量
    goodsprice = models.IntegerField()#商品价格
    goodsaddtime = models.DateTimeField()#加入购物车时间
    discount = models.IntegerField()#优惠种类

    class Meta:

        db_table = 'shopcart_twentyfour'


class StockTwentythree(models.Model):
    remains = models.IntegerField() #剩余数量
    importprice = models.IntegerField() #进货价格
    outportprice = models.IntegerField() #出售价格

    class Meta:
        db_table = 'stock_twentythree'


class SuggestTwentynine(models.Model):
    questionsort = models.IntegerField() #问题分类
    details = models.CharField(max_length=256) #问题描述

    class Meta:

        db_table = 'suggest_twentynine'


class Activity(models.Model):
    picture = models.CharField(max_length=128) #图片
    sort = models.IntegerField() #0是轮播1是活动

    class Meta:
        db_table = 'activity_head_thirty'

class Todayrecommend(models.Model):
    id = models.AutoField(primary_key=True)
    goodsid = models.IntegerField(blank=True, null=True) #商品id

    class Meta:
        db_table = 'today_recommend_thirtyone'



class Mobilecount(models.Model):
    view = models.PositiveIntegerField(default=0) #次数
    time = models.DateTimeField(auto_now_add=True) #日期

