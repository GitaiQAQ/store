from django.conf.urls import include, url 
from shopcar.views import ShopcarView   
from invoice import views

urlpatterns = [     
    url(r'^invoice/$', InvoiceView.as_view(), name='invoice'),     
]
