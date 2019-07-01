
from django.conf.urls import url, include
from django.contrib import admin

from Goods import views

urlpatterns = [


    # 地址管理
    url(r'^address/$',views.address,name='address'),
    # 模板
    url(r'^frame/$',views.frame,name='frame'),
    # 账单
    url(r'^bill/$',views.bill,name='bill'),
    # 账单明细
    url(r'^billlist/$',views.billlist,name='billlist'),
    # 绑定手机
    url(r'^bindphone/$',views.bindphone,name='bindphone'),
    #新闻页面
    url(r'^blog/$',views.blog,name='blog'),
    #我的红包
    url(r'^bonus/$',views.bonus,name='bonus'),
    # 我的银行卡
    url(r'^cardlist/$', views.cardlist, name='cardlist'),
    # 银行卡绑定
    url(r'^cardmethod/$', views.cardmethod, name='cardmethod'),
    # 退换货管理
    url(r'^change/$', views.change, name='change'),
    # 我的收藏
    url(r'^collection/$', views.collection, name='collection'),
    # 评价管理
    url(r'^comment/$', views.comment, name='comment'),
    # 发表评论
    url(r'^commentlist/$', views.commentlist, name='commentlist'),
    # 商品咨询
    url(r'^consultation/$', views.consultation, name='consultation'),
    # 优惠券
    url(r'^coupon/$', views.coupon, name='coupon'),
    # 邮箱验证
    url(r'^email/$', views.email, name='email'),
    # 我的足迹
    url(r'^foot/$', views.foot, name='foot'),
    # 实名认证
    url(r'^idcard/$', views.idcard, name='idcard'),
    # 个人中心
    url(r'^index/$', views.index, name='index'),
    # 个人资料
    url(r'^information/$', views.information, name='information'),
    # 物流信息
    url(r'^logistics/$', views.logistics, name='logistics'),
    # 我的消息
    url(r'^news/$', views.news, name='news'),
    # 订单管理
    url(r'^order/$', views.order, name='order'),
    # 订单详情
    url(r'^orderinfo/$', views.orderinfo, name='orderinfo'),
    # 修改密码
    url(r'^password/$', views.password, name='password'),
    # 我的积分
    url(r'^pointnew/$', views.pointnew, name='pointnew'),
    # 积分明细
    url(r'^points/$', views.points, name='points'),
    # 安全问题
    url(r'^question/$', views.question, name='question'),
    # 钱款去向
    url(r'^record/$', views.record, name='record'),
    # 退换货
    url(r'^refund/$', views.refund, name='refund'),
    # 安全设置
    url(r'^safety/$', views.safety, name='safety'),
    # 支付密码
    url(r'^setpay/$', views.setpay, name='setpay'),
    # 意见反馈
    url(r'^suggest/$', views.suggest, name='suggest'),
    # 账户余额
    url(r'^wallet/$', views.wallet, name='wallet'),
    # 账户明细
    url(r'^walletlist/$', views.walletlist, name='walletlist'),
    # 登录页面
    url(r'^login/$', views.login, name='login'),
    # 获取验证码
    url(r'^auth_code_/$',views.auth_code_,name='auth_code_'),
    # 注册页面
    url(r'^register/$',views.register,name='register'),
]


