from django.conf.urls import include, url 
from bill.views import BillView, BillDetailView, RabbitBillDetailView
from bill import views, adminviews
 
urlpatterns = [  
    url(r'^bills/$', BillView.as_view(), name='bills'),   
    url(r'^bills/(?P<pk>[0-9]+)/$', BillDetailView.as_view(), name='detail'), 
    url(r'^bills/(?P<pk>[0-9]+)/rabbit$', RabbitBillDetailView.as_view(), name='rabbit'),     
    url(r'^bills/pay_callback$', views.pay_callback, name='pay_callback'),
    url(r'^bills/web_callback$', views.web_callback, name='web_callback'),
    url(r'^bills/admin$', adminviews.admin, name='admin'),
    url(r'^bills/delivery$', adminviews.delivery, name='delivery'),
    url(r'^bills/sales$', adminviews.sales, name='sales'),
]
