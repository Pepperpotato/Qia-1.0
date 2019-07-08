from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from Goods.models import CommodityCategories, CommodityBrand, Goods, Goodsdetails, CommodityCategoriesTwo, Specification
from User.models import User_address

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


    commodity = CommodityCategoriesTwo.objects.get(id=commodityid)
    goods = Goods.objects.get(gid=commodity.gid)
    norm = Specification.objects.get(id=commodity.specification_id)
    total_price = int(commodity.price)*int(count)
    total=total_price+10
    return render(request,'shop/home/pay.html',context={'address':address,'goods':goods,'commodity':commodity,'count':count,'norm':norm,'total_price':total_price,'total':total})