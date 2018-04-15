#! -*- coding:utf-8 -*-
import pdb
import json
import random
import string
import os
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse 
from django.http import Http404, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 
from django.views.generic.detail import DetailView
from django.conf import settings
from django.shortcuts import redirect   
from bill.models import AdaptorBill, AdaptorBillItem
from bill.models import AdaptorCouponItem as CouponItem
from product.models import AdaptorRule, AdaptorProduct
from django.utils.translation import ugettext as _
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from coupon.models import AdaptorCoupon as Coupon 
dmb     = DetectMobileBrowser()

def web_callback(request):
    """
    网页前端查询这个接口来查看订单是否已经支付完成
    """
    retult = {}
    result['status']='error'
    result['msg'] = "支付未完成"
    if 'billno' in request.GET:
        billno = request.GET['billno']
        try:
            bill = AdaptorBill.objects.get(no=no)
            if bill.status == AdaptorBill.STATUS_PAYED:
                result['status']='ok'
                result['msg'] = "订单已支付"
        except AdaptorBill.DoesNotExist:
            raise Http404
    else:
        result['请提供订单号']

    return HttpResponse(json.dumps(result), content_type='application/json')


def pay_callback(request):
    """
    支付接口回调接口
    支付接口完成支付后调用该函数来更新我们的数据库
    """

    return HttpResponse("done")

@login_required
def admin(request):
    """
    销售订单 
    """
    isMble  = dmb.process_request(request)
    content = {} 
    bills_status = [AdaptorBill.STATUS_PAYED, AdaptorBill.STATUS_DELIVERIED,
     AdaptorBill.STATUS_FINISHED, AdaptorBill.STATUS_BAD]

    kwargs = {}
    if 'status' in request.GET:
        status = request.GET['status']
        if status != '-1':
            content['status'] = status  
            kwargs['status'] = status
        else:
            kwargs['status__in'] = bills_status
    else:
        kwargs['status__in'] = bills_status

    if 'billno' in request.GET:
        billno = request.GET['billno']
        content['billno'] = billno  
        kwargs['no__icontains'] = billno
      
    bills = AdaptorBill.objects.filter( **kwargs ) 
    content['mediaroot'] = settings.MEDIA_URL
    content['bills'] = bills
    content['menu'] = 'bill'  
    if isMble:
        return render(request, 'usercenter/usercenter_adminbill.html', content)
    else:
        return render(request, 'usercenter/usercenter_adminbill.html', content)

@login_required
def sales(request):
    """
    销售统计 
    """
    isMble  = dmb.process_request(request)
    content = {} 
    bills_status = [AdaptorBill.STATUS_PAYED, AdaptorBill.STATUS_DELIVERIED,
     AdaptorBill.STATUS_FINISHED, AdaptorBill.STATUS_BAD]

    kwargs = {}
    kwargs['status__in'] = bills_status
    if 'billno' in request.GET:
        billno = request.GET['billno']
        content['billno'] = 'billno'  
        kwargs['no__icontains'] = billno
    bills = AdaptorBill.objects.filter( **kwargs ) 
    content['mediaroot'] = settings.MEDIA_URL
    content['bills'] = bills
    content['menu'] = 'sale'  
    if isMble:
        return render(request, 'usercenter/usercenter_salesbill.html', content)
    else:
        return render(request, 'usercenter/usercenter_salesbill.html', content)

