import hashlib
import re
from random import randint

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
# 地址管理
from django.urls import reverse

from Goods.forms import UserForm1,UserForm2
from Goods.sms import send_sms
from Retailers.settings import SMSCONFIG
from User.models import User


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

# 脱货管理
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
    return render(request,'shop/person/index.html')

# 个人资料
def information(request):
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
            # # 保存session数据
            request.session['phone'] = phone
            # # 验证成功跳转到首页
            return redirect(reverse('goods:information'))


    return render(request,'shop/home/register.html',context={
        'form1':form1,
    })

