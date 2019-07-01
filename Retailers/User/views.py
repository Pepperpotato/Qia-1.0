
import hashlib

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.



def add(request):
    # user = User.objects.get(uid=3)
    # user = User(username='admin', password=hashlib.sha1('admin123'.encode('utf8')).hexdigest(),
    #      pay_password=hashlib.sha1('admin123'.encode('utf8')).hexdigest(), user_type=0, certificate='身份证',
    #      certificate_id='000000000000000000', phone_number='00000000000', email='0000@126.com')
    # user.username = '李四'
    # user.password = hashlib.sha1('lisi123'.encode('utf8')).hexdigest()
    # user.pay_password = hashlib.sha1('lisi123'.encode('utf8')).hexdigest()
    # user.save()

    return HttpResponse('增加数据')
