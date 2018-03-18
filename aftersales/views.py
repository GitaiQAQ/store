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

from sitecontent.comm import handle_uploaded_file
from aftersales.models import AdaptorAfterSales as AfterSales
from aftersales.models import AdaptorMainainCode as MainainCode
from aftersales.models import Notify  
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
       
        service_man = user.has_perm('aftersales.aftersaler_code')
         
        content['menu'] = 'service'    
        if service_man:# 客服人员
            kwargs = {}
            if 'code' in request.GET and 'phone' in request.GET:
                code = request.GET['code'].strip() 
                phone = request.GET['phone'].strip() 
                if code:
                    kwargs['code'] = code
                    content['code'] = code
                if phone:
                    kwargs['phone'] = phone
                    content['phone'] = phone
 
            if kwargs:
                codes = MainainCode.objects.filter(**kwargs)
            else:
                codes = MainainCode.objects.all()
            notifies = Notify.objects.all()


            if len(notifies) > 0:
                content['address'] = notifies[0].address
                 
            content['codes'] = codes
             
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
            codes = MainainCode.objects.filter(phone = user.phone)
            #content['aftersale_items'] = aftersale_items 
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
        """创建预约号""" 
        # 创建时：
        user = request.user
        result = {} 
        
        if 'phone' in request.POST : 
            phone = request.POST['phone'].strip() 
            address = request.POST['address'].strip() 
            if address:
                notifies = Notify.objects.all()
                notifies.delete()
                Notify.objects.create(address=address)
            code  = 'A'
            code += datetime.now().strftime('%Y%m%d') 
            today = datetime.today().date() 
            yestoday = today + timedelta(days = -1)
            mainaincodes = MainainCode.objects.filter(date__gt = yestoday) 
            counter = len(mainaincodes)
            counter += 1 
            if counter < 10:
                num = str(counter).zfill(4)
            elif counter < 100:
                num = str(counter).zfill(3)
            elif counter < 1000:
                num = str(counter).zfill(2)
            else:
                num = str(counter)
            
            code += num
            print(code)
 
            maintaincode = MainainCode.objects.create(creator=user,  phone = phone, code = code ) 
            maintaincode.save()

            # 发送验证寄修短信信息
            content = "预约服务号："+code+" 寄修信息："+address+"【" + settings.PROJECTNAME + "】"
            req = requests.get(settings.SMS_API.format(phone,content)) 
        
            result['code'] = maintaincode.code
            result['status'] ='ok'
            result['msg'] = "提交成功..." 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'

        return self.httpjson(result)
    
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
        
        user = request.user
        service_man = user.has_perm('aftersales.aftersaler_code') 
        if service_man:# 售后客服人员直接进入预约码页面
            return redirect('/aftersales/maintaincode')

        isMble  = dmb.process_request(request)
        content = {} 
        aftersale_items = AfterSales.objects.filter(user = user, deleted = 0)
 
        # 已完成的或者已发货的订单可以发起售后
        finished_bills = AdaptorBill.objects.filter(owner = user, \
                   #status__in = (AdaptorBill.STATUS_DELIVERIED, AdaptorBill.STATUS_FINISHED))
                   status__in = (AdaptorBill.STATUS_DELIVERIED, AdaptorBill.STATUS_SUBMITTED, AdaptorBill.STATUS_FINISHED))
     
        content['aftersale_items'] = aftersale_items
        content['mediaroot'] = settings.MEDIA_URL
        
        for finished_bill in finished_bills:
            finished_bill.item = []
            for item in finished_bill.adaptorbillitem_set.all(): 
                sales = AfterSales.objects.filter(bill_item = item, user = user)
          
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
            content['choices'] = AfterSales.AFTERSALES_CHOICES
            if isMble:
                return render(request, 'aftersales/usercenter_apply.html', content)
            else:
                return render(request, 'aftersales/usercenter_apply.html', content)
        elif 'aftersaleid' in request.GET : 
            aftersaleid = request.GET['aftersaleid']
            
            if 'status' in request.GET: # 发货
                status = request.GET['status']
                code = ''
                try:
                    aftersale = AfterSales.objects.get(id = aftersaleid)
                    if aftersale.status == AfterSales.START:
                        # 刚填写了信息，还没有输入预约号码
                        # 现在系统自动匹配预约号码
                        # 本人未使用的
                        codes = MainainCode.objects.filter(phone = user.phone, used = 0)
                        if len(codes) > 0:
                            code = codes[0].code
                            codes[0].used = 1
                            codes[0].save()

                            aftersale.maintain_code = codes[0]
                            aftersale.status = AfterSales.CODE
                            aftersale.code_date = datetime.today()
                            aftersale.save()
                    elif aftersale.status == AfterSales.CODE:
                        # 已经获得预约服务号
                        code = aftersale.maintain_code.code
                    elif aftersale.status == AfterSales.DELIVERIED:
                        # 已发货
                        code = aftersale.maintain_code.code
                    else:
                        # 已完成
                        code = aftersale.maintain_code.code
                        
                except AfterSales.DoesNotExist:
                    aftersale = []
                content['aftersale'] = aftersale
                content['code'] = code
                if isMble:
                    return render(request, 'aftersales/usercenter_delivery.html', content)
                else:
                    return render(request, 'aftersales/usercenter_delivery.html', content)
            elif 'detail' in request.GET: # 查看售后详情 
                try:
                    aftersale = AfterSales.objects.get(id = aftersaleid)
                except AfterSales.DoesNotExist:
                    aftersale = []
                content['aftersale'] = aftersale
                if isMble:
                    return render(request, 'aftersales/usercenter_detail.html', content)
                else:
                    return render(request, 'aftersales/usercenter_detail.html', content)
        else: 
            content['aftersales'] = aftersale_items
            if isMble:
                return render(request, 'aftersales/usercenter_aftersales_list.html', content)
            else:
                return render(request, 'aftersales/usercenter_aftersales_list.html', content)
    
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
            
            logistics_name = request.POST['logistics_name'].strip() # 物流公司名称
            logistics_nub = request.POST['logistics_nub'].strip() # 物流单号
            if logistics_name and logistics_nub:
                aftersaleid = request.POST['aftersaleid']  
                aftersale = AfterSales.objects.get(id = aftersaleid)  

                if 'pictrue' in request.FILES:
                    code    = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(4))
                    filename = handle_uploaded_file(request.FILES['pictrue'], str(user.id)+'_'+ code)
                    aftersale.delivery_pic = filename
    
                aftersale.status = AfterSales.DELIVERIED
                aftersale.delivery_company = logistics_name
                aftersale.delivery_number = logistics_nub

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
            
            aftersale = AfterSales.objects.create(user=user, name=name,
                        phone = phone,  back_addr=back_addr, proudct_code = proudct_code,
                        buy_date = buy_date, description = description, service_type=service_type )
            
            if 'email' in request.POST  :
                email = request.POST['email'].strip()
                aftersale.email = email
    
            if 'color' in request.POST:
                device_color = request.POST['color'].strip() 
                aftersale.device_color = device_color

            if 'dealer' in request.POST:
                saller = request.POST['dealer'].strip() 
                aftersale.saller = saller
            
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


