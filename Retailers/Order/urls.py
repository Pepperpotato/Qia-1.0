from django.conf.urls import url, include
from Order import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^home/$', views.home,name='home'),
    url(r'^intro/(?P<goodid>\d+)/$',views.intro,name='intro'),
    url(r'^verf/$',views.verf,name='verf'),
    url(r'^price$',views.price_change,name='price'),
    url(r'^add_cart$',views.add_cart,name='add_cart')
]