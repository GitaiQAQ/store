#! -*- coding:utf-8 -*-
import pdb
import json
import random
import string
import os
from datetime import datetime, timedelta
from django.utils import timezone
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
    user = request.user
    perm = user.has_perm('bill.manage_bill')
    if not perm:
        return HttpResponse("403")

    isMble  = dmb.process_request(request)
    content = {} 
    #bills_status = [AdaptorBill.STATUS_PAYED, AdaptorBill.STATUS_DELIVERIED,
    # AdaptorBill.STATUS_FINISHED, AdaptorBill.STATUS_BAD]
    bills_status = [AdaptorBill.STATUS_PAYED, AdaptorBill.STATUS_DELIVERIED,
     AdaptorBill.STATUS_FINISHED]

    kwargs = {}
    kwargs, content = search(request)
    kwargs['refundstatus'] = AdaptorBill.REFUNDAPPLY
    if 'status' in request.GET:
        status = request.GET['status']
        if status != '-1':
            content['status'] = status  
            kwargs['status'] = status
        else:
            kwargs['status__in'] = bills_status
    else:
        kwargs['status__in'] = bills_status # 默认什么都不显示

    if 'datefrom' in request.GET:
        datefrom = request.GET['datefrom'].strip()
        if len(datefrom) > 0:
            datefrom = datetime.strptime(datefrom, "%Y-%m-%d") 
            kwargs['date__gte'] = datefrom
            content['datefrom'] = datefrom.strftime("%Y-%m-%d")
    
    if 'dateto' in request.GET:
        dateto = request.GET['dateto'].strip()
        if len(dateto) > 0:
            dateto = datetime.strptime(dateto, "%Y-%m-%d")
            content['dateto'] = dateto.strftime("%Y-%m-%d")
            content['dateto'] = dateto.strftime("%Y-%m-%d") 
            dateto = dateto + timedelta(days=1) 
            kwargs['date__lte'] = dateto
             
    # 

    if 'delivery_datefrom' in request.GET:
        delivery_datefrom = request.GET['delivery_datefrom'].strip()
        if len(delivery_datefrom) > 0:
            delivery_datefrom = datetime.strptime(delivery_datefrom, "%Y-%m-%d")
             
            kwargs['delivery_date__gte'] = delivery_datefrom
            content['delivery_datefrom'] = delivery_datefrom.strftime("%Y-%m-%d")
    
    if 'delivery_dateto' in request.GET:
        delivery_dateto = request.GET['delivery_dateto'].strip()
        if len(delivery_dateto) > 0:
            delivery_dateto = datetime.strptime(delivery_dateto, "%Y-%m-%d")
            content['delivery_dateto'] = delivery_dateto.strftime("%Y-%m-%d") 
            delivery_dateto = delivery_dateto + timedelta(days=1) 
            kwargs['delivery_date__lte'] = delivery_dateto
            

    bills = AdaptorBill.objects.filter( **kwargs ) 
    if 'print' in request.GET:
        userid = request.user.id
        if not os.path.isdir(settings.BASE_FILE_PATH):
            os.makedirs(settings.BASE_FILE_PATH)

        filename = os.path.join(settings.BASE_FILE_PATH,'销售订单.xls' )
        kwargs = {}
        kwargs['filename'] = filename 
        kwargs['bills'] = bills 
        out_excel = excel_output.write_admin_record(**kwargs)
       
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

    # 分页开始
    counter = len(bills) 
    pagenation = False
    if counter > settings.PAGEINDEX : # 需要分页时才分页 
        pagenation = True
        i, j = divmod(counter, settings.PAGEINDEX)
        if j > 0:
            i = i + 2
        else:
            i = i + 1
        content['maxpage'] = i - 1
        content['pages'] = range(1, i)
        print(content['pages'] )
        page = 1
        if 'page' in request.GET:
            try:
                page = int(request.GET['page'])
                if page <= 0:
                    page = 1
            except ValueError:
                pass 
        content['page'] = page
        bills = bills[(page - 1) * settings.PAGEINDEX : page*settings.PAGEINDEX ]
    content['pagenation'] = pagenation
    # 分页结束


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
    user = request.user
    perm = user.has_perm('bill.manage_bill')
    if not perm:
        return HttpResponse("403")
    deliveriedbills = AdaptorBill.objects.filter(status = AdaptorBill.STATUS_DELIVERIED)
    for d_bill in deliveriedbills:
        if len(d_bill.delivery_company) == 0 or len(d_bill.delivery_no) == 0:
            d_bill.status = d_bill.STATUS_PAYED
            d_bill.save()
    isMble  = dmb.process_request(request)
    content = {} 
    content['menu'] = 'delivery'
    bills_status = [AdaptorBill.STATUS_PAYED, AdaptorBill.STATUS_DELIVERIED,
     AdaptorBill.STATUS_FINISHED, AdaptorBill.STATUS_BAD]
    kwargs = {}
    kwargs['refundstatus'] = AdaptorBill.REFUNDAPPLY
    # 等到发货的记录
    kwargs['status'] = AdaptorBill.STATUS_PAYED
    bills = AdaptorBill.objects.filter( **kwargs ) #.order_by('refundstatus', '-refund_time')
    content['bills'] = bills
    

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
                        if len(result['code'].strip()) > 0 and len(result['company'].strip()) > 0:
                            bill.delivery_company = result['company'].strip()
                            bill.delivery_no = result['code'].strip()
                            bill.status = bill.STATUS_DELIVERIED
                            bill.delivery_date = timezone.now()
                            bill.save()
                            succeed_items.append(bill)
                            succeed += 1 
                        else:
                            failed += 1
                except AdaptorBill.DoesNotExist:
                    failed += 1

            content['status'] = 'ok'
            content['succeed'] = succeed
            content['failed'] = failed
            content['bills'] = succeed_items
        else:
            content['status'] = 'error'
            content['msg'] = '请选择发货模板文件...'
    else:
        # 等到发货的记录
        #kwargs['status'] = AdaptorBill.STATUS_PAYED
        #bills = AdaptorBill.objects.filter( **kwargs ) #.order_by('refundstatus', '-refund_time')
        #content['bills'] = bills
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
    if isMble:
        return render(request, 'usercenter/usercenter_deliverybill.html', content)
    else:
        return render(request, 'usercenter/usercenter_deliverybill.html', content)


@login_required
def sales(request):
    """
    销售统计 
    """
    user = request.user
    perm = user.has_perm('bill.manage_bill')
    if not perm:
        return HttpResponse("403")
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

@login_required
def refundlist(request):
    """
    退款列表 
    可以查看：正在申请的、已经同意的和已经拒绝的
    """
    user = request.user
    perm = user.has_perm('bill.manage_bill')
    if not perm:
        return HttpResponse("403")
    isMble  = dmb.process_request(request)
    content = {}  
    refund_status = [AdaptorBill.REFUNDWAITING, AdaptorBill.REFUNDAGREE,
     AdaptorBill.REFUNDREFUSED]

    kwargs = {}
    kwargs, content = search(request)
    if 'refundstatus' in request.GET:
        refundstatus = request.GET['refundstatus'].strip()
        if len(refundstatus) > 0 and refundstatus != '-1':
            content['refundstatus'] = refundstatus
            kwargs['refundstatus'] = refundstatus
        else:
            kwargs['refundstatus__in'] = refund_status
    else:
        kwargs['refundstatus__in'] = refund_status
    
    if 'datefrom' in request.GET:
        datefrom = request.GET['datefrom'].strip()
        if len(datefrom) > 0:
            datefrom = datetime.strptime(datefrom, "%Y-%m-%d")
            kwargs['refund_time__gte'] = datefrom
            content['datefrom'] = datefrom.strftime("%Y-%m-%d")
    
    if 'dateto' in request.GET:
        dateto = request.GET['dateto'].strip()
        if len(dateto) > 0:
            dateto = datetime.strptime(dateto, "%Y-%m-%d")
            content['dateto'] = dateto.strftime("%Y-%m-%d")
            dateto = dateto + timedelta(days=1)
            kwargs['refund_time__lte'] = dateto
            

    bills = AdaptorBill.objects.filter( **kwargs ).order_by('refundstatus', '-refund_time')
    if 'print' in request.GET:
        userid = request.user.id
        if not os.path.isdir(settings.BASE_FILE_PATH):
            os.makedirs(settings.BASE_FILE_PATH)

        filename = os.path.join(settings.BASE_FILE_PATH,'退款.xls' )
        kwargs = {}
        kwargs['filename'] = filename 
        kwargs['bills'] = bills 
        out_excel = excel_output.write_refund_record(**kwargs)
    
        if os.path.isfile(filename):
            try:
                wrapper  = FileWrapper(open(filename, 'rb'))
            except IOError as e:
                return HttpResponse(e)
            print(kwargs['filename'])    
            response    = HttpResponse(wrapper,content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'inline; filename=退款.xls'  
            response['Content-Length']      = os.path.getsize(filename)
            return response
        else:
            return HttpResponse(u'未找到文件...')
    # 分页开始
    counter = len(bills)
    pagenation = False
    if counter > settings.PAGEINDEX : # 需要分页时才分页 
        pagenation = True
        i, j = divmod(counter, settings.PAGEINDEX)
        if j > 0:
            i = i + 2
        else:
            i = i + 1
        content['maxpage'] = i - 1
        content['pages'] = range(1, i)
        print(content['pages'] )
        page = 1
        if 'page' in request.GET:
            try:
                page = int(request.GET['page'])
                if page <= 0:
                    page = 1
            except ValueError:
                pass 
        content['page'] = page
        bills = bills[(page - 1) * settings.PAGEINDEX : page*settings.PAGEINDEX ]
    content['pagenation'] = pagenation
    # 分页结束
    
    content['mediaroot'] = settings.MEDIA_URL
    content['bills'] = bills
    content['menu'] = 'refundlist'  
    if isMble:
        return render(request, 'usercenter/usercenter_refundlist.html', content)
    else:
        return render(request, 'usercenter/usercenter_refundlist.html', content)
    
def search(request):
    """
    搜索：销售订单和退款用的搜索都是这个。
    """
    kwargs = {}
    content = {}
    
    if 'billno' in request.GET:
        billno = request.GET['billno'].strip()
        if len(billno) > 0:
            content['billno'] = billno
            kwargs['no__icontains'] = billno
    
    if 'phone' in request.GET:
        phone = request.GET['phone'].strip()
        if len(phone) > 0:
            content['phone'] = phone 
            kwargs['phone__icontains'] = phone
    
    if 'name' in request.GET:
        name = request.GET['name'].strip()
        content['name'] = name
        billids = []
        if len(name) > 0:
            items = AdaptorBillItem.objects.filter(product__title__icontains = name)
            for item in items:
                if item.bill.id not in billids :
                    billids.append(item.bill.id) 
            kwargs['id__in'] = billids
    
    
    
    return kwargs, content 