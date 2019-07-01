
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class ConsultTwentyeight(models.Model):
    questionsort = models.IntegerField()
    details = models.CharField(max_length=256)

    class Meta:
        db_table = 'consult_twentyeight'




class OrderTwenty(models.Model):
    uid = models.IntegerField()
    ordertime = models.DateTimeField()
    address = models.CharField(max_length=128)
    expressbrand = models.CharField(max_length=128)
    paywayid = models.IntegerField()
    integral = models.IntegerField()
    phone = models.CharField(max_length=128)
    orderstatus = models.IntegerField()
    getgoodstime = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'order_twenty'


class OrderchildTwentyone(models.Model):
    orderid = models.IntegerField()
    goodid = models.IntegerField()
    goodcount = models.IntegerField()
    goodmoney = models.IntegerField()
    goodmoneycount = models.IntegerField()

    class Meta:

        db_table = 'orderchild_twentyone'




class ReturnTwentytwo(models.Model):
    orderid = models.IntegerField()
    clientreturntime = models.DateTimeField()
    retailersreturntime = models.DateTimeField(blank=True, null=True)
    bankdotime = models.DateTimeField(blank=True, null=True)
    returnoktime = models.DateTimeField(blank=True, null=True)
    returntype = models.IntegerField(blank=True, null=True)
    returnreason = models.CharField(max_length=128, blank=True, null=True)
    returnmoney = models.IntegerField(blank=True, null=True)
    returndetails = models.CharField(max_length=256, blank=True, null=True)
    picturepath1 = models.CharField(max_length=256, blank=True, null=True)
    picturepath2 = models.CharField(max_length=256, blank=True, null=True)
    picturepath3 = models.CharField(max_length=256, blank=True, null=True)

    class Meta:

        db_table = 'return_twentytwo'


class ShopcartTwentyfour(models.Model):
    uid = models.IntegerField()
    goodsid = models.IntegerField()
    goodscount = models.IntegerField()
    goodsprice = models.IntegerField()
    goodsaddtime = models.DateTimeField()
    discount = models.IntegerField()

    class Meta:

        db_table = 'shopcart_twentyfour'


class StockTwentythree(models.Model):
    remains = models.IntegerField()
    importprice = models.IntegerField()
    outportprice = models.IntegerField()

    class Meta:
        db_table = 'stock_twentythree'


class SuggestTwentynine(models.Model):
    questionsort = models.IntegerField()
    details = models.CharField(max_length=256)

    class Meta:

        db_table = 'suggest_twentynine'




class Activity(models.Model):
    picture = models.CharField(max_length=128)
    sort = models.IntegerField()

    class Meta:
        db_table = 'activity_head_thirty'

class Todayrecommend(models.Model):
    id = models.AutoField(primary_key=True)
    goodsid = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'today_recommend_thirtyone'





