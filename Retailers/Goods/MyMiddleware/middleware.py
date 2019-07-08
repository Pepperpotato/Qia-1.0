import re

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from Retailers.settings import EXCLUDE_URL

exclued_path = [re.compile(item) for item in EXCLUDE_URL]

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # pass
        url_path = request.path
        print(url_path)
        if re.match(r'/order/intro/',url_path):
            return
        # print(EXCLUDE_URL)
        if not url_path in EXCLUDE_URL:
            if request.session.get('username') or request.session.get('email') or request.session.get('phone'):
                return
            else:
                return redirect('/goods/login')
        else:
            return







        # if request.path != '/goods/login/':
        #     print(request.path)
        #     if request.session.get('username'):
        #         return
        #     else:
        #         return redirect('/goods/login')
        # else:
        #     return
