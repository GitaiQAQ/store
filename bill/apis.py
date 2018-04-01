# -*- conding:utf-8 -*- 
import pdb

from bill.models import AdaptorBill as Bill

def get_bill_money(bill):
    """
    获取订单bill中总共应支付的金额，应支付金额=商品总价-优惠券金额

    """
    billitems = bill.adaptorbillitem_set.all()
    sum  = 0
    for billitem in billitems:
        sum += billitem.rule.price

    coupons = bill.adaptorcouponitem_set.all()
    for coupon in coupons:
        sum -= coupon.coupon.price

    return sum

def pay_bill(billno, pay_way, payed_money, trade_no, pay_datetime):
    """
    填写订单支付信息:支付方式、支付金额，支付订单号，支付时间
    验证信息：支付金额需要跟应付金额相同，否则列为异常订单
    """
    result = {}
    bill = Bill.objects.get(no = billno)
    result['bill'] = bill
    sum  = get_bill_money(bill)
 
    if str(sum) != payed_money:
        result['status']  = 'error'
        result['msg'] = "bad bill"
        bill.status = Bill.STATUS_BAD
    else:
        bill.status = Bill.STATUS_PAYED
        bill.money = payed_money
        bill.pay_way = pay_way
        bill.payed_money = payed_money
        bill.trade_no = trade_no
        bill.pay_datetime = pay_datetime
        result['status']  = 'ok'
        result['msg'] = "saved"
    bill.save()

    return result
