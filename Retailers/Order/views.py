import os

from alipay import AliPay
from django.core.serializers import json
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from Goods.models import CommodityCategories, CommodityBrand, Goods, Goodsdetails, CommodityCategoriesTwo, Specification
from Retailers import settings
from User.models import User_address, Express_company

from .models import Mobilecount
from django.db import connection
# Create your views here.
from .models import *

def home(request):
    # # temp = loader.get_template('shop/home/home3.html')
    dlb = CommodityCategories.objects.filter(parentid=0)  # 寻找大类别 3
    xlb = CommodityCategories.objects.exclude(parentid=0)  # 寻找小类别 3
    store = CommodityBrand.objects.all()  # 寻找品牌 2
    price = CommodityCategoriesTwo.objects.all()
    dic = {}
    if request.session.get('username'):
        user = User.objects.get(username=request.session.get('username'))
        shop = ShopcartTwentyfour.objects.filter(uid=user.uid).count()
    else:
        shop = 0

    for lb in dlb:
        for xl in xlb:
            if xl.parentid == lb.id:
                print(xl.categoryname,'33333333')


    for i in dlb:
        list =[]
        list.clear()
        dic[i.id] = list
        commodity = CommodityCategories.objects.filter(parentid=i.id).values('id')
        for j in commodity:

            a = Goods.objects.filter(smallclassesid=j['id'])
            if len(a):
                for num in a:
                    list.append(num)

        list1=list[-6:]

        dic[i.id] = list

    return render(request,'shop/home/home3.html',context={'dlb': dlb,'shopnum':shop ,'xlb': xlb, 'store': store,'dic':dic,'price':price})
    # return HttpResponse(res)
    # return render(request,'shop/home/home3.html')




def intro(request,goodid):
    detail = Goodsdetails.objects.filter(Goodsid=goodid).first()#提供商品详情与展示图
    # print(goodid,'+++++++++++++++++++++++++++++++')
    goods = Goods.objects.filter(gid = goodid).first()#属性主表查商品详情，提供商品名称
    attr = CommodityCategoriesTwo.objects.filter(gid = goodid).first()#属性附表查详情 提供现在价格与历史价格
    # attrnum = CommodityCategoriesTwo.objects.filter(gid=goodid).values('gid').annotate(Count('smallclassesattribute'))
    # attrnum = CommodityCategoriesTwo.objects.filter(gid=goodid).values('smallclassesattribute').distinct().count()#提供小类别个数
    attrnum = CommodityCategoriesTwo.objects.filter(gid=goodid).values('smallclassesattribute').distinct()#提供小类别的详情
    norm = CommodityCategoriesTwo.objects.filter(gid=goodid).values('specification_id').distinct()#与当前商品相关的规格
    inven = CommodityCategoriesTwo.objects.get(gid=goodid,is_show=1)
    normall = Specification.objects.all()#所有规格
    print(norm[0]['specification_id'],normall[0].id)
    # temp = loader.get_template('shop/home/introduction.html')
    if request.session.get('username'):
        user = User.objects.get(username=request.session.get('username'))
        shop = ShopcartTwentyfour.objects.filter(uid=user.uid).count()
    else:
        shop = 0



    print("attrnum",attrnum)
    # res = temp.render(context={'detail': detail, 'inven':inven,'num':1,'goods': goods, 'attr': attr, 'attrnum': attrnum, 'norm': norm, 'normall': normall})
    return render(request,'shop/home/introduction.html',context={'detail': detail,'shopnum':shop, 'inven':inven,'num':1,'goods': goods, 'attr': attr, 'attrnum': attrnum, 'norm': norm, 'normall': normall})


# def purchase(request):
#     if request.method == "POST":
#         fenliang_value = request.POST.get("fenliang_value")
#         kouwei_value = request.POST.get("kouwei_value")
#         goodid = request.POST.get("goodid")
#         count = request.POST.get("count")
#
#         print('+++++++++++++++++++++++')
#         data = {
#
#
#         }
#         return JsonResponse(data)
#     return render(request,'shop/home/pay.html')


def price_change(request):
    if request.method == "POST":
        fenliang_value = request.POST.get("fenliang_value")
        kouwei_value = request.POST.get("kouwei_value")
        goodid = request.POST.get("goodid")
        norm = Specification.objects.get(specification=fenliang_value)

        count = request.POST.get("count")
        fenliang = Specification.objects.get(specification=fenliang_value)
        attr = CommodityCategoriesTwo.objects.get(gid=goodid, specification_id=fenliang.id,smallclassesattribute=kouwei_value)
        price = CommodityCategoriesTwo.objects.get(gid=goodid,smallclassesattribute=kouwei_value,specification_id=norm.id)

        if price:
            total_count = price.inventory

            data = {
                "total_price":price.price,
                "total_count":total_count,
                'goods': attr.id,
                'count': count
            }
            return JsonResponse(data)
        else:
            data = {
                "total_price": '',
                "total_count": 0,
                'goods': attr.id,
                'count': count
            }
            return JsonResponse(data)


def add_cart(request):
    if request.method == "POST":
        user =User.objects.get(username=request.session.get('username'))
        a=request.POST.get('updatanum')
        b=request.POST.get('commodityid')
        commodity = CommodityCategoriesTwo.objects.get(id = int(b))



        shop1 = ShopcartTwentyfour.objects.filter(cid=commodity.id,uid=user.uid).exists()
        if shop1:
            shop = ShopcartTwentyfour.objects.get(cid=commodity.id, uid=user.uid)
            shop.goodscount = shop.goodscount + int(a)
            shop.totalprice = shop.price*int(a)+shop.totalprice
            shop.save()
            num = ShopcartTwentyfour.objects.filter(uid=user.uid).count()
            data = {
            'num':num
            }
            return JsonResponse(data)
        else:

            myshopcart = ShopcartTwentyfour(uid=user.uid, goodscount=int(a), cid=commodity.id,price=commodity.price,totalprice=int(a)*int(commodity.price))
            myshopcart.save()
            num = ShopcartTwentyfour.objects.filter(uid=user.uid).count()
            data = {
            'num': num
            }
            return JsonResponse(data)
    # return render(request,'shop/home/introduction.html')


def pay(request,commodityid,count):
    userid = User.objects.get(username = request.session.get('username')).uid
    address = User_address.objects.filter(uid_id = userid)
    express = Express_company.objects.all()
    if request.session.get('username'):
        user = User.objects.get(username=request.session.get('username'))
        shop = ShopcartTwentyfour.objects.filter(uid=user.uid).count()
    else:
        shop = 0
    commodity = CommodityCategoriesTwo.objects.get(id=commodityid)
    goods = Goods.objects.get(gid=commodity.gid)
    norm = Specification.objects.get(id=commodity.specification_id)
    total_price = int(commodity.price)*int(count)
    total=total_price+10
    if request.method == 'POST':
        username = request.session.get('username')
        user = User.objects.filter(username=username)[0]
        uid = User.objects.filter(username=username)[0].uid
        address = user.user_address_set.all()
        # print(address)
        aid = request.GET.get('aid')
        dell = request.GET.get('del')
        if aid:
            # 取消原有默认地址
            userr = user.user_address_set.filter(default_address=1)[0]
            userr.default_address = 0
            userr.save()
            # 设置新的默认地址
            userr = user.user_address_set.filter(aid=aid)[0]
            userr.default_address = 1
            userr.save()
        if dell:
            useraddress = user.user_address_set.filter(pk=dell)
            useraddress.delete()
            return HttpResponse(json.dumps({'data': '删除成功'}), content_type='application/json')
        if request.method == "POST":
            user_name = request.POST.get('user-name')
            user_phone = request.POST.get('user-phone')
            cmbProvince = request.POST.get('cmbProvince')
            cmbCity = request.POST.get('cmbCity')
            cmbArea = request.POST.get('cmbArea')
            detail_address = request.POST.get('user-intro')
            location = cmbProvince + cmbCity + cmbArea
            print(user_name, user_phone, cmbProvince, cmbCity, cmbArea)
            User_address.objects.create(location=location, detail_address=detail_address, receiver=user_name,
                                        phone_number=user_phone, uid_id=uid)


    return render(request,'shop/home/pay.html',context={'shopnum':shop,'express':express,'address':address,'goods':goods,'commodity':commodity,'count':count,'norm':norm,'total_price':total_price,'total':total})


def addre(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        myad = User_address.objects.get(aid = address)
        reciever = myad.receiver
        phone =myad.phone_number
        location = myad.location
        detail_info = myad.detail_address
        data = {
            'reciever':reciever,
            'phone':phone,
            'location':location,
            'info1':detail_info
        }
        return JsonResponse(data)
    # return render(request,'shop/home/pay.html')


def express(request):
    if request.method == 'POST':
        express_name= request.POST.get('express_name')
        price = request.POST.get('price')
        express = Express_company.objects.get(express_name = express_name)
        ex_id = express.id
        ex_money = express.express_price
        ex_name = express.express_name
        ex_price = int(price)+int(ex_money)
        data = {
            'ex_id':ex_id,
            'ex_money':ex_money,
            'ex_name':ex_name,
            'ex_price':ex_price
        }
        return JsonResponse(data)
    # return render(request, 'shop/home/pay.html')


def commit(request):
    if request.method == 'POST':

        user = User.objects.get(username=request.session.get('username'))
        co = request.POST.get('co')
        ad = request.POST.get('ad')
        ex = request.POST.get('ex')
        print(ex)
        num = request.POST.get('num')
        re = request.POST.get('re')
        commodity = CommodityCategoriesTwo.objects.get(id=co)
        express = Express_company.objects.get(express_name = ex)
        order = OrderTwenty(addressid=ad,uid_id=user.uid,expressbrandid=express.id,remarks=re)
        order.save()
        ord =OrderTwenty.objects.last()
        orderchild = OrderchildTwentyone(orderid=int(ord.id),goodid=int(commodity.gid),goodcount=int(num),goodmoney=int(commodity.price),goodmoneycount=int(num)*int(commodity.price),cid=int(commodity.id))
        orderchild.save()

        ordchild = OrderchildTwentyone.objects.last()
        commod = CommodityCategoriesTwo.objects.get(id=ordchild.cid)
        commod.inventory = int(commod.inventory) - int(num)
        commod.save()

        request.session['bianhao']=ord.id
        request.session['jiage'] = int(num)*int(commodity.price)+express.express_price
        data = {
                'ok':'1',
        }
        return JsonResponse(data)


def cart_commit(request):
    if request.method == 'POST':
        order_id = request.session.get('bianhao')


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

        user = User.objects.get(username=request.session.get('username'))
        co = request.POST.get('co')
        ad = request.POST.get('ad')
        ex = request.POST.get('ex')
        num = request.POST.get('num')
        re = request.POST.get('re')
        commodity = CommodityCategoriesTwo.objects.get(id=co)
        express = Express_company.objects.get(express_name=ex)
        order = OrderTwenty(addressid=ad, uid_id=user.uid, expressbrandid=express.id, remarks=re)
        order.save()
        ord = OrderTwenty.objects.last()
        orderchild = OrderchildTwentyone(orderid=int(ord.id), goodid=int(commodity.gid), goodcount=int(num),
                                         goodmoney=int(commodity.price), goodmoneycount=int(num) * int(commodity.price),
                                         cid=int(commodity.id))
        orderchild.save()

        ordchild = OrderchildTwentyone.objects.last()
        commod = CommodityCategoriesTwo.objects.get(id=ordchild.cid)
        commod.inventory = int(commod.inventory) - int(num)
        commod.save()

        request.session['bianhao'] = ord.id
        request.session['jiage'] = int(num) * int(commodity.price) + express.express_price
        data = {
            'ok': '1',
        }
        return JsonResponse(data)


def shopcart(request):
    if request.session.get('username'):
        user = User.objects.get(username=request.session.get('username'))
        shop = ShopcartTwentyfour.objects.filter(uid=user.uid).count()
    else:
        shop = 0
    user = User.objects.get(username=request.session.get('username'))
    myshop =ShopcartTwentyfour.objects.filter(uid=user.uid)
    goods =Goods.objects.all()
    commodity = CommodityCategoriesTwo.objects.all()
    norm = Specification.objects.all()
    print(shop)
    heji = ShopcartTwentyfour.objects.filter(uid=user.uid).aggregate(Sum('totalprice'))
    # he=heji['totalprice__sum']
    he = 0
    shuliang = 0
    return render(request,'shop/home/shopcart.html',context={'shuliang':shuliang,'heji':he,'shopnum':shop,'myshop':myshop,'goods':goods,'commodity':commodity,'norm':norm})


def check_cart(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        num = request.POST.get('num')
        total_price = request.POST.get('total_price')
        print('+++++++++++',cid,num,total_price)
        user =User.objects.get(username =request.session.get('username') )
        shop=ShopcartTwentyfour.objects.get(uid=user.uid,cid=int(cid))
        shop.goodscount=num
        shop.totalprice=total_price
        shop.save()
        data = {
            'ex_price':'1'
        }
        return JsonResponse(data)


def delete_cart(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        commod = ShopcartTwentyfour.objects.get(cid=int(cid))
        commod.delete()

        data = {
            'ex_price': '1'
        }
        return JsonResponse(data)

list=[]
def cart_pay(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        list.append(int(cid))
        print(list)
        data = {
            'ex_price': '1'
        }
        return JsonResponse(data)


def order_pay(request):

    userid = User.objects.get(username=request.session.get('username')).uid
    if request.session.get('username'):
        user = User.objects.get(username=request.session.get('username'))
        shop = ShopcartTwentyfour.objects.filter(uid=user.uid).count()
    else:
        shop = 0

    print(list, '+++++++++++++++++++++++++++++++++++')
    myshop = ShopcartTwentyfour.objects.filter(uid=userid)
    commod= CommodityCategoriesTwo.objects.all()
    goods =Goods.objects.all()
    norm = Specification.objects.all()
    address = User_address.objects.filter(uid_id=userid)
    express = Express_company.objects.all()
    zongjia=0
    for li in list:
        for shop in myshop:
            if li == shop.cid:
                zongjia+=shop.totalprice

    if request.method == 'POST':
        username = request.session.get('username')
        user = User.objects.filter(username=username)[0]
        uid = User.objects.filter(username=username)[0].uid
        address = user.user_address_set.all()
        # print(address)
        aid = request.GET.get('aid')
        dell = request.GET.get('del')
        if aid:
            # 取消原有默认地址
            userr = user.user_address_set.filter(default_address=1)[0]
            userr.default_address = 0
            userr.save()
            # 设置新的默认地址
            userr = user.user_address_set.filter(aid=aid)[0]
            userr.default_address = 1
            userr.save()
        if dell:
            useraddress = user.user_address_set.filter(pk=dell)
            useraddress.delete()
            return HttpResponse(json.dumps({'data': '删除成功'}), content_type='application/json')
        if request.method == "POST":
            user_name = request.POST.get('user-name')
            user_phone = request.POST.get('user-phone')
            cmbProvince = request.POST.get('cmbProvince')
            cmbCity = request.POST.get('cmbCity')
            cmbArea = request.POST.get('cmbArea')
            detail_address = request.POST.get('user-intro')
            location = cmbProvince + cmbCity + cmbArea
            print(user_name, user_phone, cmbProvince, cmbCity, cmbArea)
            User_address.objects.create(location=location, detail_address=detail_address, receiver=user_name,
                                        phone_number=user_phone, uid_id=uid)

    return render(request, 'shop/home/cart_pay.html',
                  context={'shopnum': shop, 'express': express, 'address': address,'list':list,'myshop':myshop,'commod':commod,'goods':goods,'norm':norm,'zongjia':zongjia
                          })

