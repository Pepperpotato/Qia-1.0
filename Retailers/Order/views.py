from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from Goods.models import CommodityCategories, CommodityBrand, Goods, Goodsdetails, CommodityCategoriesTwo, Specification

from .models import Mobilecount
from django.db import connection
# Create your views here.
from .models import *

def home(request):
    temp = loader.get_template('shop/home/home3.html')
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

    res = temp.render(context={'dlb': dlb, 'xlb': xlb, 'store': store,'dic':dic,'price':price})
    return HttpResponse(res)
    # return render(request,'shop/home/home3.html')




def intro(request,dlbid,xlbid,goodid):
    detail = Goodsdetails.objects.filter(Goodsid=goodid).first()#提供商品详情与展示图
    # print(goodid,'+++++++++++++++++++++++++++++++')
    goods = Goods.objects.filter(gid = goodid).first()#属性主表查商品详情，提供商品名称
    attr = CommodityCategoriesTwo.objects.filter(gid = goodid).first()#属性附表查详情 提供现在价格与历史价格
    # attrnum = CommodityCategoriesTwo.objects.filter(gid=goodid).values('gid').annotate(Count('smallclassesattribute'))
    # attrnum = CommodityCategoriesTwo.objects.filter(gid=goodid).values('smallclassesattribute').distinct().count()#提供小类别个数
    attrnum = CommodityCategoriesTwo.objects.filter(gid=goodid).values('smallclassesattribute').distinct()#提供小类别的详情
    norm = CommodityCategoriesTwo.objects.filter(gid=goodid).values('specification_id').distinct()#与当前商品相关的规格
    normall = Specification.objects.all()#所有规格
    print(norm[0]['specification_id'],normall[0].id)
    temp = loader.get_template('shop/home/introduction.html')
    res = temp.render(context={'detail':detail,'goods':goods,'attr':attr,'attrnum':attrnum,'norm':norm,'normall':normall})
    if request.POST:
        we = request.POST
        print(we,'+++++++++++++++++++++++++++++++++++++')
    return HttpResponse(res)


def verf(request,goodid):
    province = request.GET.get('province')
    city = request.GET.get('city')
    block = request.GET.get('block')
    print(province,city,block,'++++++++++++++++++++++')
    return HttpResponse('ok')