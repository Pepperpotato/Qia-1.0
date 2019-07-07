import hashlib
import json
import os
import re
from datetime import datetime
from random import randint

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
# 地址管理
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from Goods.forms import UserForm1,UserForm2
from Goods.models import Coupons
from Goods.sms import send_sms
from Retailers import settings
from Retailers.settings import SMSCONFIG, SMSCONFIGG
from User.models import User, User_grade, User_address, User_account
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.core.mail import send_mail

# 模板
def frame(request):
    return render(request,'shop/frame.html')

# 地址管理
def address(request):
    return render(request,'shop/person/address.html')

# 账单
def bill(request):
    return render(request,'shop/person/bill.html')

# 账单明细
def billlist(request):
    return render(request,'shop/person/billlist.html')


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



# 我的足迹
def foot(request):
    return render(request,'shop/person/foot.html')




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
    data=None
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
                if user_username[0].password==password and user_username[0].user_status==0:
                    request.session['phone']=user_username[0].phone_number
                    request.session['email']=user_username[0].email
                    request.session['username']=user_username[0].username
                    return redirect(reverse('order:home'))
                else:
                    data='对不起登录失败'
            #邮箱登录验证
            user_email=User.objects.filter(email=user)
            # print(user_email)
            if user_email:
                # print('youx')
                if user_email[0].password==password and user_email[0].user_status==0:
                    request.session['phone'] = user_email[0].phone_number
                    request.session['email'] = user_email[0].email
                    request.session['username']=user_email[0].username
                    return redirect(reverse('order:home'))
                else:
                    data='对不起登录失败'
            # 手机号登录验证
            user_phone = User.objects.filter(phone_number=user)
            # print(user_phone)
            if user_phone:
                # print('手机')
                if user_phone[0].password == password and user_phone[0].user_status==0:
                    request.session['phone'] = user_phone[0].phone_number
                    request.session['email'] = user_phone[0].email
                    request.session['username']=user_phone[0].username
                    return redirect(reverse('order:home'))
                else:
                    data='对不起登录失败'


    return render(request,'shop/home/login.html',context={
        'data':data,
    })


# 获取注册验证码
def auth_code_(request):
    if request.method=="POST":
        phone = request.POST.get('phone')
        res = User.objects.filter(phone_number=phone).exists()
        if res:
            return
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
                # print(uid)
                #用户首次注册赠送100积分
                User_grade.objects.create(change_source='首次注册系统赠送',change_number=100,changed_grade=100,growth_value=100,uid_id=uid)
                # 用户账户信息表
                User_account.objects.create(user_id=uid)
                # 保存session数据
                request.session['email']=email
                # 发送激活邮件
                subject = "辛姐小吃铺激活邮件"  # 邮件标题
                message = ''  # 邮件正文
                sender = settings.EMAIL_FROM  # 发件人
                # print(sender)
                receiver = [email]  # 收件人
                serializer = Serializer(settings.SECRET_KEY, 3600)  # 有效期1小时
                info = {"confirm": uid}
                token = serializer.dumps(info)
                html_message = """
                           <h1>  恭喜您成为辛姐小吃铺注册会员</h1><br/><h3>请您在1小时内点击以下链接进行账户激活</h3><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>
                """ % ( token, token)
                send_mail(subject, message, settings.EMAIL_HOST_USER, receiver, html_message=html_message)
                # 验证成功跳转到首页
                return HttpResponse('注册成功,请前往邮箱进行账户激活')
        if phone:
            auth_code = request.POST.get('auth_code')
            passwordph = request.POST.get('passwordph')
            passwordRepeatph = request.POST.get('passwordRepeatph')
            # print(phone)
            res = User.objects.filter(phone_number=phone).exists()
            if res:
                return render(request, 'shop/home/register.html', context={
                    'form1': form1,
                    'data': '对不起手机号已存在',
                })
            if auth_code != request.session.get('code') :
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
            User_account.objects.create(user_id=uid)
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
    # return HttpResponse('删除全部session')
    return redirect(reverse('order:home'))

# 安全设置
def safety(request):
    user=safety=articleyellow=phone=email=None
    username=request.session.get('username')
    print(username)
    if username:
        user=User.objects.filter(username=username)[0]

        # 用户账户信息表
        account = user.user_account
        # 计算用户安全分
        safety = 0
        if user.realname:
            safety += 10
        if user.pay_password:
            safety += 10
        if user.certificate:
            safety += 10
        if user.phone_number:
            safety += 10
        if user.email:
            safety += 10
        if user.question1:
            safety += 10
        if user.question2:
            safety += 10
        if account.pay_password:
            safety += 10
        if account.bankcard_id:
            safety += 10
        if account.alipay_number:
            safety += 5
        if account.wechat_number:
            safety += 5
        # 黄色安全条
        articleyellow = 100 - safety
        phone_number = User.objects.filter(username=username)[0].phone_number
        email = User.objects.filter(username=username)[0].email
        if email:
            # print(email)
            emaill=re.search(r'@\S+',email).group()
            # print(emaill)
            email=email[:4]+'XXXX'+emaill
        if  phone_number:
            phone = phone_number[:3] + 'XXXX' + phone_number[-4:]
    return render(request, 'shop/person/safety.html', context={
        'user': user,
        'safety': safety,
        'articleyellow': articleyellow,
        'phone':phone,
        'email':email,
    })

# 个人中心
@csrf_exempt # 请求这个方法时不需加csrf验证
def index(request):
    username = request.session.get('username')
    # print(username)
    if username:
        user = User.objects.filter(username=username)
        if user:
            user=user[0]
            print(user.uid)
            # print(user.uid)
            # 用户最新积分
            grade = user.user_grade_set.all()
            # print(grade,'*'*100)
            grade = grade[len(grade) - 1].changed_grade
            # print(grade)
            # 用户账户信息表
            account=user.user_account
            # print(account,'*'*100)
            # print(account.useroffer_id,type(account.used_userofferid))
            coupons=0
            if account:
                # 计算可用优惠券数量
                coupons=0
                if account.useroffer_id:
                    for i in account.useroffer_id:
                        coupons+=1
                if account.goodoffer_id:
                    for g in account.goodoffer_id:
                        coupons+=1
                # print(coupons)
            # 计算用户安全分
            safety = 0
            if user.realname:
                safety+=10
            if user.pay_password:
                safety+=10
            if user.certificate:
                safety+=10
            if user.phone_number:
                safety+=10
            if user.email:
                safety+=10
            if user.question1:
                safety+=10
            if user.question2:
                safety+=10
            if account.pay_password:
                safety+=10
            if account.bankcard_id:
                safety+=10
            if account.alipay_number:
                safety+=5
            if account.wechat_number:
                safety+=5
            # 黄色安全条
            articleyellow=100-safety
            # 用户订单表
            orders=user.ordertwenty_set.all()
            # print(orders)
            first=second=None
            if orders:
                # 最新订单记录
                first=orders[len(orders)-1]
                # print(first.)
                if len(orders)>1:
                    # 第二新订单记录
                    second=orders[len(orders)-2]
            # 商品优惠卷查询
            goodscoupons=Coupons.objects.order_by('-id')[:2]
            # print(goodscoupons)
            # 领取优惠券
            if request.method == 'POST':
                # print('aaaaa')
                key = str(request.POST.keys())
                if key=="dict_keys(['1'])":
                    goodoffer=user.user_account.goodoffer_id
                    user.user_account.goodoffer_id=goodoffer+str(1)
                    user.user_account.save()
                if key=="dict_keys(['2'])":
                    goodoffer=user.user_account.goodoffer_id
                    user.user_account.goodoffer_id=goodoffer+str(2)
                    user.user_account.save()

            return render(request,'shop/person/index.html',context={
            'user':user,
            'coupons':coupons,
            'account':account,
            'grade':grade,
            'first':first,
            'second':second,
            'safety':safety,
            'articleyellow':articleyellow,
            'goodscoupons':goodscoupons,
        })
    return render(request, 'shop/person/index.html',context={
        'coupons': 0,
        'grade': 0,
        'user':0,
        'articleyellow':100,
    })
# 个人资料
def information(request):
    email=request.session.get('email')
    phone=request.session.get('phone')
    # print('*'*10)
    # print(email)
    # print(phone)

    if email:
        # print(email)
        user = User.objects.filter(email=email)[0]
        # print(user.username)
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
                    # print(path)
                    pathh=path.split('Retailers/static')
                    # print(pathh[1])
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
            # print(username, realname, sex, birthday, phonee, emaill)
            if not User.objects.filter(username=username).exists() and username:
                user.username=username
                user.save()
                request.session['username']=username
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
                    # print(path)
                    pathh = path.split('Retailers/static')
                    # print(pathh[1])
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
                request.session['username']=username
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

# 修改密码
def password(request):
    username=request.session.get('username')
    data=None
    if username:
        if request.method == "POST":
            password = request.POST.get('password')
            password = hashlib.sha1(password.encode('utf8')).hexdigest()
            newpassword1 = request.POST.get('newpassword1')
            newpassword2 = request.POST.get('newpassword2')
            user=User.objects.filter(username=username)[0]
            print(user.password)
            if newpassword1==newpassword2 and re.match('\D',newpassword1) and len(newpassword1)>6 and user.password==password:
                newpassword=hashlib.sha1(newpassword1.encode('utf8')).hexdigest()
                user.password=newpassword
                user.save()
                data='恭喜你修改成功'
            else:
                data='对不起修改失败'
    return render(request,'shop/person/password.html',context={
        'data':data,
})

# 支付密码
def setpay(request):
    username = request.session.get('username')
    # print(request.GET.get('code'))
    if request.GET:
        code=request.GET.get('code')
        password1=request.GET.get('password1')
        password2=request.GET.get('password2')
        if code==request.session.get('codee')  and  len(
                 password1) == 6 and password1 == password2:
            user = User.objects.filter(username=username)[0]
            user.pay_password = password1
            user.save()
            return HttpResponse(json.dumps({'data': '修改成功'}), content_type='application/json')

        return HttpResponse(json.dumps({'data':'对不起验证失败'}), content_type='application/json')
    phone=None
    if username:
        phone_number=User.objects.filter(username=username)[0].phone_number
        phone=phone_number[:3]+'XXXX'+phone_number[-4:]
    return render(request,'shop/person/setpay.html',context={
        'phone_number':phone,
    })

# 获取验证码
def pswordcode_(request):
    code = request.GET.get('code')
    newphone = request.GET.get('newphone')
    if newphone:
        res = User.objects.filter(phone_number=newphone).exists()
        if res:
            return HttpResponse(json.dumps({'data': '对不起手机号已存在,请重新输入'}), content_type='application/json')
    if code:
        if code != request.session['codee']:
            return HttpResponse(json.dumps({'data': '验证码错误,请重新输入'}), content_type='application/json')
        codee = str(randint(100000, 999999))
        request.session['codee'] = codee
        # print(codee)
        if newphone:
            send_sms(newphone, {'code': codee}, **SMSCONFIGG)
        return HttpResponse(json.dumps({'data': '发送成功'}), content_type='application/json')

    username = request.session.get('username')
    phone=None
    if username:
        phone=User.objects.filter(username=username)[0].phone_number
    codee = str(randint(100000, 999999))
    request.session['codee'] = codee
    # print(codee)

    if phone:
        send_sms(phone, {'code': codee}, **SMSCONFIGG)
    return HttpResponse(json.dumps({'data': '发送成功'}), content_type='application/json')

# 换绑手机
def bindphone(request):
    username = request.session.get('username')
    # print(request.GET.get('code'))
    if request.GET:
        code = request.GET.get('code')
        newphone = request.GET.get('newphone')
        res = User.objects.filter(phone_number=newphone).exists()
        if code == request.session.get('codee') and not res:
            user = User.objects.filter(username=username)[0]
            user.phone_number = newphone
            user.save()
            request.session['phone']=newphone
            return HttpResponse(json.dumps({'data': '修改成功'}), content_type='application/json')

        return HttpResponse(json.dumps({'data': '对不起验证失败'}), content_type='application/json')
    phone = None
    if username:
        phone_number = User.objects.filter(username=username)[0].phone_number
        phone = phone_number[:3] + 'XXXX' + phone_number[-4:]

    return render(request,'shop/person/bindphone.html', context={
        'phone_number': phone,})

# 邮箱验证
def email(request):
    newemail=request.GET.get('newemail')
    code=request.GET.get('code')
    if newemail and code==request.session.get('codee'):
        username = request.session.get('username')
        user=User.objects.filter(username=username)[0]
        user.email=newemail
        user.save()
        request.session['email']=newemail
        return HttpResponse(json.dumps({'data': '修改成功'}), content_type='application/json')
    if newemail and not code:
        recipient_list = [newemail,]  # 收件人
        res=User.objects.filter(email=newemail).exists()
        if res :
            return HttpResponse(json.dumps({'data': '发送失败,邮箱已存在'}), content_type='application/json')
        # print(recipient_list)
        message=''
        serializer = Serializer(settings.SECRET_KEY, settings.EMAIL_TIME)  # 有效期1小时
        info = {"confirm": newemail}
        token = serializer.dumps(info)
        codee = str(randint(100000, 999999))
        request.session['codee']=codee
        html_message = """ <h1>  尊敬的会员您好,您的邮箱验证吗是:%s</h1><br/><h3>请您在1小时内点击以下链接进行账户激活</h3><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>""" % (codee,token,token)
        # print(html_message)
        # send_mail(subject, message, settings.EMAIL_HOST_USER, receiver, html_message=html_message)
        send_mail(settings.EMAIL_SUBJECT_CODE,message,  from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list, html_message=html_message,)
        return HttpResponse(json.dumps({'data': '发送成功'}), content_type='application/json')

    return render(request,'shop/person/email.html')

#  实名认证
def idcard(request):
    username=request.session.get('username')
    realname=User.objects.filter(username=username)[0].realname
    user=User.objects.filter(username=username)[0]
    if request.method=="POST":
        realnam=request.POST.get('user-name')
        if realnam:
            user.realname=realnam
            user.save()
        useridcard=request.POST.get('user-IDcard')
        if useridcard:
            user.certificate='身份证'
            user.certificate_id=useridcard
            user.save()

        # photo 是表单中文件上传的name
        file = request.FILES.get('file1')
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
                # print(path)
                pathh = path.split('Retailers/static')
                # print(pathh[1])
                user.certificate_top = pathh[1]
                user.save()
            # 创建新文件
            with open(path, 'wb') as fp:
                # 如果文件超过2.5M,则分块读写
                if file.multiple_chunks():
                    for block1 in file.chunks():
                        fp.write(block1)
                else:
                    fp.write(file.read())

                # photo 是表单中文件上传的name
                file2 = request.FILES.get('file2')
                if file2:
                    # 文件路径
                    path = os.path.join(settings.MEDIA_ROOT, file2.name)
                    # 文件类型过滤
                    ext = os.path.splitext(file2.name)
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
                        # print(path)
                        pathh = path.split('Retailers/static')
                        # print(pathh[1])
                        user.certificate_down = pathh[1]
                        user.save()
                    # 创建新文件
                    with open(path, 'wb') as fp:
                        # 如果文件超过2.5M,则分块读写
                        if file.multiple_chunks():
                            for block1 in file.chunks():
                                fp.write(block1)
                        else:
                            fp.write(file.read())
        return render(request, 'shop/person/idcard.html', context={
            'realname': realname,'data':'上传成功'
        })

    return render(request,'shop/person/idcard.html',context={
        'realname':realname,
    })