from django.shortcuts import render
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from django.conf import settings
from sitecontent.models import AdaptorBaseBlock
from product.models import AdaptorProduct as Product
from category.models import Category

dmb     = DetectMobileBrowser()


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