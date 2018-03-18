#! -*- coding:utf-8 -*-
import pdb
import json
import random
import string
import os
from datetime import datetime
from datetime import timedelta

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
from django.shortcuts import redirect
from django.urls import reverse
import requests
 
from coupon.models import AdaptorCoupon as Coupon
 

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
dmb     = DetectMobileBrowser()


class CouponView(View):
    """
    优惠劵类
    """
    @method_decorator(login_required)
    def get(self, request): 
        user = request.user
        service_man = user.has_perm('aftersales.aftersaler_code') 
        if service_man:# 售后客服人员直接进入预约码页面
            return redirect('/aftersales/maintaincode')

        isMble  = dmb.process_request(request)
           
        if isMble:
            return render(request, 'coupon/usercenter_aftersales_list.html', content)
        else:
            return render(request, 'coupon/usercenter_aftersales_list.html', content)
    
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
            if 'aftersaleid' in request.POST:
                return self.add_delivery_info(request)
            else:
                self.create(request)
                return self.get(request)

    def add_delivery_info(self, request):
        """
        添加货运信息
        """
        user = request.user
        result = {} 
        isMble  = dmb.process_request(request)
        if 'logistics_name' in request.POST and 'logistics_nub' in request.POST  :
            
            logistics_name = request.POST['logistics_name'].strip() # 
            if logistics_name and logistics_nub:
                aftersaleid = request.POST['aftersaleid']  
                aftersale = AfterSales.objects.get(id = aftersaleid)  

                if 'pictrue' in request.FILES:
                    code    = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(4))
                    filename = handle_uploaded_file(request.FILES['pictrue'], str(user.id)+'_'+ code)
                    aftersale.delivery_pic = filename
     
                aftersale.delivery_date = datetime.today()
                aftersale.save()

                result['status'] ='ok'
                result['msg'] = "提交成功..." 
                if isMble:
                    return render(request, 'aftersales/usercenterl_apply_done.html', result)
                else:
                    return render(request, 'aftersales/usercenterl_apply_done.html', result)
            else:
                result['status'] ='error'
                result['msg'] ='请填写物流公司和物流单号...'
                if isMble:
                    return render(request, 'aftersales/usercenter_delivery.html', result)
                else:
                    return render(request, 'aftersales/usercenter_delivery.html', result)
        else:
            result['status'] ='error'
            result['msg'] ='Need logistics_name and logistics_nub  in POST'

        

    def create(self, request):
        """创建寄修服务单""" 
        # 创建时：
        user = request.user
        result = {} 
        isMble  = dmb.process_request(request)

        if 'name' in request.POST and 'phone' in request.POST and \
            'address' in request.POST and 'number' in request.POST and \
             'date' in request.POST and  'description' in request.POST and \
             'service_type' in request.POST : 

            name = request.POST['name'].strip() 
            phone = request.POST['phone'].strip() 
            back_addr = request.POST['address'].strip() 

            proudct_code = request.POST['number'].strip() #产品系列号
            buy_date = request.POST['date'].strip()  #购买日期
            description = request.POST['description'].strip() 

            service_type = request.POST['service_type']
            
            aftersale = AfterSales.objects.create(user=user )
            
         
            if 'invoice' in request.FILES:
                code    = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(4))
                filename = handle_uploaded_file(request.FILES['invoice'], str(user.id)+'_'+ code)
                aftersale.invoice = filename
            
            if 'rule' in request.POST:
                device_type = request.POST['rule'].strip() 
                aftersale.device_type = device_type
            
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
        if 'aftersalsesid' in request.POST : 
            aftersalsesid = request.POST['aftersalsesid'].strip() 
            try:
                aftersale = AfterSales.objects.get(pk = aftersalsesid)
                aftersale.deleted  = 1 # 非真正删除
                aftersale.save() 
                result['status'] ='ok'
                result['msg'] = "已删除..."
            except AfterSales.DoesNotExist:
                result['status'] ='error'
                result['msg'] = _('Not found')
        else:
            result['status'] ='error'
            result['msg'] = 'Need aftersalsesid  in POST'
        
        return self.httpjson(result)

    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")



