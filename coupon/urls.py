from django.conf.urls import include, url  
from coupon import views

urlpatterns = [     
    url(r'^coupon/$', views.CouponView.as_view(), name='coupons'),     
     
]
