
from django.db import models

# Create your models here.


# 商品品牌表2
from django.utils import timezone


class CommodityBrand(models.Model):
    id = models.AutoField(primary_key=True)  #id
    brandname = models.CharField(max_length=20)  #品牌名称

    class Meta:

        db_table = 'commodity_brand_two'


# 商品类别表3
class CommodityCategories(models.Model):
    id = models.AutoField(primary_key=True)          #id
    parentid = models.IntegerField()           #父板块id
    categoryname = models.CharField(max_length=20)  #板块名称
  # 图片
    picture=models.CharField(max_length=128,blank=True,null=True)

    class Meta:

        db_table = 'commodity_categories_three'


# 商品表1
class Goods(models.Model):
    gid = models.AutoField(primary_key=True)  #商品id
    gname = models.CharField(unique=True, max_length=50) #商品名称
    discount = models.CharField( default=0,max_length=50) #优惠方式
    picture = models.CharField(max_length=1000)  #图片
    attributeid = models.IntegerField(default=1)   #商品属性id
    keyword = models.CharField(max_length=128)    #搜索关键字
    goodsstate = models.IntegerField(default=0)               #商品状态已上线0已下线1
    brandid = models.IntegerField()             #品牌id
    smallclassesid = models.IntegerField()         #小类别id
    unit = models.CharField(max_length=20, default='件')
    classid=models.ForeignKey(CommodityCategories,default=None ,db_column='id')
    class Meta:
        db_table = 'goodsone'


#  商品类别表4（属性）
class CommodityCategoriesTwo(models.Model):
    id=models.AutoField(primary_key=True)  #id
    smallclassesid = models.IntegerField()  # 小类别id
    smallclassesattribute = models.CharField(max_length=20) #小类别属性
    specification_id = models.IntegerField()
    brandid = models.IntegerField(null=True)
    price = models.IntegerField()  # 对应价格
    historicalprices = models.IntegerField()     # 历史价格
    inventory = models.IntegerField(default=0)   # 库存

    class Meta:
        db_table = 'commodity_categories_two_four'


class Specification(models.Model):
    specification = models.CharField(max_length=100)

    class Meta:
        db_table = 'specification'


# 优惠券表5
class  Coupons(models.Model):
    id = models.AutoField(primary_key=True)  # id
    preferentialthreshold=models.IntegerField()  #优惠门槛
    preferentialcontent=models.IntegerField()  #优惠内容（展示满100减10）
    expirationtime = models.DateTimeField()  #优惠券到期时间
    usingstate=models.IntegerField(default=0)  #优惠状态0代表未使用1代表已使用
    class Meta:
        db_table = 'coupons_five'

# 商品详情表7
class Goodsdetails(models.Model):
    id = models.AutoField(primary_key=True)  # id
    Goodsid=models.IntegerField()  #商品id
    productclass=models.CharField(max_length=216) #产品类别
    rawmaterial=models.CharField(max_length=216) #原料产地
    origin=models.CharField(max_length=216) #产地
    ingredients=models.CharField(max_length=216) #配料
    productspecification=models.CharField(max_length=216) #产品规格
    shelflife=models.CharField(max_length=216) #保质期
    productstandardnumber=models.CharField(max_length=216) #产品标准号
    productionlicensenumber=models.CharField(max_length=216) #生产许可证编号
    storeway=models.CharField(max_length=216) #储存方法
    eatway=models.CharField(max_length=216) #食用方法
    picture1=models.CharField(max_length=128, null=True) #图片路径
    spicture1 = models.CharField(max_length=128, null=True)
    mpicture1 = models.CharField(max_length=128, null=True)
    picture2=models.CharField(max_length=128, null=True) #图片路径
    spicture2 = models.CharField(max_length=128, null=True)
    mpicture2 = models.CharField(max_length=128, null=True)
    picture3=models.CharField(max_length=128, null=True) #图片路径
    spicture3 = models.CharField(max_length=128,null=True)
    mpicture3 = models.CharField(max_length=128,null=True)
    picture4=models.CharField(max_length=128,null=True) #图片路径
    picture5=models.CharField(max_length=128,null=True) #图片路径
    picture6=models.CharField(max_length=128,null=True) #图片路径
    picture7=models.CharField(max_length=128,null=True) #图片路径
    class Meta:
        db_table = 'goodsdetails_seven'

# 商品评价表9
class Productevaluation(models.Model):
    id=models.AutoField(primary_key=True)   #评价id
    goodsid=models.IntegerField()  #商品id
    userid=models.IntegerField()  #用户id
    ctime=models.DateTimeField(default=timezone.now)  #评论时间(默认是当前时间)
    rating = models.IntegerField()  # 评价等级
    anonymous=models.IntegerField()  #是否匿名 0匿名1不匿名
    evaluationimage=models.CharField(max_length=100) # 评价图片
    content=models.CharField(max_length=200)  #评价内容

    class Meta:
        db_table='productevaluation_nine'


