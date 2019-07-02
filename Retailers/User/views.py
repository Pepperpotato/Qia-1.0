
import hashlib

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from User.models import User, Express_company


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
    return render(request, 'admin/order_list.html')


# 订单详情
def orderdetail(request):
    return render(request, 'admin/order_detail.html')


# 会员列表
def userlist(request):
    return render(request, 'admin/user_list.html')


# 会员详情
def userdetail(request):
    return render(request, 'admin/user_detail.html')


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
    return render(request, 'admin/pay_list.html')


# 浏览量
def pageviews(request):
    return render(request, 'admin/pageviews.html')


# 销售额统计
def sales(request):
    return render(request, 'admin/sales.html')


