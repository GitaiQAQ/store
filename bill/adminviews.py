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
from wsgiref.util import FileWrapper

from bill.models import AdaptorBill, AdaptorBillItem
from bill.models import AdaptorCouponItem as CouponItem
from product.models import AdaptorRule, AdaptorProduct
from django.utils.translation import ugettext as _
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from coupon.models import AdaptorCoupon as Coupon 
from bill import excel_output
from bill import fsutil
from bill import excelutil 

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
    if 'print' in request.GET:
        userid = request.user.id
        if not os.path.isdir(settings.BASE_FILE_PATH):
            os.makedirs(settings.BASE_FILE_PATH)

        filename = os.path.join(settings.BASE_FILE_PATH,'sales.xls' )
        kwargs = {}
        kwargs['filename'] = filename 
        kwargs['bills'] = bills 
        out_excel = excel_output.write_bill_record(**kwargs)
       
        if os.path.isfile(filename):
            try:
                wrapper  = FileWrapper(open(filename, 'rb'))
            except IOError as e:
                return HttpResponse(e)
                
            response    = HttpResponse(wrapper,content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'inline; filename=%s' % os.path.basename( filename )
            response['Content-Length']      = os.path.getsize(filename)
            return response
        else:
            return HttpResponse(u'未找到文件...')
         
    content['mediaroot'] = settings.MEDIA_URL
    content['bills'] = bills
    content['menu'] = 'bill'  
    if isMble:
        return render(request, 'usercenter/usercenter_adminbill.html', content)
    else:
        return render(request, 'usercenter/usercenter_adminbill.html', content)



@login_required
def delivery(request):
    """
    批量发货 
    """
    isMble  = dmb.process_request(request)
    content = {} 
    content['menu'] = 'delivery'
    bills_status = [AdaptorBill.STATUS_PAYED, AdaptorBill.STATUS_DELIVERIED,
     AdaptorBill.STATUS_FINISHED, AdaptorBill.STATUS_BAD]
    if request.method == 'POST':
        filename = os.path.join(settings.BASE_FILE_PATH,'input.xls' )
        if 'file' in request.FILES:
        
            absolute_path = fsutil.handle_uploaded_file(filename, request.FILES['file'])
            if absolute_path == -1:
                content['status'] = 'error'
                content['msg'] = '请上传后缀为xls的excel文件'
                if isMble:
                    return render(request, 'usercenter/usercenter_deliverybill.html', content)
                else:
                    return render(request, 'usercenter/usercenter_deliverybill.html', content)
            try:
                results = excelutil.analyse(absolute_path)
            except Exception as e:
                content['status'] = 'error'
                content['msg'] = '读取excel文件失败，文件格式错误...'
                if isMble:
                    return render(request, 'usercenter/usercenter_deliverybill.html', content)
                else:
                    return render(request, 'usercenter/usercenter_deliverybill.html', content)
            # 存入结果
            failed = 0 # 失败的数量
            succeed = 0 # 成功的数量
            succeed_items = [] # 成功记录
            for result in results:
                try:
                    bill = AdaptorBill.objects.get(no = result['billno'])
                    if bill.status == bill.STATUS_PAYED: #未发货
                        bill.delivery_company = result['company']
                        bill.delivery_no = result['code'].strip()
                        bill.status = bill.STATUS_DELIVERIED
                        bill.save()
                        succeed_items.append(bill)
                        succeed += 1

                except AdaptorBill.DoesNotExist:
                    failed += 1

            content['status'] = 'ok'
            content['succeed'] = succeed
            content['failed'] = failed
            content['bills'] = succeed_items

    if isMble:
        return render(request, 'usercenter/usercenter_deliverybill.html', content)
    else:
        return render(request, 'usercenter/usercenter_deliverybill.html', content)


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

