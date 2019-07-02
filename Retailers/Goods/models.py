
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
    id = models.AutoField(primary_key=True)  #商品id
    gname = models.CharField(unique=True, max_length=50) #商品名称
    discount = models.CharField(unique=True, max_length=50) #优惠方式
    picture = models.CharField(max_length=1000)  #图片
    attribute = models.CharField(max_length=50)   #商品属性
    keyword = models.CharField(max_length=10)    #搜索关键字
    weightprice = models.IntegerField()             # 权重价格
    historicalprices = models.IntegerField()      #历史价格
    inventory = models.IntegerField()            # 库存
    goodsstate = models.IntegerField(default=0)               #商品状态已上线0已下线1
    brandid = models.IntegerField()             #品牌id
    smallclassesid = models.IntegerField()         #小类别id

    class Meta:

        db_table = 'goods_one'




#  商品类别表4（属性）
class CommodityCategoriesTwo(models.Model):
    id=models.AutoField(primary_key=True)  #id
    smallclassesid = models.IntegerField()  # 小类别id
    smallclassesattribute = models.CharField(max_length=20) #小类别属性
    weightprice = models.IntegerField() #对应价格


    class Meta:

        db_table = 'commodity_categories_two_four'



# 优惠券表5
class  coupons(models.Model):
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
    productparameters=models.CharField(max_length=200) #产品参数
    productclass=models.CharField(max_length=200) #产品类别
    rawmaterial=models.CharField(max_length=100) #原料产地
    origin=models.CharField(max_length=100) #产地
    ingredients=models.CharField(max_length=100) #配料
    productspecification=models.CharField(max_length=100) #产品规格
    shelflife=models.CharField(max_length=50) #保质期
    productstandardnumber=models.CharField(max_length=50) #产品标准号
    productionlicensenumber=models.CharField(max_length=50) #生产许可证编号
    picture1=models.CharField(max_length=128,null=True) #图片路径
    picture2=models.CharField(max_length=128,null=True) #图片路径
    picture3=models.CharField(max_length=128,null=True) #图片路径
    picture4=models.CharField(max_length=128,null=True) #图片路径
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


