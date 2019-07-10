
from django.conf.urls import url


from User import views
# from User.views import OrderPayView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^add/$', views.add, name='add'),
    url(r'^login/$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^productlist/(\d+)/$', views.productlist, name='productlist1'),
    url(r'^productlist/$', views.productlist, name='productlist'),
    # url(r'^addnewgood/$', views.addnewgood, name='addnewgood'),
    url(r'^addgood/$', views.addgood, name='addgood'),
    url(r'^addband/$', views.addband, name='addband'),
    url(r'^addbigcategory/$', views.addbigcategory, name='addbigcategory'),
    url(r'^alterbigcategory/$', views.alterbigcategory, name='alterbigcategory'),
    url(r'^addsmallcategory/$', views.addsmallcategory, name='addsmallcategory'),
    url(r'^addattrbute/$', views.addattrbute, name='addattrbute'),
    url(r'^addinventory/$', views.addinventory, name='addinventory'),
    url(r'^addinventory1/$', views.addinventory1, name='addinventory1'),
    url(r'^addinventory2/$', views.addinventory2, name='addinventory2'),
    url(r'^addinventory3/$', views.addinventory3, name='addinventory3'),
    url(r'^addinventory4/$', views.addinventory4, name='addinventory4'),
    url(r'^addgoodetail/$', views.addgoodetail, name='addgoodetail'),
    url(r'^orderlist/$', views.orderlist, name='orderlist'),
    url(r'^orderlist/(\d+)$', views.orderlist, name='orderlist1'),
    url(r'^choiceorder/(\d+)$', views.choiceorder, name='choiceorder1'),
    url(r'^choiceorder/$', views.choiceorder, name='choiceorder'),
    url(r'^delorder/(\d+)/$', views.delorder, name='delorder'),
    url(r'^orderdetail/(\d+)/$', views.orderdetail, name='orderdetail'),
    url(r'^userlist/(\d+)/$', views.userlist, name='userlist1'),
    url(r'^userlist/$', views.userlist, name='userlist'),
    url(r'^deluser/(\d+)/$', views.deluser, name='deluser'),
    url(r'^userdetail/(\d+)/$', views.userdetail, name='userdetail'),
    url(r'^userrank/$', views.userrank, name='userrank'),
    url(r'^useraccount/$', views.useraccount, name='useraccount'),
    url(r'^setting/$', views.setting, name='setting'),
    url(r'^expresslist/$', views.expresslist, name='expresslist'),
    url(r'^delexpress/(\d)/$', views.delexpress, name='delexpress'),
    url(r'^paylist/$', views.paylist, name='paylist'),
    url(r'^delpayway/(\d)/$', views.delpayway, name='delpayway'),
    url(r'^pageviews/$', views.pageviews, name='pageviews'),
    url(r'^sales/$', views.sales, name='sales'),
    url(r"^pay/$", views.pay, name='pay'),
    url(r'^checkpay/$', views.checkpay, name='checkpay'),
    url(r'^test/$', views.test, name='test'),

]

