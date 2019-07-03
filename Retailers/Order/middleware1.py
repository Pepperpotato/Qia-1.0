import sys
import datetime
from django.views.debug import technical_500_response
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from Order.models import Mobilecount


class Middleware1(MiddlewareMixin):
    def process_view(self,request, view_func, view_args, view_kwargs):
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        res = Mobilecount.objects.filter(time__contains=time)[0]
        if res:
            print(res,type(res))
            res.view+= 1
            res.save(update_fields=['view'])
        else:
            tmp = Mobilecount(view=1)
            tmp.save()
        # return response


