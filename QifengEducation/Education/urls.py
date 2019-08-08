from django.conf.urls import url


from Education import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),

]
