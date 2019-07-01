from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import *
# Create your views here.

from .models import *

def home(request):
    temp = loader.get_template('shop/home/home3.html')
    dlb = CommodityCategoriesThree.objects.filter(parentid=0) #寻找大类别
    xlb = CommodityCategoriesThree.objects.exclude(parentid=0) #寻找小类别
    store = CommodityBrandTwo.objects.all()
    res = temp.render(context={'dlb':dlb,'xlb':xlb,'store':store})
    return HttpResponse(res)
    # return render(request,'shop/home/home3.html')