
import hashlib

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from User.models import User, Express_company, Pay_way, User_account


def add(request):
    user = User()
    # user(username='admin', password=hashlib.sha1('admin123'.encode('utf8')).hexdigest(),
    #      pay_password=hashlib.sha1('admin123'.encode('utf8')).hexdigest(), user_type=1, certificate='身份证',
    #      certificate_id='000000000000000000', phone_number='00000000000', email='0000@126.com')
    user.username = 'admin'
    user.password = hashlib.sha1('admin123'.encode('utf8')).hexdigest()
    user.pay_password = hashlib.sha1('admin123'.encode('utf8')).hexdigest()
    user.user_type = 1
    user.certificate = '身份证'
    user.certificate_id = '000000000000000000'
    user.phone_number = '00000000000'
    user.email = '0000@126.com'
    user.save()

    return HttpResponse('增加数据')


# 首页
def index(request):
    admin = request.session.get('username')
    admin_info = User.objects.filter(username=admin)

    return render(request, 'admin/index.html', context={
        'admin_info': admin_info
    })


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = hashlib.sha1(password.encode('utf8')).hexdigest()
        if User.objects.filter(username=username) and User.objects.values('password').filter(username=username)[0].get('password') == password:
            request.session['username'] = username
            return redirect(reverse('admin:index'))

    return render(request, 'admin/login.html')


# 登出
def logout(request):
    request.session.clear()
    return redirect(reverse('admin:login'))


# 商品列表
def productlist(request):
    return render(request, 'admin/product_list.html')


# 商品详情
def productdetail(request):
    return render(request, 'admin/product_detail.html')


# 订单列表
def orderlist(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from order_twenty o join user_address a on o.addressid=a.aid ")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]
    print(res)
    return render(request, 'admin/order_list.html', context={
        'res': res
    })


# 订单详情
def orderdetail(request):
    return render(request, 'admin/order_detail.html')


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
    current_user = User.objects.filter(uid=uid)
    return render(request, 'admin/user_detail.html', context={
        'current_user': current_user[0]
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
    return render(request, 'admin/pageviews.html')


# 销售额统计
def sales(request):
    return render(request, 'admin/sales.html')


def delpayway(request, id):
    payway = Pay_way.objects.filter(id=id)
    payway.delete()
    return redirect(reverse('admin:paylist'))

