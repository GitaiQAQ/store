from django.conf.urls import include, url  
from aftersales import views

urlpatterns = [     
    url(r'^aftersales/$', views.AfterSalesView.as_view(), name='aftersales'),     
    url(r'^maintaincode/$', views.MainainCodeView.as_view(), name='maintaincode'),
]
