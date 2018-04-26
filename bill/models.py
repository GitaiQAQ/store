
# -*- conding:utf-8 -*- 
from django.db import models
from django.utils.translation import ugettext_lazy as _
from appuser.models import AdaptorUser as User
from basedatas.models import BaseDate
from bill.manager import AdaptorBillManager, AdaptorBillItemManager
from product.models import AdaptorProduct, AdaptorRule
from address.models import Address
from invoice.models import Invoice
from coupon.models import AdaptorCoupon as Coupon
import threading

class Bill(BaseDate):
    """
    订单主表
    """
    STATUS_FAILED = -3 # 订单创建失败
    STATUS_SUBMITTED = -2 # 订单已提交
    STATUS_UNPAYED = 0 # 未支付
    STATUS_PAYED = 1   # 已支付
    STATUS_DELIVERIED = 2   # 已发货
    STATUS_FINISHED = 3# 已完成
    STATUS_BAD = 4 #异常订单
    STATUS_REFUND = 5 # 已退款

    #TIMEOUT = 24 * 60 * 5 # 24小时内支付
    TIMEOUT =  60 * 15 # 15 分钟内支付

    STATUS_CHOICES = (
        (STATUS_FAILED, '失败'),
        (STATUS_SUBMITTED, '已提交，未支付'), 
        (STATUS_PAYED, '已支付，即将发货'),
        (STATUS_DELIVERIED, '已发货，等待签收'),
        (STATUS_FINISHED, '已签收，订单已完成'), 
        (STATUS_REFUND, '已退款'),
        (STATUS_BAD, '异常订单'),
    )

    # 组成方式：年月日时分秒毫秒用户ID
    no = models.CharField(_('Bill No.'), max_length=1024)
    # 提交订单的人
    owner = models.ForeignKey(User, related_name="bill_owner") 
    
    # 收货人地址
    address_detail = models.CharField(_('address_detail'), max_length=1024, null = True) 
    # 收货人电话号码
    phone = models.CharField(_('phone'), max_length=20, null = True) 
    # 收货人姓名
    reciever = models.CharField(_('reciever'), max_length=120, null = True)
  
    #应付金额
    money = models.DecimalField(_('Money'), max_digits = 9, decimal_places = 2, default = 0.0)

    # 订单状态
    # 订单已提交状态在验证了库存之后，直接转入未支付状态
    status = models.SmallIntegerField(choices = STATUS_CHOICES, default = STATUS_SUBMITTED)
    
    # 订单失败的原因， 在订单创建失败之后，这个字段存储创建失败的原因，如库存不足
    errromsg = models.CharField(_('Phone'), max_length = 4096, null =True) 

    # 备注
    remark = models.TextField(_('Remark'), null=True)
    # 发票信息
    invoice = models.ForeignKey(Invoice, null = True)  
    
    # 物流公司和物流号
    delivery_company = models.CharField( max_length = 128, null =True) 
    delivery_no = models.CharField( max_length = 128, null =True) 

    # 支付信息
    ALIPAY = 'zhifubao' #支付宝
    WEIXINPAY = 'weixin' #微信
 
    PAY_CHOICES = (
        (WEIXINPAY, '微信'),
        (ALIPAY, '支付宝'), 
    )
    # 支付方式
    pay_way = models.CharField( choices=PAY_CHOICES, max_length = 128, null =True)
    # 支付金额
    payed_money = models.DecimalField(_('Payed Money'), max_digits = 9, decimal_places = 2, null =True)
    # 微信或者支付宝的支付编号
    trade_no = models.CharField(_('trade no'), max_length = 4096, null = True) 
    pay_datetime = models.DateTimeField(_('pay date'),null = True) 
    
    # 退款相关信息
    # 退款状态
    REFUNDAPPLY = 0
    REFUNDWAITING = 1
    REFUNDAGREE = 2
    REFUNDREFUSED = 3

    REFUND_CHOICES = (
        (REFUNDAPPLY, '申请退款'),
        (REFUNDWAITING, '等待客服审批'), 
        (REFUNDAGREE, '退款已同意'), 
        (REFUNDREFUSED, '退款被拒绝'), 
    )
    
    refundstatus = models.SmallIntegerField( choices=REFUND_CHOICES, max_length = 128, 
                    default =REFUNDAPPLY)
    refund_reason = models.TextField(_('refund reason'), null=True)
    # 退款申请时间
    refund_time = models.DateTimeField( null=True)

    # 退款审批信息：
    # 审批人
    refund_approver = models.ForeignKey(User, related_name="refund_approver", null=True)
     
    # 退款审批状态  
    REFUND_APPROVE_CHOICES = ( 
        (REFUNDAGREE, '退款已同意'), 
        (REFUNDREFUSED, '退款被拒绝'), 
    )
    refund_approve_status = models.CharField( choices=REFUND_APPROVE_CHOICES, max_length = 128, 
                    null =True)
    # 审批时间
    refund_approve_time = models.DateTimeField( null=True)
    # 审批原因
    refund_approve_reason = models.TextField(_('refund approve reason'), null=True)


    def __str__(self):
        return self.no

    @property
    def get_adminrefund_status(self):
        """
        返回管理员可以看到的退款状态列表
        """
        return [self.REFUNDWAITING, self.REFUNDAGREE, self.REFUNDREFUSED]

    class Meta:
        abstract = True
        ordering = ['-date']

class AdaptorBill(Bill):
    objects = AdaptorBillManager()

class BillItem(models.Model):
    """
    订单items
    """  
    # 订单主表
    bill = models.ForeignKey(AdaptorBill)

    # 产品名称:ASU 手表
    product_title = models.CharField(_('Title'), max_length = 4096, null = True) 
    # 规格名称：黑金版，红色
    rule_title = models.CharField(_('Rule'), max_length = 4096, null = True) 
    
    # 外键，规格和产品都有可能被删除和编辑，所以这里的外键仅作为减库存时的依据
    # 如果在减库存的时候，
    rule = models.ForeignKey(AdaptorRule, on_delete=models.SET_NULL, null = True)
    product = models.ForeignKey(AdaptorProduct, on_delete=models.SET_NULL, null = True)

    # 下订单时的价格
    price = models.DecimalField(_('Price'), max_digits = 9, decimal_places = 2, default = 0.0)
    # 订单中某商品的数量
    num = models.PositiveIntegerField(_('Number'))
    
    
 
    class Meta:
        abstract = True
        permissions = (
            ('manage_bill', u'订单管理权限'),
        )


class AdaptorBillItem(BillItem):
    objects = AdaptorBillItemManager()

class CouponItem(models.Model):
    """
    订单中优惠劵减免记录
    """  
    # 订单主表
    bill = models.ForeignKey(AdaptorBill)

    # 优惠劵码
    coupon = models.ForeignKey(Coupon, null = True)   
 
    class Meta:
        abstract = True


class AdaptorCouponItem(CouponItem):
    pass