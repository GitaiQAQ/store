
# -*- coding:utf-8 -*-
from django.db import models
from appuser.models import AdaptorUser as User
from invoice.manager import AdaptorInvoiceManager

class Invoice(models.Model):
    """
    发票模型
    每个用户，一种发票类型只有一条记录：
    """
    PERSONAL = 1
    COMPANY = 0
    user = models.ForeignKey(User)
    # 纳税人编号
    code = models.CharField(max_length = 1024, null= True)
    # 发票内容
    content = models.CharField(max_length = 1024, default="商品明细") 
    # 发票抬头
    title = models.CharField(max_length = 512) 
    # 发票类型：企业0还是个人1，默认是个人
    invoicetype = models.SmallIntegerField(default = PERSONAL) 
    objects = AdaptorInvoiceManager()
     
    