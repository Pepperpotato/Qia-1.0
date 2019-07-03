from django.conf.urls import url, include
from Order import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^view/$',views.view,name='view'),
    url(r'^home/$', views.home,name='home'),
]