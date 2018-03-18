#! -*- coding:utf-8 -*-
import pdb

from django.db import models
from appuser.models import AdaptorUser as User 
from category.models import Category
from django.utils.translation import ugettext_lazy as _
from basedatas.models import BaseDate
from django.db.models import F
from bill.models import AdaptorBill, AdaptorBillItem

class MainainCode(BaseDate):
    """
    寄修预约号
    """
    creator = models.ForeignKey(User)
    # 格式：A日期+4位顺序码，A201307230001
    code = models.CharField('寄修预约号', max_length = 20, unique = True)
    phone = models.CharField('预约手机号码', max_length = 11)
    # 预约码是否使用
    # 默认0， 未使用，
    # 1 已使用
    used = models.SmallIntegerField(default = 0)
    class Meta:
        permissions = (
            ('aftersaler_code', u'售后客服-生成预约码'),
        ) 
        abstract = True
        ordering = ('used','-date')

class AdaptorMainainCode(MainainCode):
    """MainainCode 适配器"""
    def __str__(self):
        return self.code 

class Notify(models.Model):
    """
    售后生成预约码之后，会发短信给用户，短信里包含预约码+回寄地址，这个类中保存的就是回寄地址
    """
    # 回寄地址
    address = models.TextField()


class AfterSales(BaseDate):
    """
    售后服务  
    之
    维修信息
    """
    TURNBACK = 0 #7日内退机
    MAINTAIN_MAIN = 1 #返修主机
    MAINTAIN_SUB = 2 # 返修配件
    EXCHANGE = 3 # # 换机
 
    AFTERSALES_CHOICES = (
        (TURNBACK, '7日内退机'),
        (MAINTAIN_MAIN, '返修主机'),
        (MAINTAIN_SUB, '返修配件'),
        (EXCHANGE, '换机')
    )

    # 姓名
    name = models.CharField(_('name'), max_length = 128)
    phone = models.CharField(_('phone'), max_length = 11)
    email = models.CharField(_('email'), max_length = 128, null= True)
    back_addr = models.CharField('回寄地址', max_length = 1024)

    device_type = models.CharField('型号', max_length = 128, null= True)
    device_color = models.CharField('颜色', max_length = 56, null= True)
    proudct_code = models.CharField('产品序列号', max_length = 56)
    buy_date = models.DateTimeField('购买日期')
    saller = models.CharField('经销商', max_length = 128, null= True)

    invoice = models.CharField('发票路径', max_length = 128, null= True)
    delivery_company = models.CharField('物流公司名称', max_length = 128, null= True) 
    delivery_number = models.CharField('物流单号', max_length = 64, null= True)
    delivery_pic = models.CharField('物流单号图片路径', max_length = 128, null= True)
    # 故障描述
    description = models.TextField(null=True)
    # 返修类型
    service_type = models.CharField(max_length=2,
                choices=AFTERSALES_CHOICES, default = MAINTAIN_MAIN)

    # 创建者
    user = models.ForeignKey(User) 

    # 寄修预约码
    maintain_code = models.ForeignKey(AdaptorMainainCode, null=True) 
    
    # 待维修的商品，支持一个订单中不同的商品单独申请售后
    bill_item = models.ForeignKey(AdaptorBillItem, null=True) 
    
    # 输入预约码的时间
    code_date = models.DateTimeField( null=True)

    # 发货的时间
    delivery_date = models.DateTimeField( null=True)
 
    # 售后完成的时间
    finished_date = models.DateTimeField( null=True)

    # 默认0
    START = 0 # 发起
    CODE = 1 # 已获取寄修号码
    DELIVERIED = 2 # 已发货
    FINISHED = 3 # 已完成

    STATUS_CHOICES = (
        (START, '已提交'),
        (CODE, '已输入预约服务码'),
        (DELIVERIED, '已发货'),
        (FINISHED, '售后已完成')
    )

    status = models.SmallIntegerField( choices=STATUS_CHOICES, default = START)
  

    class Meta:
        permissions = (
           ( 'aftersaler', u'售后客服-填写寄修单'),
        ) 
        abstract = True


class AdaptorAfterSales(AfterSales):
    """AfterSales 适配器""" 
    def __str__(self):
        return self.name 
 
 



