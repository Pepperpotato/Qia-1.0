# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CommodityBrandTwo(models.Model):
    brandname = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'commodity_brand_two'


class CommodityCategoriesThirtyThreeFour(models.Model):
    smallclassesid = models.IntegerField()
    smallclassesattribute = models.CharField(max_length=20)
    weightprice = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'commodity_categories_thirty_three_four'


class CommodityCategoriesThree(models.Model):
    parentid = models.IntegerField()
    categoryname = models.CharField(max_length=20)
    picture = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commodity_categories_three'


class ConsultTwentyeight(models.Model):
    questionsort = models.IntegerField()
    details = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'consult_twentyeight'


class CouponsFive(models.Model):
    preferentialthreshold = models.IntegerField()
    preferentialcontent = models.IntegerField()
    expirationtime = models.DateTimeField()
    usingstate = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'coupons_five'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ExpressCompany(models.Model):
    express_name = models.CharField(max_length=10)
    express_price = models.IntegerField()
    express_phonenumber = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'express_company'


class ExpressInfo(models.Model):
    express_id = models.IntegerField()
    status = models.IntegerField()
    updatetime = models.DateTimeField(blank=True, null=True)
    update_info = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'express_info'


class GoodsOne(models.Model):
    gname = models.CharField(unique=True, max_length=50)
    discount = models.CharField(unique=True, max_length=50, blank=True, null=True)
    picture = models.CharField(max_length=1000)
    attribute = models.CharField(max_length=50)
    keyword = models.CharField(max_length=10)
    weightprice = models.IntegerField()
    historicalprices = models.IntegerField()
    inventory = models.IntegerField()
    goodsstate = models.IntegerField()
    brandid = models.IntegerField()
    smallclassesid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'goods_one'


class GoodsdetailsSeven(models.Model):
    goodsid = models.IntegerField(db_column='Goodsid')  # Field name made lowercase.
    productparameters = models.CharField(max_length=200)
    productclass = models.CharField(max_length=200)
    rawmaterial = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=100)
    productspecification = models.CharField(max_length=100)
    shelflife = models.CharField(max_length=50)
    productstandardnumber = models.CharField(max_length=50)
    productionlicensenumber = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'goodsdetails_seven'


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
        managed = False
        db_table = 'order_twenty'


class OrderchildTwentyone(models.Model):
    orderid = models.IntegerField()
    goodid = models.IntegerField()
    goodcount = models.IntegerField()
    goodmoney = models.IntegerField()
    goodmoneycount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orderchild_twentyone'


class ProductevaluationNine(models.Model):
    goodsid = models.IntegerField()
    userid = models.IntegerField()
    ctime = models.DateTimeField()
    rating = models.IntegerField()
    anonymous = models.IntegerField()
    evaluationimage = models.CharField(max_length=100)
    content = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'productevaluation_nine'


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
        managed = False
        db_table = 'return_twentytwo'


class ShopcartTwentyfour(models.Model):
    uid = models.IntegerField()
    goodsid = models.IntegerField()
    goodscount = models.IntegerField()
    goodsprice = models.IntegerField()
    goodsaddtime = models.DateTimeField()
    discount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shopcart_twentyfour'


class StockTwentythree(models.Model):
    remains = models.IntegerField()
    importprice = models.IntegerField()
    outportprice = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock_twentythree'


class SuggestTwentynine(models.Model):
    questionsort = models.IntegerField()
    details = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'suggest_twentynine'


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    realname = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    pay_password = models.CharField(max_length=128)
    user_type = models.IntegerField(blank=True, null=True)
    certificate = models.CharField(max_length=20)
    certificate_id = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    sex = models.CharField(max_length=5, blank=True, null=True)
    shopping_grade = models.IntegerField(blank=True, null=True)
    reg_time = models.DateTimeField(blank=True, null=True)
    birthday = models.CharField(max_length=20, blank=True, null=True)
    user_status = models.IntegerField(blank=True, null=True)
    vip_level = models.IntegerField(blank=True, null=True)
    safety_grade = models.IntegerField(blank=True, null=True)
    question1 = models.CharField(max_length=50, blank=True, null=True)
    answer1 = models.CharField(max_length=50, blank=True, null=True)
    question2 = models.CharField(max_length=50, blank=True, null=True)
    answer2 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserAccount(models.Model):
    pay_password = models.CharField(max_length=128)
    bankcard_id = models.CharField(max_length=50)
    money = models.IntegerField()
    alipay_number = models.CharField(max_length=20, blank=True, null=True)
    wechat_number = models.CharField(max_length=20, blank=True, null=True)
    useroffer_id = models.CharField(max_length=100, blank=True, null=True)
    goodoffer_id = models.CharField(max_length=100, blank=True, null=True)
    integral_id = models.IntegerField(blank=True, null=True)
    uid = models.ForeignKey(User, models.DO_NOTHING)
    used_goodofferid = models.CharField(max_length=100, blank=True, null=True)
    used_userofferid = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_account'


class UserAddress(models.Model):
    aid = models.AutoField(primary_key=True)
    default_address = models.IntegerField()
    location = models.CharField(max_length=20)
    detail_address = models.CharField(max_length=100, blank=True, null=True)
    receiver = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=11)
    uid = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_address'


class UserCollection(models.Model):
    cid = models.AutoField(primary_key=True)
    gid = models.IntegerField(blank=True, null=True)
    collection_time = models.DateTimeField(blank=True, null=True)
    uid = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_collection'


class UserFoot(models.Model):
    fid = models.AutoField(primary_key=True)
    gid = models.IntegerField()
    isdisplay = models.IntegerField()
    uid = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_foot'


class UserGrade(models.Model):
    gid = models.AutoField(primary_key=True)
    change_source = models.CharField(max_length=50)
    change_number = models.IntegerField(blank=True, null=True)
    change_time = models.DateTimeField(blank=True, null=True)
    changed_grade = models.IntegerField(blank=True, null=True)
    growth_value = models.IntegerField(blank=True, null=True)
    uid = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_grade'


class UserNotice(models.Model):
    nid = models.AutoField(primary_key=True)
    picture_path = models.CharField(max_length=200, blank=True, null=True)
    sendtime = models.DateTimeField(blank=True, null=True)
    tag_path = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_notice'


class UserOffer(models.Model):
    offer_content = models.CharField(max_length=200)
    offer_time = models.DateTimeField(blank=True, null=True)
    offer_door = models.IntegerField(blank=True, null=True)
    offer_money = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_offer'

class Ad(models.Model):
    goodsid = models.IntegerField(blank=True, null=True)
    goods_category = models.IntegerField(blank=True,null=True)
    goods_price = models.IntegerField(blank=True,null=True)
    goodspicture = models.CharField(max_length=128,blank=True,null=True)
    detail_b = models.CharField(max_length=128,blank=True,null=True)
    detail_r = models.CharField(max_length=128,blank=True,null=True)

