#! -*- coding:utf-8 -*-
import pdb
import json
import random
import string
import os
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import Http404, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response 
 
from invoice.models import Invoice

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser


dmb     = DetectMobileBrowser()
 
class InvoiceView(APIView):

    @method_decorator(login_required)
    def get(self, request,  format=None ):
        """获取某个用户的购物车列表"""
        if 'invoicetype' in request.GET:
            invoicetype = request.GET['invoicetype']
            invoices = Invoice.objects.filter(user = request.user, invoicetype=invoicetype)
        else:
            invoices = Invoice.objects.filter(user = request.user, invoicetype=1)
        
        
        content = {}  
        if len(invoices) > 0:
            invoice = invoices[0]
            content['invoicetype'] = invoice.invoicetype
            content['code'] = invoice.code
            content['title'] = invoice.title
            content['content'] = invoice.content 
         
        return HttpResponse(json.dumps(content), content_type='application/json')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request ):
        """
        创建、删除
        创建需要参数：method:create, ruleid, num, desc
        """
        result = {} 
        if request.method == 'POST': 
            user = request.user　
            if 'method' in request.POST:　
                invoicetype = request.POST['invoicetype']
                code = request.POST.get('code')
                title = request.POST['title']
                content = request.POST.get('content')　
                invoice = Invoice.objects.create(user = user, code=code,
               　　　　　　 invoicetype=invoicetype, content=content, title=title)　
                result['status'] = 'ok'
                result['msg']    = _('Add successfully....') # '添加成功...' 　
            else:   
                result['status'] = 'error'
                result['msg']    = _('Need method in post...') 
        else:
            result['status'] = 'error'
            result['msg']    = _('Method error..')
                  
        return HttpResponse(json.dumps(result), content_type='application/json')
         