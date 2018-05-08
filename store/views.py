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
    print(request.session.get('token'))
    #products = Product.objects.all().order_by('category', '-date')
    products = Product.objects.filter(status = Product.PUBLISHED).order_by('category', '-date')
    categories = Category.objects.all()
    content['products'] = products
    content['categories'] = categories 
    if isMble:
        return render(request, 'm_home.html',content) 
    else:
        return render(request, 'home.html',content) 

def caritems(request):
    # 查看用户的购物车情况，如果购物车中有记录的话，需要更新session 
    if not request.user.is_anonymous():
        caritems = CartItem.objects.filter(user = request.user)
        counter = len(caritems) 
        adminperm = request.user.has_perm('product.manage_product')
    else:
        counter = 0 
        adminperm = False
    token = False 
    if 'token' in request.session:
        token = request.session['token']
    return {'caritems': counter, 'adminperm':adminperm, 'token':token}