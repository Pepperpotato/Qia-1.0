from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from Goods.models import CommodityCategories,CommodityBrand,Goods
from .models import Mobilecount
from django.db import connection
# Create your views here.

from .models import *

def home(request):
    temp = loader.get_template('shop/home/home3.html')
    dlb = CommodityCategories.objects.filter(parentid=0) #寻找大类别
    xlb = CommodityCategories.objects.exclude(parentid=0) #寻找小类别
    store = CommodityBrand.objects.all()#寻找品牌
    pub = xlb[0].goods_set.all()

    res = temp.render(context={'dlb':dlb,'xlb':xlb,'store':store})
    return HttpResponse(res)
    # return render(request,'shop/home/home3.html')


