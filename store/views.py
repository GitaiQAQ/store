from django.shortcuts import render
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from django.conf import settings
from sitecontent.models import AdaptorBaseBlock
from product.models import AdaptorProduct as Product
from category.models import Category
from shopcar.models import CartItem
dmb     = DetectMobileBrowser()
import pdb

def home(request):
    content ={}
    isMble  = dmb.process_request(request)

    sitecontents = AdaptorBaseBlock.objects.all()#sget_available_content()
    content['sitecontents'] = sitecontents
    content['mediaroot'] = settings.MEDIA_URL
    
    products = Product.objects.all().order_by('category')
    categories = Category.objects.all()
    content['products'] = products
    content['categories'] = categories
     
    if isMble:
        return render(request, 'home.html',content) 
    else:
        return render(request, 'home.html',content) 

def caritems(request):
    # 查看用户的购物车情况，如果购物车中有记录的话，需要更新session 
    if not request.user.is_anonymous():
        caritems = CartItem.objects.filter(user = request.user)
        counter = len(caritems) 
    else:
        counter = 0 
    return {'caritems': counter}