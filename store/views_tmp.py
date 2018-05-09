from django.shortcuts import render
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from django.conf import settings
from sitecontent.models import AdaptorBaseBlock
from product.models import AdaptorProduct as Product
from category.models import Category
from shopcar.models import CartItem
dmb     = DetectMobileBrowser()
import pdb
from django.shortcuts import redirect 
def service(request):
    return redirect('/aftersales/aftersales/')
     
 