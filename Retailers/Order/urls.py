from django.conf.urls import url, include
from Order import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^home/$', views.home,name='home'),
    url(r'^intro/(?P<goodid>\d+)/$',views.intro,name='intro'),
    # url(r'^purchase/$',views.purchase,name='purchase'),
    url(r'^price$',views.price_change,name='price'),
    url(r'^add_cart$',views.add_cart,name='add_cart'),
    url(r'^pay/(?P<commodityid>\d+)/(?P<count>\d+)/$',views.pay,name='pay'),
    url(r'^addre/$',views.addre,name='addre'),
    url(r'^express/$',views.express,name='express'),
    url(r'^commit/$',views.commit,name='commit'),
    url(r'^shopcart/$',views.shopcart,name='shopcart'),
    url(r'^check_cart$', views.check_cart, name='check_cart'),
    url(r'^delete_cart$', views.delete_cart, name='delete_cart')
]