from django.core.serializers import json
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from Goods.models import CommodityCategories, CommodityBrand, Goods, Goodsdetails, CommodityCategoriesTwo, Specification
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
        list.sort(reverse=True)
        list1=list[:6]
        dic[i.id] = list1

    return render(request,'shop/home/home3.html',context={'dlb': dlb, 'xlb': xlb, 'store': store,'dic':dic,'price':price})
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


    print("attrnum",attrnum)
    # res = temp.render(context={'detail': detail, 'inven':inven,'num':1,'goods': goods, 'attr': attr, 'attrnum': attrnum, 'norm': norm, 'normall': normall})
    return render(request,'shop/home/introduction.html',context={'detail': detail, 'inven':inven,'num':1,'goods': goods, 'attr': attr, 'attrnum': attrnum, 'norm': norm, 'normall': normall})


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


# def add_cart(request):
#     if request.method == "POST":
#         fenliang_value = request.POST.get("fenliang_value")
#         kouwei_value = request.POST.get("kouwei_value")
#         goodid = request.POST.get("goodid")
#         count = request.POST.get("count")
#         data = {
#             'emm':count
#         }
#         return JsonResponse(data)


def pay(request,commodityid,count):
    userid = User.objects.get(username = request.session.get('username')).uid
    address = User_address.objects.filter(uid_id = userid)
    express = Express_company.objects.all()

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


    return render(request,'shop/home/pay.html',context={'express':express,'address':address,'goods':goods,'commodity':commodity,'count':count,'norm':norm,'total_price':total_price,'total':total})


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
    return render(request,'shop/home/pay.html')


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
    return render(request, 'shop/home/pay.html')


def commit(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.session.get('username'))
        co = request.POST.get('co')
        ad = request.POST.get('ad')
        ex = request.POST.get('ex')
        num = request.POST.get('num')
        re = request.POST.get('re')
        commodity = CommodityCategoriesTwo.objects.get(id=co)
        express = Express_company.objects.get(express_name = ex)
        order = OrderTwenty(addressid=ad,uid_id=user.uid,expressbrandid=express.id,remarks=re)
        order.save()
        ord =OrderTwenty.objects.last()
        orderchild = OrderchildTwentyone(orderid=int(ord.id),goodid=int(commodity.gid),goodcount=int(num),goodmoney=int(commodity.price),goodmoneycount=int(num)*int(commodity.price),cid=int(commodity.id))
        orderchild.save()
        request.session['bianhao']=ord.id
        request.session['jiage'] = int(num)*int(commodity.price)
        data = {
                'ok':'1'
        }
        return JsonResponse(data)
    return render(request, 'shop/home/pay.html')