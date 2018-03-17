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
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.utils.translation import ugettext as _
 
from sitecontent.comm import handle_uploaded_file
from aftersales.models import AdaptorAfterSales as AfterSales
from aftersales.models import AdaptorMainainCode as MainainCode
from bill.models import AdaptorBill, AdaptorBillItem

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
dmb     = DetectMobileBrowser()

class MainainCodeView(View):
    """
    寄修预约号码
    """
    @method_decorator(login_required)
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        user = request.user
        aftersale_items = MainainCode.objects.filter(user = user)
        service_man = user.has_perm('aftersales.aftersaler_code')
        if service_man:# 客服人员
            content['aftersale_items'] = aftersale_items
             
            if 'new' in request.GET:
                if isMble:
                    return render(request, 'maintaincode/usercenter.html', content)
                else:
                    return render(request, 'maintaincode/usercenter.html', content)
            else:
                if isMble:
                    return render(request, 'maintaincode/lists.html', content)
                else:
                    return render(request, 'maintaincode/lists.html', content)
        else:
            content['aftersale_items'] = aftersale_items 
            if 'new' in request.GET:
                if isMble:
                    return render(request, 'maintaincode/usercenter.html', content)
                else:
                    return render(request, 'maintaincode/usercenter.html', content)
            else:
                if isMble:
                    return render(request, 'maintaincode/lists.html', content)
                else:
                    return render(request, 'maintaincode/lists.html', content)
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request ): 
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                self.put(request)
                return   self.get(request)
            elif method == 'create': # 创建
                return self.create(request) 
            elif method == 'delete': # 删除
                return self.delete(request) 
        else:
            self.create(request)
            return self.get(request)

    def create(self, request):
        """创建寄修服务单""" 
        # 创建时：
        user = request.user
        result = {} 
        
        if 'phone' in request.POST : 
            phone = request.POST['phone'].strip() 
            code  = ''.join(random.choice(string.digits) for i in range(6))
            code += datetime.now().strftime('%Y%m%d%H%M%S') 
 
            maintaincode = MainainCode.objects.create(creator=user, name=name,
                        phone = phone, code = code ) 
            maintaincode.save()
            result['code'] = maintaincode.code
            result['status'] ='ok'
            result['msg'] = "提交成功..." 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'

        if isMble:
            return render(request, 'maintaincode/detail.html', result)
        else:
            return render(request, 'maintaincode/detail.html', result)
    
    def put(self, request):
        """修改""" 
        # 修改时：blockid字段是必须的,title\url\pic\mark\status是可选字段
        user = request.user
        result = {}
        if 'blockid' in request.POST : 
            blockid = request.POST['blockid'].strip() 

            # 创建Block 
            aftersale = models.AdaptorBaseBlock.objects.get(pk = blockid)
            
            if  'title' in request.POST  :
                title = request.POST['title'].strip()
                aftersale.title = title
            
            if 'pic' in request.FILES:
                pic = request.FILES['pic'] 
                pic_url = handle_uploaded_file(pic, user.id)
                aftersale.pic = pic_url

            if  'url' in request.POST  :
                url = request.POST['url'].strip()
                aftersale.url = url
            
            if 'mark' in request.POST:
                mark = request.POST['mark'].strip() 
                if mark:
                    aftersale.mark = mark
            
            if 'status' in request.POST:
                status = request.POST['status'].strip()   
                aftersale.status = int(status)
            
            aftersale.save()
            result['id'] = aftersale.id
            result['status'] ='ok'
            result['msg'] = _('Saved completely!') 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'
        return self.httpjson(result)

    def delete(self, request):
        user = request.user
        result = {}
        if 'id' in request.POST : 
            aftersales_id = request.POST['id'].strip() 
            try:
                aftersale = AfterSales.objects.get(pk = aftersales_id)
                aftersale.delete()
                result['status'] ='ok'
                result['msg'] = "已删除..."
            except AfterSales.DoesNotExist:
                result['status'] ='error'
                result['msg'] = _('Not found')
        else:
            result['status'] ='error'
            result['msg'] = 'Need title  in POST'
        
        return self.httpjson(result)

    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")




class AfterSalesView(View):
    """
    售后服务类
    """
    @method_decorator(login_required)
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        aftersale_items = AfterSales.objects.filter(user = request.user)
        
        # 已完成的或者已发货的订单可以发起售后
        finished_bills = AdaptorBill.objects.filter(owner = request.user, \
                   #status__in = (AdaptorBill.STATUS_DELIVERIED, AdaptorBill.STATUS_FINISHED))
                   status__in = (AdaptorBill.STATUS_DELIVERIED, AdaptorBill.STATUS_SUBMITTED, AdaptorBill.STATUS_FINISHED))
     
        content['aftersale_items'] = aftersale_items
        content['mediaroot'] = settings.MEDIA_URL
        
        for finished_bill in finished_bills:
            finished_bill.item = []
            for item in finished_bill.adaptorbillitem_set.all(): 
                sales = AfterSales.objects.filter(bill_item = item, user = request.user)
          
                if len( sales ) == 0: 
                    item.status = AfterSales.STATUS_CHOICES[AfterSales.START][1]
                elif len( sales ) == 1:
                    item.status = AfterSales.STATUS_CHOICES[sales[0].status][1]
                else: 
                    item.status = "未知售后状态"
                
                finished_bill.item.append(item)

        content['bills'] = finished_bills
        content['menu'] = 'service'
        if 'new' in request.GET:
            if isMble:
                return render(request, 'aftersales/usercenter.html', content)
            else:
                return render(request, 'aftersales/usercenter.html', content)
        else:
            if isMble:
                return render(request, 'usercenter/usercenter_aftersales_list.html', content)
            else:
                return render(request, 'usercenter/usercenter_aftersales_list.html', content)
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request ): 
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                self.put(request)
                return   self.get(request)
            elif method == 'create': # 创建
                return self.create(request) 
            elif method == 'delete': # 删除
                return self.delete(request) 
        else:
            self.create(request)
            return self.get(request)

    def create(self, request):
        """创建寄修服务单""" 
        # 创建时：
        user = request.user
        result = {} 
        
        if 'name' in request.POST and 'phone' in request.POST and \
            'back_addr' in request.POST and 'proudct_code' in request.POST and \
             'buy_date' in request.POST and  'description' in request.POST and \
             'service_type' in request.POST : 

            name = request.POST['name'].strip() 
            phone = request.POST['phone'].strip() 
            back_addr = request.POST['back_addr'].strip() 

            proudct_code = request.POST['proudct_code'].strip() 
            buy_date = request.POST['buy_date'].strip() 
            description = request.POST['description'].strip() 
 
            aftersale = AfterSales.objects.create(user=user, name=name,
                        phone = phone,  back_addr=back_addr, proudct_code = proudct_code,
                        buy_date = buy_date, description = description )
            
            if 'email' in request.POST  :
                email = request.POST['email'].strip()
                aftersale.email = email
  
            if 'invoice' in request.FILES:
                invoice = request.FILES['invoice'] 
                invoice_url = handle_uploaded_file(invoice, user.id)
                aftersale.invoice = invoice_url

            if 'device_color' in request.POST:
                saller = request.POST['device_color'].strip() 
                aftersale.device_color = device_color

            if 'saller' in request.POST:
                saller = request.POST['saller'].strip() 
                aftersale.saller = saller
             
            aftersale.save()
            result['id'] = aftersale.id
            result['status'] ='ok'
            result['msg'] = "提交成功..." 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'

        if isMble:
            return render(request, 'aftersales/lists.html', result)
        else:
            return render(request, 'aftersales/lists.html', result)
    
    def put(self, request):
        """修改""" 
        # 修改时：blockid字段是必须的,title\url\pic\mark\status是可选字段
        user = request.user
        result = {}
        if 'blockid' in request.POST : 
            blockid = request.POST['blockid'].strip() 

            # 创建Block 
            aftersale = models.AdaptorBaseBlock.objects.get(pk = blockid)
            
            if  'title' in request.POST  :
                title = request.POST['title'].strip()
                aftersale.title = title
            
            if 'pic' in request.FILES:
                pic = request.FILES['pic'] 
                pic_url = handle_uploaded_file(pic, user.id)
                aftersale.pic = pic_url

            if  'url' in request.POST  :
                url = request.POST['url'].strip()
                aftersale.url = url
            
            if 'mark' in request.POST:
                mark = request.POST['mark'].strip() 
                if mark:
                    aftersale.mark = mark
            
            if 'status' in request.POST:
                status = request.POST['status'].strip()   
                aftersale.status = int(status)
            
            aftersale.save()
            result['id'] = aftersale.id
            result['status'] ='ok'
            result['msg'] = _('Saved completely!') 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'
        return self.httpjson(result)

    def delete(self, request):
        user = request.user
        result = {}
        if 'id' in request.POST : 
            aftersales_id = request.POST['id'].strip() 
            try:
                aftersale = AfterSales.objects.get(pk = aftersales_id)
                aftersale.delete()
                result['status'] ='ok'
                result['msg'] = "已删除..."
            except AfterSales.DoesNotExist:
                result['status'] ='error'
                result['msg'] = _('Not found')
        else:
            result['status'] ='error'
            result['msg'] = 'Need title  in POST'
        
        return self.httpjson(result)

    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")


