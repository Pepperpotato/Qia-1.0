from django.conf.urls import url, include
from django.contrib import admin

from User import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^add/$', views.add, name='add')
]