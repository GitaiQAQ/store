from django.shortcuts import render
from pay.controller import MainController

def weixin(request):
    return HttpResponse("get u")