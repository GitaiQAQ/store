#! -*- coding:utf-8 -*-
import json
import pdb

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from address.models import Address
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from area.models      import  Area
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
dmb     = DetectMobileBrowser()
bigcity = ['110100', '120000', '310000', '500000']
class AddressView(View):
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {}
        addresses = Address.objects.filter(user = request.user)
        content['addresses'] = addresses
        content['menu'] = 'address'
        
        if 'new' in request.GET:
            if 'template' in request.GET:
                provinces = Area.objects.filter(Q(level = 1) | Q(name='北京市'))
                content['provinces'] = provinces
                if isMble:
                    return render(request, 'address_template/m_new.html', content)
                else:
                    return render(request, 'address_template/m_new.html', content)
            else:
                if isMble:
                    return render(request, 'address/m_new.html', content)
                else:
                    return render(request, 'address/new.html', content)
        if 'addressid' in request.GET:
            addressid = request.GET['addressid']
            
            try:
                address = Address.objects.get(user = request.user, id = addressid)
                content['address'] = address
                 
            except Address.DoesNotExist:
                pass
            if 'template' in request.GET: 
                provinces = Area.objects.filter(Q(level = 1) | Q(name='北京市'))
                cities = Area.objects.filter(id = address.area.parent_id)
                counties = Area.objects.filter(parent_id = address.area.parent_id)
                content['provinces'] = provinces
                content['cities'] = cities
                content['counties'] = counties
                
                city = Area.objects.get(id = address.area.parent_id)
                if str(city.id) in bigcity:
                    # 直辖市
                    province = city
                else:
                    province = Area.objects.get(id = city.parent_id)
                content['address_provice'] = province.id
                content['address_city'] = address.area.parent_id
                content['address_county'] = address.area.id


                return render(request, 'address_template/m_new.html', content)
            else: 
                if isMble:
                    return render(request, 'address/m_new.html', content)
                else:
                    return render(request, 'address/new.html', content)
        else: 
            if 'template' in request.GET:
                content['addresses'] = addresses[:3]
                if isMble :
                    return render(request, 'address_template/m_address.html', content)
                else:
                    return render(request, 'address_template/address.html', content)
            else:
                if isMble :
                    return render(request, 'address/m_address.html', content)
                else:
                    return render(request, 'address/address.html', content)
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        新建地址名称
        """
        result = {}
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                return self.put(request)
            elif method == 'delete': # 删除
                return self.delete(request)
            
        # 新建类别
        # name字段是必须的；如果提供了parentid，则新的类别为parent类别的子类别
        # 否则添加为父类别
        if 'areaid' in request.POST and 'phone' in request.POST \
           and 'receiver' in request.POST and 'detail' in request.POST: 
            areaid = request.POST['areaid'].strip()
            phone = request.POST['phone'].strip()
            receiver = request.POST['receiver'].strip()
            detail = request.POST['detail'].strip() 
            address = Address.objects.create(user = request.user, area_id=areaid, phone=phone, 
                                           receiver=receiver, detail = detail)
            if 'default' in request.POST: 
                default = request.POST['default']
                if default == '1':
                    address.default = 1  
                    addresses = Address.objects.filter(user=request.user)
                    addresses.update(default = 0)
 
            result['id'] = address.id
            result['status'] ='ok'
            result['msg'] ='保存成功'
        else:
            result['status'] ='error'
            result['msg'] ='Need name in POST'
   
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    def put(self, request):
        """
        修改地址名称
        """
        result = {}  
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            addressid = data['id']
            try:
                address = Address.objects.get(id=addressid)
                if 'areaid' in data:
                    areaid = data['areaid']
                    address.area_id = areaid
                if 'phone' in data:
                    phone = data['phone']
                    address.phone = phone
                if 'receiver' in data:
                    receiver = data['receiver']
                    address.receiver = receiver
                if 'detail' in data:
                    detail = data['detail']
                    address.detail = detail 
                if 'default' in data: 
                    default = data['default']
                    if default == '1':
                        address.default = 1
                        addresses = Address.objects.filter(user=request.user) 
                        addresses.update(default = 0)

                address.save()
             
                result['status'] ='ok'
                result['msg'] ='保存成功'
            except Address.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id'
     
        else:
            result['status'] ='error'
            result['msg'] ='Need name and id  in POST'

        return HttpResponse(json.dumps(result), content_type="application/json")

    def delete(self, request):
        """
        删除指定地址
        """
        result = {}
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            addressid = data['id'] 
            try: 
                address = Address.objects.get(id=addressid) 
                address.delete() 
                result['status'] ='ok'
                result['msg'] ='已完成'
            except Address.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id' 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return HttpResponse(json.dumps(result), content_type="application/json")
