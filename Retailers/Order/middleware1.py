import sys
from datetime import datetime
from django.views.debug import technical_500_response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class Middleware1(MiddlewareMixin):
    pass
