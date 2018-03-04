# -*- conding:utf-8 -*- 
from django.db import models
from django.utils.translation import ugettext_lazy as _
from appuser.models import AdaptorUser as User
from basedatas.models import BaseDate
import uuid

class Coupon(BaseDate):
    """ 
    优惠劵类： 
    """ 
    owner = models.ForeignKey(User, related_name="owner")
    creator = models.ForeignKey(User, related_name="creator")
    date_added = models.DateTimeField(auto_now_add=True) 
    # 优惠劵号码，uuid类型
    code = models.CharField(_('name'), max_length=128, unique=True) 
    # 优惠劵类型
    #  
    #     1 满多少减多少，如： 1000减300
    #     2 直减，直接减去多少，如：直接减1000
    coupon_type = models.PositiveIntegerField(default = 0)
    # 是否已使用
    #  
    #     0 未使用
    #     1 已使用
    used = models.PositiveIntegerField(default = 0)
    # 满足的金额
    top_price = models.DecimalField(_('price'), max_digits=9, decimal_places=0, null=True) 
    # 优惠金额   
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=0, null=True) 

    class Meta: 
        ordering = ['-date'] 
        abstract = True

class AdaptorCoupon(Coupon):
     
    def get_uuid(self):
        return uuid.uuid4()