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
from django.utils  import timezone
from coupon.models import AdaptorCoupon as Coupon
from category.models import Category
from product.models import AdaptorRule as Rule

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
        if 'used' in request.GET:
            used = request.GET['used']
            content['used'] = used

        if 'number' in request.GET and 'items' in request.GET:
            result = {}
            number = request.GET['number']
            items = json.loads(request.GET['items'])
            
            try:
                coupon = Coupon.objects.get(code = number)
                # 判断：1 是否已使用；2 判断是否过期； 3 判断是否本订单可用
                # 1 判断是否已使用
                if coupon.used == 1: # 已使用
                    result['status'] = 'error'
                    result['msg'] = '该优惠劵已使用...' 
                else:
                    # 2 判断是否已过期
                    now = timezone.now()
                    if coupon.deadline < now:
                        result['status'] = 'error'
                        result['msg'] = '该优惠劵已过期...'
                    else:
                        bill_categoryid = set()
                        for item in items: 
                            rule = Rule.objects.get(id = item['ruleid'])
                            bill_categoryid.add(rule.product.category.id)
                        
                        coupon_categoriesid = set()
                        
                        coupon_categories = coupon.categories.all()
                        for category in coupon_categories: 
                            coupon_categoriesid.add(category.id) 
            
                        if bill_categoryid < coupon_categoriesid or bill_categoryid == coupon_categoriesid:
                            result['status'] = 'ok'
                            result['price'] =  str(coupon.price)
                        else:
                            result['status'] = 'error'
                            result['msg'] = '该优惠劵不能在本次订单中使用，使用规则：' + coupon.rule
                        
            except Coupon.DoesNotExist:
                result['status'] = 'error'
                result['msg'] = '该优惠劵不存在...'
            
            return self.httpjson(result)
        
        if perm:# 管理人员 
            now = timezone.now()
            unused_coupons = Coupon.objects.filter(used = 0)
            for coupon_item in unused_coupons:
                if coupon_item.deadline < now:
                    coupon_item.used = 2
                    coupon_item.save()

            coupons = self.pagination(request) 
            content['coupons'] =coupons
            content['categories'] = self.get_categories()
            if isMble:
                return render(request, 'coupon/lists.html', content)
            else:
                return render(request, 'coupon/lists.html', content) 
        else: # 普通用户查看自己的优惠劵
            coupons = Coupon.objects.filter(owner = user)
            content['coupons'] = coupons
            if isMble:
                return render(request, 'coupon/mycoupon.html', content)
            else:
                return render(request, 'coupon/mycoupon.html', content)

    def sublist(self, lst1, lst2):
        ls1 = [element for element in lst1 if element in lst2]
        ls2 = [element for element in lst2 if element in lst1]
        return ls1 == ls2     

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
                return self.put(request) 
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
        """创建优惠劵""" 
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
                            creator=user, deadline=date, rule = rule)
                  
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
        """
        分页
        """
        page = 1
        if 'page' in request.GET:
            try:
                pageindex = request.GET['page'].strip() 
                page = int(pageindex)
            except :
                pass
        
        pagenum = 20 
        if 'used' in request.GET:
            used = request.GET['used']
            coupons = Coupon.objects.filter(used = used)[(page-1)*pagenum : page*pagenum]
        else:
            coupons = Coupon.objects.all()[(page-1)*pagenum : page*pagenum]
        return coupons

    def put(self, request):
        """激活优惠券""" 
        user = request.user
        isMble  = dmb.process_request(request)
        result = {}
        if 'code' in request.POST : 
            code = request.POST['code'].strip() 

            # 查找未使用的code
            try:
                coupon = Coupon.objects.get(code = code, used = 0)
                coupon.owner =  user
                coupon.save()
                result['status'] ='ok'
                result['msg'] = '激活成功...'
            except Coupon.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='激活失败...'
             
            coupons = Coupon.objects.filter(owner = user)
            result['coupons'] = coupons 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'

        if isMble:
            return render(request, 'coupon/mycoupon.html', result) 
        else:
            return render(request, 'coupon/mycoupon.html', result)

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



