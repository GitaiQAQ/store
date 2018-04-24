# -*- conding:utf-8 -*- 
import pdb

from bill.models import AdaptorBill as Bill
from django.utils import timezone


def get_bill_money(bill):
    """
    获取订单bill中总共应支付的金额，应支付金额=商品总价-优惠券金额

    """
    billitems = bill.adaptorbillitem_set.all()
    sum  = 0
    for billitem in billitems:
        sum += billitem.rule.price * billitem.num

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
    try:
        bill = Bill.objects.get(no = billno)
    except Bill.DoesNotExist:
        result['status']  = 'error'
        result['msg'] = "未找到订单:{0}".format(billno)
        return result
    result['bill'] = bill
    sum  = get_bill_money(bill) 
    if str(sum) != str(payed_money):
        result['status']  = 'error'
        result['msg'] = "bad bill"
        bill.status = Bill.STATUS_BAD
        bill.money = payed_money
        bill.payed_money = payed_money
        bill.errormsg = '支付金额与订单金额不符.'
    else:
        bill.status = Bill.STATUS_PAYED
        bill.money = payed_money
        bill.pay_way = pay_way
        bill.payed_money = payed_money
        bill.trade_no = trade_no
        bill.pay_datetime = pay_datetime
        for billitem in bill.adaptorbillitem_set.all(): 
            # 更新 item中的价格
            billitem.price = billitem.rule.price
            billitem.product_title = billitem.rule.product.title
            billitem.save() 

        result['status']  = 'ok'
        result['msg'] = "saved"
    bill.save()

    return result


def check_inventory(items):
    """ 
    检查订单中是否有库存不足的商品，
    如果有：result['status'] 返回false，并且在result['items']中返回库存不足的商品
    如果没有：result['status'] 返回True
    """
    result = {} 
    result['status'] = True
    for item in items: 
        if item['rule'].inventory == 0:
            """
            无库存
            """
            result['status'] = False
            result['product'] = item['rule'].product.title + '|' +  item['rule'].name
            return result
        elif item['rule'].inventory > 0 :
            if item['rule'].inventory < item['num'] :
                # 库存不足
                result['status'] = False
                result['product'] = item['rule'].product.title + '|' +  item['rule'].name
                return result

    return result

def getavailabletime(bill):
    """
    获取订单剩余的支付时间
    """ 
    now = timezone.now()
    seconds = int((now - bill.date).total_seconds())
    result = {}
    if seconds < bill.TIMEOUT: 
        result['status'] = 'ok'
        result['timeout'] = False
    else:
        # 超时，不能继续支付订单
        result['status'] = 'error'
        result['timeout'] = True 
        if bill.status == bill.STATUS_UNPAYED or bill.status == bill.STATUS_SUBMITTED:
            # 有库存管理的商品进行退库
            billitems = bill.adaptorbillitem_set.all()
            for billitem in billitems:
                if billitem.rule.inventory is not None:
                    billitem.rule.inventory += billitem.num
                    billitem.rule.save()
            bill.delete() # 未支付订单，删除
    
    return result


def check_bill_timeout(bills):
    """
    查看订单是否已过期，如果过期，则自定删除
    """
    for bill in bills: 
        if bill.status == bill.STATUS_SUBMITTED or bill.status == bill.STATUS_UNPAYED:
            # 订单已支付，不需要删除了
            getavailabletime(bill)


       