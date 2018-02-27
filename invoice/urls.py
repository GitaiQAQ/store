from django.conf.urls import include, url 
from invoice.views import InvoiceView   　

urlpatterns = [     
    url(r'^invoice/$', InvoiceView.as_view(), name='invoice'),     
]
