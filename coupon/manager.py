#! -*- coding:utf-8 -*-
from django.db import models  
import pdb
import json
from datetime import datetime
import uuid

class CouponManager(models.Manager): 
    def create_coupon(self, post, user):
        pass

class AdaptorCouponManager(CouponManager):
    pass

 