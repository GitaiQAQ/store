# -*- conding:utf-8 -*- 
from django.db import models
from django.utils.translation import ugettext_lazy as _
from appuser.models import AdaptorUser as User
from basedatas.models import BaseDate

from category.models import Category

class Coupon(BaseDate):
    """ 
    优惠劵类： 
    """ 
    # 哪个用户
    owner = models.ForeignKey(User, related_name="owner", null=True)
    creator = models.ForeignKey(User, related_name="creator")
    deadline = models.DateTimeField() 
    # 优惠劵号码，uuid类型
    code = models.CharField(_('name'), max_length=128, unique=True) 
    # 优惠劵类型
    #  
    #     1 满多少减多少，如： 1000减300
    #     0 直减，直接减去多少，如：直接减1000
    coupon_type = models.PositiveIntegerField(default = 0)
    # 是否已使用
    #  
    #     0 未使用
    #     1 已使用
    #     2 已过期
    used = models.PositiveIntegerField(default = 0)
    # 满足的金额
    top_price = models.DecimalField(_('price'), max_digits=9, decimal_places=0, null=True) 
    # 优惠金额 或者 直减金额
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=0, null=True) 
    # 适用类别
    categories = models.ManyToManyField(Category)
    # 使用规则
    rule = models.TextField(null=True)
    class Meta: 
        ordering = [ 'used', '-date',] 
        abstract = True
        permissions = (
           ( 'manager_coupon', u'管理优惠劵：删除-创建'),
        ) 

class AdaptorCoupon(Coupon):
     
    def get_uuid(self):
        return uuid.uuid4()