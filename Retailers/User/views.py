
import hashlib

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Goods.models import Goods
from Order.models import OrderTwenty, OrderchildTwentyone
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
    all_goods = Goods.objects.all()
    print(all_goods)
    return render(request, 'admin/product_list.html',context={
        'all_goods': all_goods
    })


# 商品详情
def productdetail(request):
    return render(request, 'admin/product_detail.html')


# 订单列表
def orderlist(request):
    with connection.cursor() as cursor:
        cursor.execute("select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]
    print(res)
    return render(request, 'admin/order_list.html', context={
        'res': res
    })


# 删除订单
def delorder(request, id):
    del_order = OrderTwenty.objects.get(id=id)
    del_order.delete()
    return redirect(reverse('admin:orderlist'))


# 订单详情
def orderdetail(request, uid):
    # 当前用户的订单详情 uid为Order主表中的uid
    with connection.cursor() as cursor:
        cursor.execute("select * from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid join orderchild_twentyone t on o.id=t.orderid where o.uid_id=%s",[uid])
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]
    print(res)
    buy_what = OrderchildTwentyone.objects.filter(orderid=res[0].get('id'))

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
            if usertype != 2:
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
                if usertype != 2:
                    current_user.user_type = usertype
                current_user.email = form.cleaned_data.get('email')
                current_user.phone_number = form.cleaned_data.get('phonenumber')
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
    return render(request, 'admin/pageviews.html')


# 销售额统计
def sales(request):
    return render(request, 'admin/sales.html')


def delpayway(request, id):
    payway = Pay_way.objects.filter(id=id)
    payway.delete()
    return redirect(reverse('admin:paylist'))


