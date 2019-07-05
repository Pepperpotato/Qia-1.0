
import hashlib
import os
from datetime import datetime
from random import randint

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Goods.models import Goods, CommodityBrand, CommodityCategories
from Order.models import OrderTwenty, OrderchildTwentyone, Mobilecount
from Retailers import settings
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
    print(admin)
    admin_info = User.objects.filter(username=admin)

    return render(request, 'admin/index.html', context={
        'admin_info': admin_info,
        'admin': admin
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
def productlist(request):
    all_goods = Goods.objects.all()
    print(all_goods)
    return render(request, 'admin/product_list.html',context={
        'all_goods': all_goods
    })


# 商品详情
def productdetail(request):
    # 商品品牌
    commodity_brand = CommodityBrand.objects.all()
    commodity_categories = CommodityCategories.objects.all()

    return render(request, 'admin/product_detail.html', context={
        'commodity_brand': commodity_brand,
        'commodity_categories': commodity_categories
    })



def addgood(request):
    gname = request.POST.get('gname')
    print(gname)

    return redirect(reverse('admin:productdetail'))



# 订单列表
def orderlist(request):

    with connection.cursor() as cursor:
        cursor.execute("select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'admin/order_list.html', context={
        'res': res
    })


# 删除订单
def delorder(request, id):
    del_order = OrderTwenty.objects.get(id=id)
    del_order.delete()
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
    print(res)
    # buy_what = OrderchildTwentyone.objects.filter(orderid=id)
    # print(111111,buy_what)
    with connection.cursor() as cursor:
        cursor.execute("select * from orderchild_twentyone t join goodsone g on t.goodid=g.gid where t.orderid=%s", [id])
    columns = [col[0] for col in cursor.description]
    buy_what = [dict(zip(columns, row)) for row in cursor.fetchall()]
    # print(222222,res1)

    return render(request, 'admin/order_detail.html', context={
        'res': res[0],
        'buy_what': buy_what
    })


# 会员列表
def userlist(request):
    all_user = User.objects.all()
    all_account = User_account.objects.all()
    # account = User_account.objects.all()
    # user_info = account.user
    # print(user_info)
    return render(request, 'admin/user_list.html', context={
        'all_user': all_user,
        'all_account': all_account
    })


# 删除用户
def deluser(request, uid):
    deluser = User.objects.filter(uid=uid)
    deluser.delete()
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
    express.delete()
    return redirect(reverse('admin:expresslist'))


# 支付列表
def paylist(request):
    payway = Pay_way.objects.all()
    return render(request, 'admin/pay_list.html', context={
        'payways': payway
    })


# 浏览量
def pageviews(request):
    view_count = Mobilecount.objects.all()
    print(view_count)
    return render(request, 'admin/pageviews.html', context={
        'view_count': view_count
    })


# 销售额统计
def sales(request):
    return render(request, 'admin/sales.html')


def delpayway(request, id):
    payway = Pay_way.objects.filter(id=id)
    payway.delete()
    return redirect(reverse('admin:paylist'))


def choiceorder(request):
    if request.method == 'POST':
        way = request.POST.get('choice')
        if way == 'waitpay':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 0")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]
            print(2222, res)
            return render(request, 'admin/order_list.html', context={
                'res': res
            })
        elif way == 'waitsend':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 1")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return render(request, 'admin/order_list.html', context={
                'res': res
            })
        elif way == 'waitget':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 2")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return render(request, 'admin/order_list.html', context={
                'res': res
            })
        elif way == 'waitsay':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 3 or o.orderstatus = 4")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return render(request, 'admin/order_list.html', context={
                'res': res
            })
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return render(request, 'admin/order_list.html', context={
                'res': res
            })