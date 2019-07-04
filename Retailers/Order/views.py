from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse


from Goods.models import CommodityCategories, CommodityBrand, Goods

from .models import Mobilecount
from django.db import connection
# Create your views here.

from .models import *


def home(request):
    temp = loader.get_template('shop/home/home3.html')
    dlb = CommodityCategories.objects.filter(parentid=0)  # 寻找大类别 3
    xlb = CommodityCategories.objects.exclude(parentid=0)  # 寻找小类别 3
    store = CommodityBrand.objects.all()  # 寻找品牌 2
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
                    list.append(num.gid)
        dic[i.id] = list
        print(dic)


    res = temp.render(context={'dlb': dlb, 'xlb': xlb, 'store': store,'dic':dic})
    return HttpResponse(res)
    # return render(request,'shop/home/home3.html')
