#! -*- coding:utf-8 -*-
import pdb
import json
import random
import string
import os
from datetime import datetime
from django.shortcuts import redirect 
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import Http404, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from category.models import Category
from product.models import AdaptorProduct, AdaptorRule, ProductPic,RuleName
from common.fileupload import FileUpload
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext  as _
from product.comm import handle_uploaded_file

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from django import forms
from basedatas.bd_comm import Common 

dmb     = DetectMobileBrowser()
comm    = Common()
dmb     = DetectMobileBrowser()

class AdaptorProductForm(forms.ModelForm):

    class Meta:
        model = AdaptorProduct
        fields = ('detail',)

@login_required 
@permission_required('product.manage_product')
def change(request, pk):
    isMble  = dmb.process_request(request)
    content = {}
    content['mediaroot'] = settings.MEDIA_URL
    categories = Category.objects.all()  
    content['categories'] = categories
    content['menu'] = 'product'

    if request.method == 'GET':
        try:
             product = AdaptorProduct.objects.get(pk=pk)
             content['product'] =product 
             form = AdaptorProductForm(instance=product)
             content['form'] = form
        except AdaptorProduct.DoesNotExist:
            raise Http404
        
        if 'pic' in request.GET:
            if isMble:
                return render(request, 'm_pic.html', content)
            else:
                return render(request, 'pic.html', content)
        else: 
            if 'categoryid' in request.GET:
                categoryid = request.GET['categoryid'].strip()
                category = Category.objects.get(id=categoryid)
            else:
                category = categories[0]
            content['category'] = category
            rulenames = RuleName.objects.filter(category = category)
            rulename = rulenames.filter(mainrule= True)[0]
            content['rulename'] = rulename.name
            
            rulename = rulenames.filter(mainrule= False)
            if len(rulename) > 0:
                content['vicerulename'] = rulename[0].name
            if isMble:
                return render(request, 'change.html', content)
            else:
                return render(request, 'change.html', content)

    return HttpResponse()
class ProductDetailView(APIView):
    """product detail"""
    model = AdaptorProduct
    def get_object(self, pk):
        try:
            return AdaptorProduct.objects.get(pk=pk)
        except AdaptorProduct.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        isMble  = dmb.process_request(request)
        
        content={
            'product':product
        }
        pics = product.productpic_set.exclude(url = product.thumbnail)

        content['mediaroot'] = settings.MEDIA_URL
        content['pics'] = pics
        if isMble:
            return render(request, 'm_detail.html', content)
        else:
            return render(request, 'detail.html', content)


    @method_decorator(csrf_exempt)
    def post(self, request, pk, format=None):
        product = self.get_object(pk)
         
        content={
            'product':product
        } 
        result = {}		 
        if request.method == 'POST': 
            user = request.user
            if 'method' in request.POST:
                method = request.POST['method']
                if method == 'delete':
                    picid = request.POST['picid']
                    productpic = ProductPic.objects.get(pk = picid)
                    productpic.delete()
                    result['status'] = 'OK'
                    result['msg']    = _('Delete sucessfully')#'删除成功...' 
            elif 'picid' in request.POST: # 说明是在设置主缩略图
                picid = request.POST['picid']
                productpic = ProductPic.objects.get(pk = picid)
                product.thumbnail = productpic.url 
                product.save()
                
                result['status'] = 'OK'
                result['msg']    = _('Config sucessfully') # '设置成功...'
            else: 
                code    = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(4))
                filename = handle_uploaded_file(request.FILES['pic'], str(user.id)+'_'+ code)
                
                ProductPic.objects.create(product=product, url=filename.replace('\\', '/'))
                
                result['status'] = 'OK'
                result['msg']    = _('Upload sucessfully')
        else:
            result['status'] = 'ERROR'
            result['msg']    = 'Method error..'
                  
        return HttpResponse(json.dumps(result), content_type='application/json')
         
   
class ProductView(View):

    @method_decorator(login_required)
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        products = AdaptorProduct.objects.filter(status__in = [0, 1, 2])
        categories = Category.objects.all()
        
        content['products'] = products
        content['categories'] = categories
        content['mediaroot'] = settings.MEDIA_URL 
         
        if 'keywords' in request.GET:
            keywords = request.GET['keywords'].strip()
            products = AdaptorProduct.objects.filter(title__icontains = keywords)
            content['products'] = products
         
        form = AdaptorProductForm()
        content['form'] = form
        if 'new' in request.GET:
            if  request.user.is_anonymous():
                return comm.redirect_login_path(isMble, request)
            if 'categoryid' in request.GET:
                categoryid = request.GET['categoryid'].strip()
                category = Category.objects.get(id=categoryid)
            else:
                category = categories[0]
            content['category'] = category
            rulenames = RuleName.objects.filter(category = category)
            rulename = rulenames.filter(mainrule= True)[0]
            content['rulename'] = rulename.name
            
            rulename = rulenames.filter(mainrule= False)
            if len(rulename) > 0:
                content['vicerulename'] = rulename[0].name
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'new.html', content)
        if 'newrule' in request.GET:
            rules = RuleName.objects.all()
            content['rules'] = rules
             
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'newrule.html', content)
        if 'pic' in request.GET:
            if isMble:
                return render(request, 'm_pic.html', content)
            else:
                return render(request, 'pic.html', content)
        if 'manage' in request.GET: 
            return render(request, 'lists.html', content)
        else:
            content['menu'] = 'product'
            if isMble:
                return render(request, 'm_lists.html', content)
            else:
                return render(request, 'lists.html', content)
 
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        新建产品
            下架：参数中带有method，并且值是'fallback'，大小写不敏感
                # # id【必须字段】：商品id 
            删除：参数中带有method，并且值是'delete'，大小写不敏感
                # # id【必须字段】：商品id 
            修改：参数中带有method，并且值是'put'，大小写不敏感
                # id【必须字段】：商品id 
                # title【可选字段】：商品名称 
                # categoryid【可选字段】： 商品所属类别ID 
                # unit【可选字段】： 商品的计量单位，如：个、只
                # price【可选字段】： 商品的计量单位，如：个、只
                # parameters【可选字段】： 商品的自定义规格，是一个json数据
                # detail【可选字段】： 商品的详情
            新建: 参数中带没有method，或method的值不等于put或者delete
                # title【必须字段】：商品名称 
                # categoryid【必须字段】： 商品所属类别ID 
                # unit【可选字段】： 商品的计量单位，如：个、只
                # price【可选字段】： 商品的计量单位，如：个、只
                # parameters【可选字段】： 商品的自定义规格，是一个json数据
                # detail【可选字段】： 商品的详情 
        """ 
        user = request.user
        perm = user.has_perm('product.manage_product')
        if not perm:
            return HttpResponse("403")
            
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                return self.put(request)
            elif method == 'delete': # 删除 
                if 'rulenameid' in request.POST:
                    # 删除规格 
                    rulenameid = request.POST['rulenameid'] 
                    RuleName.objects.get(id=rulenameid).delete()
                    return HttpResponse('ok')
                else:
                    return self.delete(request)
            elif method == 'fallback': # 下架
                return self.fallback(request)
            elif method == 'create': # 创建
                return self.create(request) 
        else:
            # 创建主规格 
            if 'title' in request.POST and 'categoryid' in request.POST :
                title = request.POST['title'].strip()
                categoryid = request.POST['categoryid'].strip()
                category = Category.objects.get(id=categoryid)  
                if 'mainrule' in request.POST:
                    mainrule = True 
                else:
                    mainrule = False
                rulename = RuleName.objects.create(name = title, category=category, mainrule=mainrule) 
                if mainrule:
                    RuleName.objects.set_main_rule(category, rulename) 
                return redirect('/product/products/?newrule')
            else:
                return HttpResponse('Error')
        
    
    def create(self, request):
        """创建"""
        # 新建商品
        # title\category字段是必须的
        user = request.user
        result = {}
        if 'title' in request.POST and 'categoryid' in request.POST: 
            title = request.POST['title'].strip()
            categoryid = request.POST['categoryid'].strip()
            
            # 创建商品
            try:
                category = Category.objects.get(id=categoryid)  
                product = AdaptorProduct.objects.create(user=user, title=title, 
                          category=category)
       
              
                if 'description' in request.POST:
                    description = request.POST['description'].strip()
                    product.description = description 
  
                 
                if 'mail_price' in request.POST:
                    mail_price = request.POST['mail_price'].strip()
                    product.mail_price = mail_price 
  
                if 'delivery_time' in request.POST:
                    delivery_time = request.POST['delivery_time'].strip() 
                    product.delivery_time = delivery_time

                if 'detail' in request.POST:
                    detail = request.POST['detail'].strip()
                    product.detail = detail
                
                if 'status' in request.POST:
                    status = request.POST['status'].strip()
                    product.status = status
                
                if 'taobaourl' in request.POST:
                    taobaourl = request.POST['taobaourl'].strip()
                    product.taobaourl = taobaourl
                 
                if 'rules' in request.POST:  
                    mainrulename = request.POST['mainrulename'].strip()
                    rules = request.POST['rules'].strip() 
                    AdaptorRule.objects.mul_mainrule_create(rules, product, mainrulename)
                if 'parameters' in request.POST: 
                    parameters = request.POST['parameters'].strip()
                    vicerulename = request.POST['vicerulename'].strip()
                    AdaptorRule.objects.mul_mainrule_create(parameters, product, vicerulename, mainrule=False)
                product.save()
                result['id'] = product.id
                result['status'] ='ok'
                result['msg'] = '创建成功...'
            except Category.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Category not found ID:{}'.format(categoryid)  
        else:
            result['status'] ='error'
            result['msg'] ='Need title and categoryid in POST'
        return self.httpjson(result)

    def put(self, request):
        """
        修改 
        """
        result = {}  
        data = QueryDict(request.body.decode('utf-8'))  
        if 'id' in data:
            productid = data['id']
            try:
                product = AdaptorProduct.objects.get(id=productid)
                if 'title' in data:
                    title = data['title']
                    product.title = title
                if 'categoryid' in data:
                    categoryid = data['categoryid']
                    try:
                        category = Category.objects.get(id = categoryid) 
                        product.category = category
                    except Category.DoesNotExist:
                        result['status'] = 'error' 
                        result['msg'] = 'Category not found, category id:{}'.format(categoryid) 
                        return self.httpjson(result)
                    
                if 'unit' in data:
                    unit = data['unit']
                    product.unit = unit
                if 'price' in data:
                    price = data['price']
                    product.price = price
              
                if 'description' in request.POST:
                    description = request.POST['description'].strip()
                    product.description = description 
                if 'detail' in data:
                    detail = data['detail']
                    product.detail = detail 
              
                if 'taobaourl' in request.POST:
                    taobaourl = request.POST['taobaourl'].strip()
                    product.taobaourl = taobaourl
                    
                if 'mail_price' in request.POST:
                    mail_price = request.POST['mail_price'].strip()
                    product.mail_price = mail_price 
  
                if 'delivery_time' in request.POST:
                    delivery_time = request.POST['delivery_time'].strip() 
                    product.delivery_time = delivery_time

                if 'rules' in request.POST:  
                    rules = request.POST['rules'].strip()
                    mainrulename = request.POST['mainrulename'].strip()
                    product.set_undeleted() 
                    AdaptorRule.objects.mul_modify(rules, product, mainrulename) 
                    product.delete_droped_rules() 
                
                if 'status' in request.POST:
                    status = request.POST['status'].strip()
                    product.status = status

                if 'parameters' in request.POST: 
                    parameters = request.POST['parameters'].strip()
                    vicerulename = request.POST['vicerulename'].strip()
                    AdaptorRule.objects.mul_modify(parameters, product, vicerulename, mainrule=False)

                product.save() 
                result['status'] ='ok'
                result['msg'] = '修改成功...'
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the Product ID:{}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id  in POST'


        return self.httpjson(result)

    def delete(self, request):
        """
        删除指定商品
        """
        result = {}
        data = QueryDict(request.body.decode('utf-8'))  
        if 'id' in data:
            productid = data['id'] 
            try: 
                product = AdaptorProduct.objects.get(id=productid)
                product.delete() 
                result['status'] ='ok'
                result['msg'] = _('Done sucessfully')
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id {}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return self.httpjson(result)

    def fallback(self, request):
        """下架商品"""
        result = {}
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            productid = data['id'] 
            try: 
                product = AdaptorProduct.objects.get(id=productid)
                AdaptorProduct.objects.fallback(product)
                result['status'] ='ok'
                result['msg'] = _('Done sucessfully')
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id {}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return self.httpjson(result)
 
    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")
