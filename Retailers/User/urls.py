
from django.conf.urls import url


from User import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^add/$', views.add, name='add'),
    url(r'^login/$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^productlist/$', views.productlist, name='productlist'),
    url(r'^productdetail/$', views.productdetail, name='productdetail'),
    url(r'^orderlist/$', views.orderlist, name='orderlist'),
    url(r'^orderdetail/$', views.orderdetail, name='orderdetail'),
    url(r'^userlist/$', views.userlist, name='userlist'),
    url(r'^userdetail/$', views.userdetail, name='userdetail'),
    url(r'^userrank/$', views.userrank, name='userrank'),
    url(r'^useraccount/$', views.useraccount, name='useraccount'),
    url(r'^setting/$', views.setting, name='setting'),
    url(r'^expresslist/$', views.expresslist, name='expresslist'),
    url(r'^delexpress/(\d)/$', views.delexpress, name='delexpress'),
    url(r'^paylist/$', views.paylist, name='paylist'),
    url(r'^delpayway/(\d)/$', views.delpayway, name='delpayway'),
    url(r'^pageviews/$', views.pageviews, name='pageviews'),
    url(r'^sales/$', views.sales, name='sales')
]

