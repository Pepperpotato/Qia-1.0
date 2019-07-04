from django.conf.urls import url, include
from Order import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^home/$', views.home,name='home'),
    url(r'^intro/(?P<dlbid>\d+)/(?P<xlbid>\d+)/(?P<goodid>\d+)/$',views.intro,name='intro'),
    url(r'^verf$',views.verf,name='verf')
]