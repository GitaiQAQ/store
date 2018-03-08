#! -*- coding:utf-8 -*-
import pdb
from django import template
from area.models import Area

register = template.Library()
bigcity = [110100, 120000, 310000, 500000]
@register.filter
def areas(area):  
     
    city = Area.objects.get(id = area.parent_id) 
    if city.id in bigcity:
        province = city
    else:
        province = Area.objects.get(id = city.parent_id)
    string = province.short_name + '省 '+ city.short_name + '市 ' 
    return string
     