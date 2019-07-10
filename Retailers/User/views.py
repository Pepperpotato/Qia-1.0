import time
import hashlib
import json
import os
from datetime import datetime
from random import randint

from alipay import AliPay
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from Goods.models import Goods, CommodityBrand, CommodityCategories, Specification, CommodityCategoriesTwo, \
    Goodsdetails, uploadpic
from Order.models import OrderTwenty, OrderchildTwentyone, Mobilecount
from Retailers import settings
from Retailers.settings import NUMOFPAGE
from User.forms import ChangeForm
from User.models import User, Express_company, Pay_way, User_account, User_grade


def add(request):
    user = User()
    # user(username='admin', password=hashlib.sha1('admin123'.encode('utf8')).hexdigest(),
    #      pay_password=hashlib.sha1('admin123'.encode('utf8')).hexdigest(), user_type=1, certificate='身份证',
    #      certificate_id='000000000000000000', phone_number='00000000000', email='0000@126.com')
    user.username = 'admin1'
    user.password = hashlib.sha1('admin123'.encode('utf8')).hexdigest()
    user.pay_password = hashlib.sha1('admin123'.encode('utf8')).hexdigest()
    user.user_type = 0
    user.certificate = '身份证'
    user.certificate_id = '000000000000000000'
    user.phone_number = '00000000000'
    user.email = '0000@126.com'
    # user.save()

    return HttpResponse('增加数据')


# 首页
def index(request):
    admin = request.session.get('username')

    admin_info = User.objects.filter(username=admin)

    user_count = User.objects.count()

    month = datetime.now().month
    lastmonth = month - 1
    # 本月订单量
    order_count = OrderTwenty.objects.filter(ordertime__month=month).count()
    # 上月订单量
    lastorder_count = OrderTwenty.objects.filter(ordertime__month=lastmonth).count()

    # 库存不足产品
    with connection.cursor() as cursor:
        cursor.execute("select c.gid,g.gname,specification,inventory from goodsone g join commodity_categories_two_four c on g.gid=c.gid join specification s on s.id=c.specification_id where inventory<50")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]

    with connection.cursor() as cursor:
        cursor.execute("select * from orderchild_twentyone t join goodsone g on t.goodid=g.gid join order_twenty o on o.id=t.orderid")
    columns = [col[0] for col in cursor.description]
    res1 = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'admin/index.html', context={
        'admin_info': admin_info,
        'admin': admin,
        'user_count': user_count,
        'order_count': order_count,
        'lastorder_count': lastorder_count,
        'res': res
    })


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = hashlib.sha1(password.encode('utf8')).hexdigest()
        if User.objects.filter(username=username) and User.objects.values('password').filter(username=username)[0].get('password') == password and User.objects.values('user_type').filter(username=username)[0].get('user_type') == 1:
            request.session['username'] = username
            return redirect(reverse('admin:index'))

    return render(request, 'admin/login.html')


# 登出
def logout(request):
    request.session.clear()
    return redirect(reverse('admin:login'))


# 商品列表
def productlist(request, page=1):
    with connection.cursor() as cursor:
        cursor.execute("select * from goodsone g join commodity_categories_two_four c on g.gid=c.gid join specification s on s.id=c.specification_id")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(res, NUMOFPAGE)
    page = int(page)
    pagination = paginator.page(page)

    if paginator.num_pages> 5:
        #如果当前页码-5小于0
        if page - 2 <= 0:
            customRange = range(1,6)
        elif page + 2 > paginator.num_pages:
            customRange = range(paginator.num_pages-4,paginator.num_pages+1)
        else:
            customRange = range(page-2,page+2)
    else: #页码总数小于10
        customRange = paginator.page_range
    return render(request, 'admin/product_list.html', context={
        'res': pagination.object_list,
        'pagerange': customRange,
        'pagination': pagination,

    })


# 添加已有类别商品
def addgood(request):
    if request.method == 'POST':
        # 品牌id
        brand = int(request.POST.get('brand'))
        # 小版块id
        category = int(request.POST.get('category'))
        # 商品名称
        goodname = request.POST.get('goodname')
        # 关键字'
        keyword = request.POST.get('keyword')
        # 图片
        file = request.FILES.get('picture')
        pathpic = uploadpic(file)

        newgood = Goods()
        newgood.gname = goodname
        if pathpic:
            newgood.picture = pathpic
        newgood.keyword = keyword
        newgood.brandid = brand
        newgood.smallclassesid = category
        newgood.save()
        return redirect(reverse('admin:productlist'))

    commodity_brand = CommodityBrand.objects.all()
    commodity_categories = CommodityCategories.objects.filter(parentid__gt=0)
    with connection.cursor() as cursor:
        cursor.execute("select * from commodity_categories_three c join goodsone g on g.smallclassesid=c.id join commodity_brand_two b on b.id=g.brandid ")
    columns = [col[0] for col in cursor.description]
    all_goods = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'admin/add_good.html', context={
        'commodity_brand': commodity_brand,
        'commodity_categories': commodity_categories,
        'all_goods': all_goods
    })

# 修改商品
def altergood(request):
    if request.is_ajax():
        if request.is_ajax():
            good_id = request.POST.get('gid')
            brandid = request.POST.get('brandid')
            categoryid = request.FILES.get('categoryid')
            gname = request.POST.get('gname')
            keyword = request.POST.get('keyword')
            picture = request.FILES.get('picture')
            new_picture = uploadpic(picture)

            current_good = Goods.objects.get(pk=int(good_id))
            current_good.brandid = brandid
            current_good.smallclassesid = categoryid
            current_good.gname = gname
            current_good.keyword = keyword
            if new_picture:
                current_good.picture = new_picture
            current_good.save()
            return JsonResponse({'code': 1, 'msg': '修改以保存'})

# 删除商品
def delgood(request):
    if request.is_ajax():
        current_id = request.POST.get('gid')
        current_good = Goods.objects.get(pk=int(current_id))
        # current_good.delete()
        print(current_good.gname)
        return JsonResponse({'code': 1, 'data': '已删除'})


# 添加新的商品大类别
@csrf_exempt
def addbigcategory(request):
    if request.method == 'POST':
        newbigcategory = request.POST.get('newbigcategory')
        check_category = CommodityCategories.objects.filter(categoryname=newbigcategory)
        if check_category:
            return JsonResponse({'code': 0, 'data': '大类别已存在，请重新输入'})

        category = CommodityCategories()

        file = request.FILES.get('newpicture')
        if file:
            # 文件路径
            path = os.path.join(settings.MEDIA_ROOT, file.name)

            # 文件类型过滤
            ext = os.path.splitext(file.name)
            if len(ext) < 1 or not ext[1] in settings.ALLOWED_FILEEXTS:
                return JsonResponse({'code': 2, 'data': '不允许的图片格式'})

            pathh = path.split('Retailers/static')

            goodphoto = pathh[1]
            category.picture = goodphoto
            # 创建新文件
            with open(path, 'wb') as fp:
                # 如果文件超过2.5M,则分块读写
                if file.multiple_chunks():
                    for block1 in file.chunks():
                        fp.write(block1)
                else:
                    fp.write(file.read())

        category.categoryname = newbigcategory
        category.parentid = 0
        category.save()
        return JsonResponse({'code': 1, 'data': '新大类别已添加'})
    all_bigcategory = CommodityCategories.objects.filter(parentid=0)
    return render(request, 'admin/add_bigcategory.html', context={
        'all_bigcategory': all_bigcategory
    })

# 修改大类别
def alterbigcategory(request):
    if request.is_ajax():
        category_id = request.POST.get('cid')
        name = request.POST.get('name')
        picture = request.FILES.get('newpicture')
        new_picture = uploadpic(picture)
        current_bigcategory = CommodityCategories.objects.get(pk=int(category_id))
        current_bigcategory.categoryname = name
        if new_picture:
            current_bigcategory.picture = new_picture
        current_bigcategory.save()
        return JsonResponse({'code': 1, 'msg': '修改以保存'})

        # return redirect(reverse('admin:addattrbute'))


# 删除大类别
def delbigcategory(request):
    if request.is_ajax():
        current_id = request.POST.get('bid')
        current_bicategory = CommodityCategories.objects.get(pk=int(current_id))
        # current_bicategory.delete()
        return JsonResponse({'code': 1, 'data': '已删除'})


# 添加商品小类别
def addsmallcategory(request):
    if request.is_ajax():
        smallcategory = request.POST.get('smallcategory')
        bigcategoryid = request.POST.get('bigcategoryid')

        if CommodityCategories.objects.filter(parentid=int(bigcategoryid),categoryname=smallcategory):
            return JsonResponse({'code': 0, 'data': '新商品小类别已存在，请重新填写'})

        category = CommodityCategories()
        category.categoryname = smallcategory
        category.parentid = int(bigcategoryid)
        category.save()
        return JsonResponse({'code': 1, 'data': '新商品小类别已储存'})
    res = CommodityCategories.objects.filter(parentid=0)
    res1 = CommodityCategories.objects.filter(parentid__gt=0)
    return render(request, 'admin/add_smallcategory.html', context={
        'res': res,
        'res1': res1
    })


#  修改小类别
def altersmallcategory(request):
    if request.is_ajax():
        category_id = request.POST.get('cid')
        name = request.POST.get('name')
        current_smaillcategory = CommodityCategories.objects.get(pk=int(category_id))
        current_smaillcategory.categoryname = name
        current_smaillcategory.save()
        return JsonResponse({'code': 1, 'msg': '修改以保存'})


# 删除小类别
def delsmallcategory(request):
    if request.is_ajax():
        current_id = request.POST.get('sid')
        current_smallategory = CommodityCategories.objects.get(pk=int(current_id))
        # current_smallategory.delete()
        return JsonResponse({'code': 1, 'data': '已删除'})


# 添加商品品牌
def addband(request):
    if request.method == 'POST':
        bandname = request.POST.get('newband')
        newband = CommodityBrand()
        newband.brandname = bandname
        newband.save()
        return redirect(reverse('admin:productlist'))

    all_brand = CommodityBrand.objects.all()
    return render(request, 'admin/add_band.html',context={
        'all_brand': all_brand
    })


# 修改品牌
def alterband(request):
    if request.is_ajax():
        brand_id = request.POST.get('bid')
        name = request.POST.get('name')
        current_brand = CommodityBrand.objects.get(pk=int(brand_id))
        current_brand.brandname = name
        current_brand.save()
        return JsonResponse({'code': 1, 'msg': '修改已保存'})


#  删除品牌
def delband(request):
    if request.is_ajax():
        current_id = request.POST.get('bid')
        current_brand = CommodityBrand.objects.get(pk=int(current_id))
        # current_brand.delete()
        print(current_brand.brandname)
        return JsonResponse({'code': 1, 'data': '已删除'})



@csrf_exempt
# 添加库存
def addinventory(request):

    if request.is_ajax():
        categoryid = request.POST.get('categoryid')
        if categoryid:
            # 小类别id 松子
            request.session['categoryid'] = categoryid
        with connection.cursor() as cursor:
            cursor.execute("select gname,gid from commodity_categories_three c join goodsone g on g.smallclassesid=c.id where parentid>0 and  smallclassesid=%s", [categoryid])
        columns = [col[0] for col in cursor.description]
        res1 = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return JsonResponse(res1, safe=False)

    commodity_categories = CommodityCategories.objects.filter(parentid__gt=0)
    commodity_brand = CommodityBrand.objects.all()
    return render(request, 'admin/add_inventory.html', context={
        'commodity_brand': commodity_brand,
        'commodity_categories': commodity_categories
    })


@csrf_exempt
def addinventory1(request):
    if request.is_ajax():
        brandid = request.POST.get('brandid')
        if brandid:
            # 品牌id 良品铺子
            request.session['brandid'] = brandid
        cid = int(request.session['categoryid'])
        with connection.cursor() as cursor:
            cursor.execute("select distinct smallclassesattribute from goodsone g join commodity_categories_two_four c on g.gid=c.gid where c.smallclassesid=%s", [cid])
        columns = [col[0] for col in cursor.description]
        res = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return JsonResponse(res, safe=False)

@csrf_exempt
def addinventory2(request):
    if request.is_ajax():
        section = request.POST.get('section')
        if section:
            # 属性  奶油
            request.session['section'] = section
        cid = request.session.get('categoryid')
        with connection.cursor() as cursor:
            cursor.execute("select s.id,specification from commodity_categories_two_four c join specification s on c.specification_id=s.id where c.smallclassesid=%s and c.smallclassesattribute=%s", [cid,section])
        columns = [col[0] for col in cursor.description]
        res = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return JsonResponse(res, safe=False)

@csrf_exempt
def addinventory3(request):
    if request.is_ajax():
        specificationid = request.POST.get('specificationid')
        if specificationid:
            request.session['specificationid'] = specificationid
        cid = request.session.get('categoryid')
        section = request.session.get('section')
        with connection.cursor() as cursor:
            cursor.execute("select inventory from commodity_categories_two_four where smallclassesid=%s and smallclassesattribute=%s and specification_id=%s", [cid, section, specificationid])
        columns = [col[0] for col in cursor.description]
        res = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return JsonResponse(res, safe=False)


def addinventory4(request):
    if request.method == 'POST':
        inventory = request.POST.get('add')

        cid = request.session.get('categoryid')
        section = request.session.get('section')
        specificationid = request.session.get('specificationid')
        current_id = CommodityCategoriesTwo.objects.values('id').filter(smallclassesid=cid, smallclassesattribute=section, specification_id=specificationid)
        id = current_id[0]['id']
        current_good = CommodityCategoriesTwo.objects.get(pk=id)
        current_good.inventory += int(inventory)
        current_good.save()
        return redirect(reverse('admin:productlist'))


# 添加商品属性
def addattrbute(request):

    if request.is_ajax():

        categoryid = request.POST.get('categoryid')
        if categoryid:
            # 小类别id 松子
            request.session['categoryid'] = categoryid
        with connection.cursor() as cursor:
            cursor.execute("select gname,gid from commodity_categories_three c join goodsone g on g.smallclassesid=c.id where parentid>0 and  smallclassesid=%s",[categoryid])
        columns = [col[0] for col in cursor.description]
        res1 = [dict(zip(columns, row)) for row in cursor.fetchall()]
        if res1:
            return JsonResponse(res1, safe=False)

        brandid = request.POST.get('brandid')
        if brandid:
            # 品牌id 良品铺子
            request.session['brandid'] = brandid
        cid = int(request.session['categoryid'])
        with connection.cursor() as cursor:
            cursor.execute("select distinct smallclassesattribute from goodsone g join commodity_categories_two_four c on g.gid=c.gid where c.smallclassesid=%s",[cid])
        columns = [col[0] for col in cursor.description]
        res = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return JsonResponse(res, safe=False)

    if request.method == 'POST':
        print(111111)
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        goodid = request.POST.get('goodid')
        specification = request.POST.get('specification')
        unit = request.POST.get('unit')
        attrbute = request.POST.get('attrbute')
        price = request.POST.get('price')
        ishow = request.POST.get('ishow')
        stockprice = request.POST.get('stockprice')
        inventory = request.POST.get('inventory')

        new_atrr = CommodityCategoriesTwo()
        new_specification = Specification()

        new_atrr.smallclassesid = category
        new_atrr.brandid = brand
        new_specification.specification = specification
        new_specification.save()
        specification_id = new_specification.id
        new_atrr.specification_id = specification_id
        new_atrr.gid = goodid
        new_atrr.unit = unit
        new_atrr.smallclassesattribute = attrbute
        new_atrr.price = int(price)
        new_atrr.is_show = int(ishow)
        new_atrr.stockprice = int(stockprice)
        new_atrr.inventory = int(inventory)
        new_atrr.save()
        return redirect(reverse('admin:productlist'))

    commodity_categories = CommodityCategories.objects.filter(parentid__gt=0)
    commodity_brand = CommodityBrand.objects.all()
    all_good = Goods.objects.all()
    all_specification = Specification.objects.all()
    with connection.cursor() as cursor:
        cursor.execute("select f.id,c.categoryname,b.brandname,g.gname,f.is_show,f.smallclassesattribute,s.specification,f.unit,f.price,f.stockprice,f.inventory from commodity_categories_two_four f join commodity_categories_three c on f.smallclassesid=c.id join goodsone g on g.gid=f.gid join commodity_brand_two b on b.id=f.brandid join specification s on f.specification_id=s.id")
    columns = [col[0] for col in cursor.description]
    good_attr = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'admin/add_attrbute.html', context={
        'commodity_brand': commodity_brand,
        'commodity_categories': commodity_categories,
        'all_goods': all_good,
        'good_attr': good_attr,
        'all_specification': all_specification
    })


# 修改属性
def alterattrbute(request):
    if request.is_ajax():
        aid = request.POST.get('attrid')
        categoryid = request.POST.get('categoryid')
        brandid = request.POST.get('brandid')
        goodid = request.POST.get('goodid')
        specificationid = request.POST.get('specificationid')
        unit = request.POST.get('unit')
        attr = request.POST.get('attr')
        price = request.POST.get('price')
        is_show = request.POST.get('is_show')
        stockprice = request.POST.get('stockprice')
        inventory = request.POST.get('inventory')

        current_attr = CommodityCategoriesTwo.objects.get(pk=int(aid))
        current_attr.smallclassesid = categoryid
        current_attr.brandid = brandid
        current_attr.gid = goodid
        current_attr.smallclassesattribute = attr
        current_attr.specification_id = specificationid
        current_attr.unit = unit
        if is_show:
            current_attr.is_show = int(is_show)
        if price:
            current_attr.price = int(price)
            current_attr.historicalprices = int(price) + 20
        if stockprice:
            current_attr.stockprice = int(stockprice)
        if inventory:
            current_attr.inventory = int(inventory)
        current_attr.save()
        return JsonResponse({'code': 1, 'msg': '修改已保存'})


def delattrbute(request):
    if request.is_ajax():
        current_id = request.POST.get('aid')
        current_attr = CommodityCategoriesTwo.objects.get(pk=int(current_id))
        # current_attr.delete()
        print(current_attr.smallclassesattribute)
        return JsonResponse({'code': 1, 'data': '已删除'})




def addgoodetail(request):
    if request.method == 'POST':
        gid = request.POST.get('good')
        good_detail = Goodsdetails()
        good_detail.Goodsid = gid
        good_detail.productclass = request.POST.get('productclass')
        good_detail.rawmaterial = request.POST.get('rawmaterial')
        good_detail.origin = request.POST.get('origin')
        good_detail.ingredients = request.POST.get('ingredients')
        good_detail.productspecification = request.POST.get('productspecification')
        good_detail.shelflife = request.POST.get('shelflife')
        good_detail.productstandardnumber = request.POST.get('productstandardnumber')
        good_detail.productionlicensenumber = request.POST.get('productionlicensenumber')
        good_detail.storeway = request.POST.get('storeway')
        good_detail.eatway = request.POST.get('eatway')

        # 图片一上传
        picture1 = request.FILES.get('picture1')
        pathpic1 = uploadpic(picture1)
        if pathpic1:
            good_detail.picture1 = pathpic1

        mpicture1 = request.FILES.get('mpicture1')
        pathmpic1 = uploadpic(mpicture1)
        if pathmpic1:
            good_detail.mpicture1 = pathmpic1

        spicture1 = request.FILES.get('spicture1')
        pathspic1 = uploadpic(spicture1)
        if pathspic1:
            good_detail.spicture1 = pathspic1

        # 图片二上传
        picture2 = request.FILES.get('picture2')
        pathpic2 = uploadpic(picture2)
        if pathpic2:
            good_detail.picture2 = pathpic2

        mpicture2 = request.FILES.get('mpicture2')
        pathmpic2 = uploadpic(mpicture2)
        if pathmpic2:
            good_detail.mpicture2 = pathmpic2

        spicture2 = request.FILES.get('spicture2')
        pathspic2 = uploadpic(spicture2)
        if pathspic2:
            good_detail.spicture2 = pathspic2

        # 图片三上传
        picture3 = request.FILES.get('picture3')
        pathpic3 = uploadpic(picture3)
        if pathpic3:
            good_detail.picture3 = pathpic3

        mpicture3 = request.FILES.get('mpicture3')
        pathmpic3 = uploadpic(mpicture3)
        if pathmpic3:
            good_detail.mpicture3 = pathmpic3

        spicture3 = request.FILES.get('spicture3')
        pathspic3 = uploadpic(spicture3)
        if pathspic3:
            good_detail.spicture3 = pathspic3

        # 图片四上传
        picture4 = request.FILES.get('picture4')
        pathpic4 = uploadpic(picture4)
        if pathpic4:
            good_detail.picture4 = pathpic4

        # 图片五上传
        picture5 = request.FILES.get('picture5')
        pathpic5 = uploadpic(picture5)
        if pathpic5:
            good_detail.picture5 = pathpic5

        # 图片六上传
        picture6 = request.FILES.get('picture6')
        pathpic6 = uploadpic(picture6)
        if pathpic6:
            good_detail.picture6 = pathpic6

        # 图片七上传
        picture7 = request.FILES.get('picture7')
        pathpic7 = uploadpic(picture7)
        if pathpic7:
            good_detail.picture7 = pathpic7

        good_detail.save()

        return redirect(reverse('admin:productlist'))

    all_good = Goods.objects.all()
    return render(request, 'admin/add_goodetail.html',context={

        'all_good': all_good
    })


# 订单列表
def orderlist(request, page=1):

    with connection.cursor() as cursor:
        cursor.execute("select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(res, NUMOFPAGE)
    page = int(page)
    pagination = paginator.page(page)

    if paginator.num_pages > 5:
        # 如果当前页码-5小于0
        if page - 2 <= 0:
            customRange = range(1, 6)
        elif page + 2 > paginator.num_pages:
            customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            customRange = range(page - 2, page + 2)
    else:  # 页码总数小于10
        customRange = paginator.page_range
    return render(request, 'admin/order_list.html', context={
        'res': pagination.object_list,
        'pagerange': customRange,
        'pagination': pagination,
    })


# 删除订单
def delorder(request, id):
    del_order = OrderTwenty.objects.get(id=id)
    # del_order.delete()
    return redirect(reverse('admin:orderlist'))


# 订单详情
def orderdetail(request, id):
    # 根据订单id获取用户id
    uid = OrderTwenty.objects.values('uid').filter(id=id)
    uid = uid[0]['uid']

    with connection.cursor() as cursor:
        cursor.execute("select * from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid join orderchild_twentyone t on o.id=t.orderid where o.id=%s", [id])
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]


    with connection.cursor() as cursor:
        cursor.execute("select * from orderchild_twentyone t join goodsone g on t.goodid=g.gid where t.orderid=%s", [id])
    columns = [col[0] for col in cursor.description]
    buy_what = [dict(zip(columns, row)) for row in cursor.fetchall()]


    with connection.cursor() as cursor:
        cursor.execute("select sum(goodmoneycount) as sum1 from orderchild_twentyone t join goodsone g on t.goodid=g.gid where t.orderid=%s", [id])
    columns = [col[0] for col in cursor.description]
    sum1 = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'admin/order_detail.html', context={
        'res': res[0],
        'buy_what': buy_what,
        'sum1': sum1[0]['sum1']
    })


# 会员列表
def userlist(request, page=1):
    all_user = User.objects.all()
    all_account = User_account.objects.all()
    with connection.cursor() as cursor:
        cursor.execute("select * from user u right join user_account a on u.uid=a.uid")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(res, NUMOFPAGE)
    page = int(page)
    pagination = paginator.page(page)

    if paginator.num_pages> 5:
        #如果当前页码-5小于0
        if page - 2 <= 0:
            customRange = range(1,6)
        elif page + 2 > paginator.num_pages:
            customRange = range(paginator.num_pages-4,paginator.num_pages+1)
        else:
            customRange = range(page-2,page+2)
    else: #页码总数小于10
        customRange = paginator.page_range

    return render(request, 'admin/user_list.html', context={
        'all_user': all_user,
        'all_account': all_account,
        'pagerange': customRange,
        'pagination': pagination,
        'res': pagination.object_list
    })


# 删除用户
def deluser(request, uid):
    deluser = User.objects.filter(uid=uid)
    # deluser.delete()
    return redirect(reverse('admin:userlist'))


# 会员详情
def userdetail(request, uid):
    # 当前用户所有信息
    current_user = User.objects.filter(uid=uid)[0]
    current_grade = User_grade.objects.filter(uid=uid)
    current_account = User_account.objects.filter(user_id=uid)

    if request.method == 'POST':
        sid = User.objects.values('uid').filter(username=request.session.get('username'))[0]['uid']

        if sid != int(uid):
            current_user.email = request.POST.get('email')
            current_user.phone_number = request.POST.get('phonenumber')
            usertype = request.POST.get('usertype')
            current_user.user_type = usertype
            current_user.save()
            return redirect(reverse('admin:userlist'))
        else:
            form = ChangeForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                newpassword = form.cleaned_data.get('newpassword')
                newpassword = hashlib.sha1(newpassword.encode('utf8')).hexdigest()
                if newpassword != 'da39a3ee5e6b4b0d3255bfef95601890afd80709':
                    current_user.password = newpassword
                usertype = request.POST.get('usertype')
                current_user.user_type = usertype
                current_user.email = form.cleaned_data.get('email')
                current_user.phone_number = form.cleaned_data.get('phonenumber')
                file = request.FILES.get('picture')

                current_user.save()
                return render(request, 'admin/login.html')

            return render(request, 'admin/user_detail.html', context={
                'current_user': current_user,
                'current_grade': current_grade[0],
                'current_account': current_account[0],
                'form': form
            })

    else:

        return render(request, 'admin/user_detail.html', context={
            'current_user': current_user,
            'current_grade': current_grade[0],
            'current_account': current_account[0]
        })


# 会员等级
def userrank(request):
    return render(request, 'admin/user_rank.html')


# 会员账户
def useraccount(request):
    return render(request, 'admin/user_account.html')


# 站点设置
def setting(request):
    return render(request, 'admin/setting.html')


# 物流列表
def expresslist(request):
    express = Express_company.objects.all()

    return render(request, 'admin/express_list.html', context={
        'express': express
    })


def delexpress(request, id):
    express = Express_company.objects.filter(id=id)
    # express.delete()
    return redirect(reverse('admin:expresslist'))


# 支付列表
def paylist(request):
    payway = Pay_way.objects.all()
    return render(request, 'admin/pay_list.html', context={
        'payways': payway
    })


# 浏览量
def pageviews(request):
    res = Mobilecount.objects.values('view', 'time').order_by('-time')[:7]
    day7 = res[0]
    day7view = day7['view']
    day7time = day7['time']

    day6 = res[1]
    day6view = day6['view']
    day6time = day6['time']

    day5 = res[2]
    day5view = day5['view']
    day5time = day5['time']

    day4 = res[3]
    day4view = day4['view']
    day4time = day4['time']
    #
    day3 = res[4]
    day3view = day3['view']
    day3time = day3['time']
    #
    day2 = res[5]
    day2view = day2['view']
    day2time = day2['time']
    #
    day1 = res[6]
    day1view = day1['view']
    day1time = day1['time']
    return render(request, 'admin/pageviews.html', context={
        'day7view': day7view,
        'day7time': day7time,
        'day6view': day6view,
        'day6time': day6time,
        'day5view': day5view,
        'day5time': day5time,
        'day4view': day4view,
        'day4time': day4time,
        'day3view': day3view,
        'day3time': day3time,
        'day2view': day2view,
        'day2time': day2time,
        'day1view': day1view,
        'day1time': day1time
    })


# 销售额统计
def sales(request):
    return render(request, 'admin/sales.html')


def delpayway(request, id):
    payway = Pay_way.objects.filter(id=id)
    # payway.delete()
    return redirect(reverse('admin:paylist'))


# 按条件选择订单
def choiceorder(request, page=1):
    if request.method == 'POST':
        way = request.POST.get('choice')
        if way == 'waitpay':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 0")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })
        elif way == 'waitsend':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 1")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })
        elif way == 'waitget':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 2")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })
        elif way == 'waitsay':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 3 or o.orderstatus = 4")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })

@csrf_exempt
# class OrderPayView(View):
#     """订单支付"""
#     def post(self, request):

def pay(request):
        print(1111111)
        order_id = request.session.get('bianhao')
        # order_id = 1
        # if not order_id:
        #     return JsonResponse({"errno": 1, "error_msg": "参数不完整"})
        # try:
        #     # order = OrderTwenty.objects.get(id=order_id, user=user, pay_method=3, order_status=1)
        #     order = OrderTwenty.objects.get(id=order_id, paywayid=1, orderstatus=0)
        # except OrderTwenty.DoesNotExist:
        #     return JsonResponse({"errno": 2, "error_msg": "无效订单"})

        alipay = AliPay(
            appid="2016101100659250",  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(settings.BASE_DIR, 'User/keys/app_private_key.pem'),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'User/keys/alipay_public_key.pem'),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False

        )
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # total_pay = order.total_price + order.transit_price
        # total_pay = request.session.get('total_price')
        total_pay = request.session.get('jiage')
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,  # 订单编号
            total_amount=str(total_pay),
            subject="辛姐的小吃铺<%s>" % order_id,
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        # 构造用户跳转的支付链接地址
        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string

        return JsonResponse({"errno": "ok", "pay_url": pay_url})


def test(request):
    return render(request, 'admin/test.html')


def checkpay(request):
    print(22222222222)
    order_id = request.session.get("bianhao")
    order = OrderTwenty.objects.get(pk=int(order_id))
    alipay = AliPay(
        appid="2016101100659250",  # 应用id
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, 'User/keys/app_private_key.pem'),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=os.path.join(settings.BASE_DIR, 'User/keys/alipay_public_key.pem'),
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False

    )

    while True:
        response = alipay.api_alipay_trade_query(order_id)
        # 从支付宝返回的响应数据中获取code以及trade_status
        code = response.get("code")
        trade_status = response.get("trade_status")

        if code == '10000' and trade_status == "TRADE_SUCCESS":
            # 表示成功
            # 获取支付宝交易号
            # trade_no = response.get("trade_no")
            # 更新订单状态
            # order.trade_no = trade_no
            order.orderstatus = 1  # 待评价
            order.integral = int(request.session.get('jiage'))
            order.save()
            # 返回正确响应
            return JsonResponse({"errno": "ok", "error_msg": "交易成功"})
        elif code == '40004' or (code == '10000' and trade_status == "WAIT_BUYER_PAY"):
            # 业务处理失败以及等待买家付款
            import time
            time.sleep(5)  # 休眠5秒再次调用支付宝交易查询接口，重新获取状态码以及支付状态信息
            continue
        else:
            return JsonResponse({"errno": 4, "error_msg": "交易失败"})


