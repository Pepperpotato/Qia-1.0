from django.conf.urls import url
from django.contrib import admin

from App import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^add/$', views.index, name='index')
]
