import hashlib
import os
import re
from datetime import datetime
from random import randint

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
# 地址管理
from django.urls import reverse

from Goods.forms import UserForm1,UserForm2
from Goods.sms import send_sms
from Retailers import settings
from Retailers.settings import SMSCONFIG
from User.models import User, User_grade, User_address, User_account


# 地址管理
def address(request):
    return render(request,'shop/person/address.html')

# 模板
def frame(request):
    return render(request,'shop/frame.html')

# 账单
def bill(request):
    return render(request,'shop/person/bill.html')

# 账单明细
def billlist(request):
    return render(request,'shop/person/billlist.html')
# 绑定手机
def bindphone(request):
    return render(request,'shop/person/bindphone.html')

# 新闻页面
def blog(request):
    return render(request,'shop/person/blog.html')

# 我的红包
def bonus(request):
    return render(request,'shop/person/bonus.html')

# 我的银行卡
def cardlist(request):
    return render(request,'shop/person/cardlist.html')

# 银行卡绑定
def cardmethod(request):
    return render(request,'shop/person/cardmethod.html')

# 退货管理
def change(request):
    return render(request,'shop/person/change.html')

# 我的收藏
def collection(request):
    return render(request,'shop/person/collection.html')

# 评价管理
def comment(request):
    return render(request,'shop/person/comment.html')

# 发表评论
def commentlist(request):
    return render(request,'shop/person/commentlist.html')
# 商品咨询
def consultation(request):
    return render(request,'shop/person/consultation.html')

# 优惠券
def coupon(request):
    return render(request,'shop/person/coupon.html')

# 邮箱验证
def email(request):
    return render(request,'shop/person/email.html')

# 我的足迹
def foot(request):
    return render(request,'shop/person/foot.html')

#  实名认证
def idcard(request):
    return render(request,'shop/person/idcard.html')

# 个人中心
def index(request):
    username = request.session.get('username')
    # print(username)
    user = User.objects.filter(username=username)
    if user:
        user=user[0]
        print(user.uid)
        # print(user.uid)
        # 用户余额
        account=user.user_account
        # print(account,'*'*100)
        # 用户最新积分
        grade=user.user_grade_set.all()
        # print(grade,'*'*100)
        grade=grade[len(grade)-1].changed_grade
        print(grade)
        # print(account.useroffer_id,type(account.used_userofferid))
        if account:
            # 计算可用优惠券数量
            global coupons
            coupons=0
            if account.useroffer_id:
                for i in account.useroffer_id:
                    coupons+=1
            if account.goodoffer_id:
                for g in account.goodoffer_id:
                    coupons+=1
            # print(coupons)

        # 用户订单表
        # order=user.order_twenty
        # print(order)

        return render(request,'shop/person/index.html',context={
        'user':user,
        'coupons':coupons,
        'account':account,
        'grade':grade,
    })
    return render(request, 'shop/person/index.html')

# 个人资料
def information(request):
    email=request.session.get('email')
    phone=request.session.get('phone')
    print('*'*10)
    print(email)
    print(phone)

    if email:
        print(email)
        user = User.objects.filter(email=email)[0]
        print(user.username)
        if request.method == "POST":
            # photo 是表单中文件上传的name
            file = request.FILES.get('picture')
            if file:

                # 文件路径
                path = os.path.join(settings.MEDIA_ROOT, file.name)

                # 文件类型过滤
                ext = os.path.splitext(file.name)
                if len(ext) < 1 or not ext[1] in settings.ALLOWED_FILEEXTS:
                    return redirect(reverse('upload'))

                # 解决文件重名
                if os.path.exists(path):
                    # 日期目录
                    dir = datetime.today().strftime("%Y/%m/%d")
                    dir = os.path.join(settings.MEDIA_ROOT, dir)
                    if not os.path.exists(dir):
                        os.makedirs(dir)  # 递归创建目录

                    # list.png
                    file_name = ext[0] + datetime.today().strftime("%Y%m%d%H%M%S") + str(randint(1, 1000)) + ext[1] if len(
                        ext) > 1 else ''
                    path = os.path.join(dir, file_name)
                    print(path)
                    pathh=path.split('Retailers/static')
                    print(pathh[1])
                    user.user_photo=pathh[1]
                    user.save()

                # 创建新文件
                with open(path, 'wb') as fp:
                    # 如果文件超过2.5M,则分块读写
                    if file.multiple_chunks():
                        for block1 in file.chunks():
                            fp.write(block1)
                    else:
                        fp.write(file.read())

            username = request.POST.get('user-name')
            realname = request.POST.get('realname')
            sex = request.POST.get('radio10')
            birthyear = request.POST.get('birthyear')
            birthmonth = request.POST.get('birthmonth')
            birthday = request.POST.get('birthday')
            birthday = birthyear + birthmonth + birthday
            phonee = request.POST.get('user-phone')
            emaill = request.POST.get('user-email')
            print(username, realname, sex, birthday, phonee, emaill)
            if not User.objects.filter(username=username).exists() and username:
                user.username=username
                user.save()
            if not User.objects.filter(realname=realname).exists() and realname :
                user.realname=realname
                user.save()
            if not User.objects.filter(phone_number=phonee).exists() and phonee:
                user.phone_number=phonee
                user.save()
            if not User.objects.filter(email=emaill).exists() and emaill:
                user.email=emaill
                user.save()
            if sex:
                user.sex=sex
                user.save()
            if birthday:
                user.birthday=birthday
                user.save()
        return render(request, 'shop/person/information.html',context={
            'user':user,
        })
    if phone:
        user = User.objects.filter(phone_number=phone)[0]
        if request.method == "POST":

            # photo 是表单中文件上传的name
            file = request.FILES.get('picture')
            if file:

                # 文件路径
                path = os.path.join(settings.MEDIA_ROOT, file.name)

                # 文件类型过滤
                ext = os.path.splitext(file.name)
                if len(ext) < 1 or not ext[1] in settings.ALLOWED_FILEEXTS:
                    return redirect(reverse('upload'))

                # 解决文件重名
                if os.path.exists(path):
                    # 日期目录
                    dir = datetime.today().strftime("%Y/%m/%d")
                    dir = os.path.join(settings.MEDIA_ROOT, dir)
                    if not os.path.exists(dir):
                        os.makedirs(dir)  # 递归创建目录

                    # list.png
                    file_name = ext[0] + datetime.today().strftime("%Y%m%d%H%M%S") + str(randint(1, 1000)) + ext[
                        1] if len(
                        ext) > 1 else ''
                    path = os.path.join(dir, file_name)
                    print(path)
                    pathh = path.split('Retailers/static')
                    print(pathh[1])
                    user.user_photo = pathh[1]
                    user.save()

                # 创建新文件
                with open(path, 'wb') as fp:
                    # 如果文件超过2.5M,则分块读写
                    if file.multiple_chunks():
                        for block1 in file.chunks():
                            fp.write(block1)
                    else:
                        fp.write(file.read())





            username = request.POST.get('user-name')
            realname = request.POST.get('realname')
            sex = request.POST.get('radio10')
            birthyear = request.POST.get('birthyear')
            birthmonth = request.POST.get('birthmonth')
            birthday = request.POST.get('birthday')
            birthday = birthyear + birthmonth + birthday
            phonee = request.POST.get('user-phone')
            emaill = request.POST.get('user-email')
            print(username, realname, sex, birthday, phonee, emaill)
            if not User.objects.filter(username=username).exists():
                user.username = username
                user.save()
            if not User.objects.filter(realname=realname).exists():
                user.realname = realname
                user.save()
            if not User.objects.filter(phone_number=phonee).exists():
                user.phone_number = phonee
                user.save()
            if not User.objects.filter(email=emaill).exists():
                user.email = emaill
                user.save()
            user.sex = sex
            user.birthday = birthday
            user.save()
        return render(request, 'shop/person/information.html', context={
            'user': user,
        })
    return render(request,'shop/person/information.html')

# 物流信息
def logistics(request):
    return render(request,'shop/person/logistics.html')

# 我的消息
def news(request):
    return render(request,'shop/person/news.html')

# 订单管理
def order(request):
    return render(request,'shop/person/order.html')

# 订单详情
def orderinfo(request):
    return render(request,'shop/person/orderinfo.html')

# 修改密码
def password(request):
    return render(request,'shop/person/password.html')

# 我的积分
def pointnew(request):
    return render(request,'shop/person/pointnew.html')

# 积分明细
def points(request):
    return render(request,'shop/person/points.html')

# 安全问题
def question(request):
    return render(request,'shop/person/question.html')

# 钱款去向
def record(request):
    return render(request,'shop/person/record.html')

# 退换货
def refund(request):
    return render(request,'shop/person/refund.html')

# 安全设置
def safety(request):
    return render(request,'shop/person/safety.html')

# 支付密码
def setpay(request):
    return render(request,'shop/person/setpay.html')

# 意见反馈
def suggest(request):
    return render(request,'shop/person/suggest.html')

# 账户余额
def wallet(request):
    return render(request,'shop/person/wallet.html')

# 账户明细
def walletlist(request):
    return render(request,'shop/person/walletlist.html')

# 登录页面
def login(request):
    if request.method =="POST":
        user=request.POST.get('user')
        password=request.POST.get('password')
        # print(user,type(user),password)
        if password:
            password=hashlib.sha1(password.encode('utf8')).hexdigest()
        if user:
            #用户名登录验证
            user_username=User.objects.filter(username=user)
            # print(user_username)
            if user_username:
                # print('sss')
                if user_username[0].password==password:
                    request.session['phone']=user_username[0].phone_number
                    request.session['email']=user_username[0].email
                    request.session['username']=user_username[0].username
                    return redirect(reverse('order:home'))
            #邮箱登录验证
            user_email=User.objects.filter(email=user)
            # print(user_email)
            if user_email:
                # print('youx')
                if user_email[0].password==password:
                    request.session['phone'] = user_email[0].phone_number
                    request.session['email'] = user_email[0].email
                    request.session['username']=user_email[0].username
                    return redirect(reverse('order:home'))
            # 手机号登录验证
            user_phone = User.objects.filter(phone_number=user)
            # print(user_phone)
            if user_phone:
                # print('手机')
                if user_phone[0].password == password:
                    request.session['phone'] = user_phone[0].phone_number
                    request.session['email'] = user_phone[0].email
                    request.session['username']=user_phone[0].username
                    return redirect(reverse('order:home'))


    return render(request,'shop/home/login.html')



code=None
# 获取验证码
def auth_code_(request):
    if request.method=="POST":
        phone = request.POST.get('phone')
        global code
        code = str(randint(100000, 999999))
        request.session['code']=code
        send_sms(phone, {'code': code}, **SMSCONFIG)

# 注册页面
def register(request):
    form1 = UserForm1()  # 空的表单,没有数据
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if email:
            form1 = UserForm1(request.POST)
            if form1.is_valid():  # 验证通过
                # print(form1.cleaned_data)
                email = form1.cleaned_data.get('email')
                password_1 = form1.cleaned_data.get('password_1')
                password = hashlib.sha1(password_1.encode('utf8')).hexdigest()
                # print(email,password)
                # 写入数据库
                # User.objects.create(**form1.cleaned_data)
                User.objects.create(email=email,password=password)
                # 获取新用户的uid
                uid=User.objects.filter(email=email)[0].uid
                #用户首次注册赠送100积分
                User_grade.objects.create(change_source='首次注册系统赠送',change_number=100,changed_grade=100,growth_value=100,uid_id=uid)
                # 用户账户信息表
                User_account.objects.create(uid=uid)
                # 保存session数据
                request.session['email']=email
                # 验证成功跳转到首页
                return redirect(reverse('goods:information'))
        if phone:
            auth_code = request.POST.get('auth_code')
            passwordph = request.POST.get('passwordph')
            passwordRepeatph = request.POST.get('passwordRepeatph')

            if auth_code != code :

                return render(request, 'shop/home/register.html', context={
                    'form1': form1,
                    'data': '对不起验证码输入错误',
                })
            if  passwordph!=passwordRepeatph :
                return render(request, 'shop/home/register.html', context={
                    'form1': form1,
                    'data': '对不起密码不一致',
                })
            if re.match(r'\d+$', passwordph ):
                return render(request, 'shop/home/register.html', context={
                    'form1': form1,
                    'data': '对不起密码不能是纯数字',
                })
            if len(passwordph)==0:
                return render(request, 'shop/home/register.html', context={
                    'form1': form1,
                    'data': '对不起密码不能为空',
                })
            res = User.objects.filter(phone_number=phone).exists()
            if res:
                return render(request, 'shop/home/register.html', context={
                    'form1': form1,
                    'data': '对不起手机号已存在',
                })
            password = hashlib.sha1(passwordRepeatph.encode('utf8')).hexdigest()
            # print(phone, password)
            # 写入数据库
            # User.objects.create(**form1.cleaned_data)
            User.objects.create(phone_number=phone, password=password)
            # 获取新用户的uid
            uid = User.objects.filter(phone_number=phone)[0].uid
            # 用户首次注册赠送100积分
            User_grade.objects.create(change_source='首次注册系统赠送', change_number=100, changed_grade=100, growth_value=100,
                                      uid_id=uid)

            # 用户账户信息表
            User_account.objects.create(uid=uid)
            # # 保存session数据
            request.session['phone'] = phone
            # # 验证成功跳转到首页
            return redirect(reverse('goods:information'))
    return render(request,'shop/home/register.html',context={
        'form1':form1,
    })

# 删除session
def sc(request):
    request.session.flush()
    return HttpResponse('删除全部session')