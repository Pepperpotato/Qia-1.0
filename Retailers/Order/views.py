from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from Goods.models import CommodityCategories,CommodityBrand,Goods
from django.db import connection
# Create your views here.

from .models import *

def home(request):
    temp = loader.get_template('shop/home/home3.html')
    dlb = CommodityCategories.objects.filter(parentid=0) #寻找大类别
    xlb = CommodityCategories.objects.exclude(parentid=0) #寻找小类别
    store = CommodityBrand.objects.all()#寻找品牌
    count = len(dlb)
    print(count)
    list = []
    category = {}
    for num in dlb:
        cursor = connection.cursor()
        cursor.execute("select * from Goods where smallclassesid in (select id from CommodityCategories where parentid ==(select id from CommodityCategories where parentid ==0 limit ))")
        rows = cursor.fetchall()
        print(rows)
    # goods = Goods.objects.all()#
    res = temp.render(context={'dlb':dlb,'xlb':xlb,'store':store})
    return HttpResponse(res)
    # return render(request,'shop/home/home3.html')