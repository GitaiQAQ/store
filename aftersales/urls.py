from django.conf.urls import include, url  
from aftersales import views

urlpatterns = [     
    url(r'^aftersales/$', views.AfterSalesView.as_view(), name='aftersales'),     
    url(r'^aftersales/(?P<pk>[0-9]+)/$', views.AfterSalesDetailView.as_view(), name='detail'),
    url(r'^maintaincode/$', views.MainainCodeView.as_view(), name='maintaincode'),
]
