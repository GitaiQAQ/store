#! -*- coding:utf-8 -*-
import pdb
import json
import random
import string
import os
import uuid
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
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.urls import reverse
import requests
from django.core.exceptions import ValidationError

from coupon.models import AdaptorCoupon as Coupon
from category.models import Category

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
dmb     = DetectMobileBrowser()


class CouponView(View):
    """
    优惠劵类
    """
    @method_decorator(login_required)
    def get(self, request):
        content = {} 
        user = request.user
        isMble  = dmb.process_request(request)
        perm = user.has_perm('coupon.manager_coupon') 
         
        content['menu'] = 'coupon'
        coupons = self.pagination(request) 
        content['coupons'] =coupons
        if perm:# 管理人员 
            content['categories'] = self.get_categories()
            if isMble:
                return render(request, 'coupon/lists.html', content)
            else:
                return render(request, 'coupon/lists.html', content) 
        else: # 普通用户查看自己的优惠劵
            if isMble:
                return render(request, 'coupon/mycoupon.html', content)
            else:
                return render(request, 'coupon/mycoupon.html', content)

         
    def get_categories(self, ids = []):
        if ids :
            categories = Category.objects.filter(level = Category.TOP_LEVEL, id__in = ids) 
        else:
            categories = Category.objects.filter(level = Category.TOP_LEVEL) 
        return categories
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request ): 
        user = request.user
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
            perm = user.has_perm('coupon.manager_coupon') 
            if perm:
                # 创建优惠劵
                return self.create(request)
            
    def create(self, request):
        """创建寄修服务单""" 
        # 创建时：
        user = request.user
        result = {} 
        isMble  = dmb.process_request(request)
        result['categories'] = self.get_categories()
        
        if 'money' in request.POST and 'num' in request.POST and 'rule' in request.POST and \
            'date' in request.POST and 'categories' in request.POST : 

            money = request.POST['money'].strip() 
            rule = request.POST['rule'].strip() 
            try:
                num = int(request.POST['num'].strip() )
            except :
                result['status'] ='error'
                result['msg'] ='优惠劵数量不正确'
                coupons = self.pagination(request)
                result['coupons'] =coupons
                if isMble:
                    return render(request, 'coupon/lists.html', result) 
                else:
                    return render(request, 'coupon/lists.html', result)

            date = request.POST['date'].strip() 
            category_ids = request.POST.getlist('categories') #产品系列号
            categories = self.get_categories(category_ids)

            # 64 位UUID作为优惠劵号码
            for i in range(num): 
                code = uuid.uuid1().int>>64  
                while True:
                    # 防止优惠码出现重复的情况，
                    # 当出现重复情况之后，再次生成新的，直到没有重复的
                    try:
                        coupon = Coupon.objects.create(code = code, price=money, 
                            creator=user, deanline=date, rule = rule)
                  
                        coupon.categories.add(*list(categories))
                        break
                    except IntegrityError:
                        code = uuid.uuid1().int>>64 
                    except ValidationError as e:
                        result['status'] ='error'
                        result['msg'] = e
                        break 
            result['status'] ='ok'
            result['msg'] = "创建成功..." 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'
    

        coupons = self.pagination(request)
        result['coupons'] =coupons
        if isMble:
            return render(request, 'coupon/lists.html', result) 
        else:
            return render(request, 'coupon/lists.html', result) 
    
    def pagination(self, request):
        page = 1
        if 'page' in request.GET:
            try:
                pageindex = request.GET['page'].strip() 
                page = int(pageindex)
            except :
                pass
        
        pagenum = 20 
        coupons = Coupon.objects.all()[(page-1)*pagenum : page*pagenum]
        return coupons

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



