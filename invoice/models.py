
# -*- coding:utf-8 -*-
from django.db import models
from appuser.models import AdaptorUser as User
 

class Invoice(models.Model):
    """
    发票模型
    """
    PERSONAL = 1
    COMPANY = 0
    user = models.ForeignKey(User)
    # 纳税人编号
    code = models.CharField(max_length = 1024, null= True)
    # 发票内容
    content = models.CharField(max_length = 1024, null = True) 
    # 发票抬头
    title = models.CharField(max_length = 512) 
    # 发票类型：企业0还是个人1，默认是个人
    invoicetype = models.SmallIntegerField(default = PERSONAL) 
    # 标记被显示在什么位置：如主轮播图中
    mark = models.CharField(max_length = 128) 
    
  