
import hashlib
import json
import os
from datetime import datetime
from random import randint

from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Goods.models import Goods, CommodityBrand, CommodityCategories, Specification, CommodityCategoriesTwo
from Order.models import OrderTwenty, OrderchildTwentyone, Mobilecount
from Retailers import settings
from Retailers.settings import NUMOFPAGE

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
def productlist(request, page=1):
    with connection.cursor() as cursor:
        cursor.execute("select * from goodsone g join commodity_categories_two_four c on g.gid=c.gid join specification s on s.id=c.specification_id")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(res, NUMOFPAGE)
    page = int(page)
    pagination = paginator.page(page)

    if paginator.num_pages> 5:
        #如果当前页码-5小于0
        if page - 2 <= 0:
            customRange = range(1,6)
        elif page + 2 > paginator.num_pages:
            customRange = range(paginator.num_pages-4,paginator.num_pages+1)
        else:
            customRange = range(page-2,page+2)
    else: #页码总数小于10
        customRange = paginator.page_range
    return render(request, 'admin/product_list.html', context={
        'res': pagination.object_list,
        'pagerange': customRange,
        'pagination': pagination,

    })


# 添加新商品
def addnewgood(request):

    # 商品品牌
    commodity_brand = CommodityBrand.objects.all()
    commodity_categories = CommodityCategories.objects.all()

    return render(request, 'admin/addnewgood.html', context={
        'commodity_brand': commodity_brand,
        'commodity_categories': commodity_categories
    })


# 添加已有类别商品
def addgood(request):
    if request.method == 'POST':
        # 品牌id
        brand = int(request.POST.get('brand'))
        # 小版块id
        category = int(request.POST.get('category'))
        # 商品名称
        goodname = request.POST.get('goodname')
        # 类型
        newsection = request.POST.get('newsection')
        # 规格
        format = request.POST.get('format')
        # 单价
        price = int(request.POST.get('price'))
        # 单位
        unit = request.POST.get('unit')
        # 库存
        inventory = int(request.POST.get('inventory'))
        # 关键字'
        keyword = request.POST.get('keyword')
        # 图片
        file = request.FILES.get('picture')
        if file:

            # 文件路径
            path = os.path.join(settings.MEDIA_ROOT, file.name)
            print(path)
            # 文件类型过滤
            ext = os.path.splitext(file.name)
            if len(ext) < 1 or not ext[1] in settings.ALLOWED_FILEEXTS:
                return redirect(reverse('admin:addgood'))

            pathh = path.split('Retailers/static')
            print(2222,pathh[1])
            goodphoto = pathh[1]

            # 创建新文件
            with open(path, 'wb') as fp:
                # 如果文件超过2.5M,则分块读写
                if file.multiple_chunks():
                    for block1 in file.chunks():
                        fp.write(block1)
                else:
                    fp.write(file.read())

        newgood = Goods()
        newgood.gname = goodname
        newgood.picture = goodphoto
        newgood.keyword = keyword
        newgood.brandid = brand
        newgood.smallclassesid = category
        newgood.save()
        gid = newgood.gid

        newspecification = Specification()
        newspecification.specification = format
        newspecification.save()
        sid = newspecification.id

        newcategory = CommodityCategoriesTwo()
        newcategory.smallclassesid = category
        newcategory.smallclassesattribute = newsection
        newcategory.specification_id = sid
        newcategory.brandid = brand
        newcategory.price = price
        newcategory.inventory = inventory
        newcategory.unit = unit
        newcategory.gid = gid
        newcategory.save()

        return redirect(reverse('admin:productlist'))

    commodity_brand = CommodityBrand.objects.all()
    commodity_categories = CommodityCategories.objects.filter(parentid__gt=0)

    return render(request, 'admin/add_good.html', context={
        'commodity_brand': commodity_brand,
        'commodity_categories': commodity_categories
    })


# 添加商品品牌
def addband(request):
    if request.method == 'POST':
        bandname = request.POST.get('newband')
        newband = CommodityBrand()
        newband.brandname = bandname
        newband.save()
        return redirect(reverse('admin:productlist'))

    return render(request, 'admin/add_band.html')


@csrf_exempt
# 添加库存
def addinventory(request):
    if request.is_ajax():
        brandid = request.POST.get('brandid')
        if brandid:
            request.session['brandid'] = brandid
        with connection.cursor() as cursor:
            cursor.execute("select categoryname,id as categoryid from commodity_categories_three c join goodsone g on g.smallclassesid=c.id where parentid>0 and brandid=%s", [brandid])
        columns = [col[0] for col in cursor.description]
        res = [dict(zip(columns, row)) for row in cursor.fetchall()]

        print(request.POST)
        bid = request.session.get('brandid')

        categoryid = request.POST.get('categoryid')
        if categoryid:
            request.session['categoryid'] = categoryid
        with connection.cursor() as cursor:
            cursor.execute("select gname,gid from commodity_categories_three c join goodsone g on g.smallclassesid=c.id where parentid>0 and brandid=%s and smallclassesid=%s", [bid, categoryid])
        columns = [col[0] for col in cursor.description]
        res1 = [dict(zip(columns, row)) for row in cursor.fetchall()]


        if res1:
            return JsonResponse(res1, safe=False)
        else:
            return JsonResponse(res, safe=False)
    commodity_brand = CommodityBrand.objects.all()
    commodity_categories = CommodityCategories.objects.filter(parentid__gt=0)

    return render(request, 'admin/add_inventory.html',context={
        'commodity_brand': commodity_brand,
        'commodity_categories': commodity_categories
    })

@csrf_exempt
def addinventory1(request):

    if request.is_ajax():
        gid = request.POST.get('gid')
        attr = CommodityCategoriesTwo.objects.filter(gid=gid)
        res = json.dumps(list(attr.values()))
        return JsonResponse(res, safe=False)


# 订单列表
def orderlist(request, page=1):

    with connection.cursor() as cursor:
        cursor.execute("select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(res, NUMOFPAGE)
    page = int(page)
    pagination = paginator.page(page)

    if paginator.num_pages > 5:
        # 如果当前页码-5小于0
        if page - 2 <= 0:
            customRange = range(1, 6)
        elif page + 2 > paginator.num_pages:
            customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            customRange = range(page - 2, page + 2)
    else:  # 页码总数小于10
        customRange = paginator.page_range
    return render(request, 'admin/order_list.html', context={
        'res': pagination.object_list,
        'pagerange': customRange,
        'pagination': pagination,
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
def userlist(request, page=1):
    all_user = User.objects.all()
    all_account = User_account.objects.all()
    with connection.cursor() as cursor:
        cursor.execute("select * from user u right join user_account a on u.uid=a.uid")
    columns = [col[0] for col in cursor.description]
    res = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(res, NUMOFPAGE)
    page = int(page)
    pagination = paginator.page(page)

    if paginator.num_pages> 5:
        #如果当前页码-5小于0
        if page - 2 <= 0:
            customRange = range(1,6)
        elif page + 2 > paginator.num_pages:
            customRange = range(paginator.num_pages-4,paginator.num_pages+1)
        else:
            customRange = range(page-2,page+2)
    else: #页码总数小于10
        customRange = paginator.page_range

    # account = User_account.objects.all()
    # user_info = account.user
    # print(user_info)
    return render(request, 'admin/user_list.html', context={
        'all_user': all_user,
        'all_account': all_account,
        'pagerange': customRange,
        'pagination': pagination,
        'res': pagination.object_list
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
    res = Mobilecount.objects.values('view', 'time').order_by('-time')[:7]
    day7 = res[0]
    day7view = day7['view']
    day7time = day7['time']

    day6 = res[1]
    day6view = day6['view']
    day6time = day6['time']

    day5 = res[2]
    day5view = day5['view']
    day5time = day5['time']

    day4 = res[3]
    day4view = day4['view']
    day4time = day4['time']
    #
    # day3 = res[4]
    # day3view = day3['view']
    # day3time = day3['time']
    #
    # day2 = res[5]
    # day2view = day2['view']
    # day2time = day2['time']
    #
    # day1 = res[6]
    # day1view = day1['view']
    # day1time = day1['time']
    return render(request, 'admin/pageviews.html', context={
        'day7view': day7view,
        'day7time': day7time,
        'day6view': day6view,
        'day6time': day6time,
        'day5view': day5view,
        'day5time': day5time,
        'day4view': day4view,
        'day4time': day4time,
        # 'day3view': day3view,
        # 'day3time': day3time,
        # 'day2view': day2view,
        # 'day2time': day2time,
        # 'day1view': day1view,
        # 'day1time': day1time
    })


# 销售额统计
def sales(request):
    return render(request, 'admin/sales.html')


def delpayway(request, id):
    payway = Pay_way.objects.filter(id=id)
    payway.delete()
    return redirect(reverse('admin:paylist'))


# 按条件选择订单
def choiceorder(request, page=1):
    if request.method == 'POST':
        way = request.POST.get('choice')
        if way == 'waitpay':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 0")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })
        elif way == 'waitsend':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 1")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })
        elif way == 'waitget':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 2")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })
        elif way == 'waitsay':
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid where o.orderstatus = 3 or o.orderstatus = 4")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select o.id,o.uid_id,a.receiver,a.phone_number,e.express_name,a.location,a.detail_address,o.orderstatus from order_twenty o join user_address a on o.addressid=a.aid join express_company e on e.id=o.expressbrandid")
            columns = [col[0] for col in cursor.description]
            res = [dict(zip(columns, row)) for row in cursor.fetchall()]

            paginator = Paginator(res, NUMOFPAGE)
            page = int(page)
            pagination = paginator.page(page)

            if paginator.num_pages > 5:
                # 如果当前页码-5小于0
                if page - 2 <= 0:
                    customRange = range(1, 6)
                elif page + 2 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    customRange = range(page - 2, page + 2)
            else:  # 页码总数小于10
                customRange = paginator.page_range
            return render(request, 'admin/order_list.html', context={
                'res': pagination.object_list,
                'pagerange': customRange,
                'pagination': pagination,
            })


