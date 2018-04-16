# -*- coding: utf-8 -*-
from django.db import models
from area.models import Area
from appuser.models import AdaptorUser as User
from django.utils.translation import ugettext_lazy as _


class Address(models.Model):
    BIGCITY = [110100, 120000, 310000, 500000]
    user = models.ForeignKey(User)
    area = models.ForeignKey(Area)
    # 收货人地址
    detail = models.CharField(_('Detail'), max_length = 4096, null = True)
    #收货人
    receiver = models.CharField(_('Receiver'), max_length = 256, null = True) 
    #收货人电话
    phone = models.CharField(_('Phone'), max_length = 128, null = True) 
    # 默认地址
    # 1 是默认地址
    # 0 是非默认地址
    default = models.PositiveIntegerField(default = 0)
    class Meta:
        ordering = ['-default', '-id']

    def get_detail(self):
        """
        获得完整的详细地址
        """
        return areas(self.area) + self.detail
    
def areas(area):   
    city = Area.objects.get(id = area.parent_id) 
    if city.id in Address.BIGCITY:
        province = city
    else:
        province = Area.objects.get(id = city.parent_id)
    if province.id in Address.BIGCITY:
        string = city.short_name + '市 ' 
    else:
        string = province.short_name + '省 '+ city.short_name + '市 ' 
    string += area.short_name
    return string


 