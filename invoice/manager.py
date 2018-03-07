#! -*- coding:utf-8 -*-
from django.db import models  
import pdb
import json
from datetime import datetime


class InvoiceManager(models.Manager): 
    def add(self, post, user):
        """
        添加发票
        """
        invoicetype = post['invoicetype']
        
        try:
            invoice = self.get(user = user, invoicetype = invoicetype)
        except self.model.DoesNotExist:
            invoice = self.create(user = user, invoicetype = invoicetype)
        except self.model.MultipleObjectsReturned:
            invoices = self.filter(user = user, invoicetype = invoicetype)
            invoices.delete()
            invoice = self.create(user = user, invoicetype = invoicetype)
        
        title = post['title']
        code = post['code']
        invoice.title = title
        invoice.code = code
        invoice.save()
        return invoice

class AdaptorInvoiceManager(InvoiceManager):
    pass

 