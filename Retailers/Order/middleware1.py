
import datetime
from django.utils.deprecation import MiddlewareMixin

from Order.models import Mobilecount


class Middleware1(MiddlewareMixin):
    def process_view(self,request, view_func, view_args, view_kwargs):
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        print(time)
        res = Mobilecount.objects.filter(time__contains=time).first()
        if res:
            res.view+= 1
            res.save(update_fields=['view'])
        else:
            tmp = Mobilecount(view=1)
            tmp.save()



