from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from alipay import AliPay
import os
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


import pdb
from bill.apis import pay_bill


def init():
    alipay_intance = AliPay(
        appid=settings.ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_path=settings.PRIVATE_KEY,
        alipay_public_key_path=settings.ALI_PUBLIC_KEY,

        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False  # 默认False  配合沙箱模式使用
    )
    return alipay_intance

def alipay(order_id, total_amount, subject, pc= True):
    #request.POST.get("order_id")
    # 创建用于进行支付宝支付的工具对象
    total_amount = str(total_amount) 
    alipay = init()

    
    if pc:
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no = order_id,
            total_amount = str(total_amount),  # 将Decimal类型转换为字符串交给支付宝
            subject = subject,
            return_url = settings.ALIPAY_RETURN_URL,
            notify_url = settings.ALIPAY_NOTIFY_URL  # 可选, 不填则使用默认notify url
        )
    else: 
        # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_wap_pay(
            out_trade_no= order_id,
            total_amount=str(total_amount),
            subject=subject,
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL  # 可选, 不填则使用默认notify url
        )
    # 让用户进行支付的支付宝页面网址
    url = settings.ALIPAY_URL + "?" + order_string
    return url  

def alipay_refund(order_id, total_amount):
    # 退款
    # 创建用于进行支付宝支付的工具对象
    alipay =  init()
   
    # 2018042723221914
    result = alipay.api_alipay_trade_refund(str(total_amount), order_id)
    #return redirect(url)
     
    return result


def alipay_notify(request):
    """

    """
    
    return HttpResponse("get from alipay")


def alipay_query(order_id):
    """
    支付宝支付接口查询订单状态
    """
    alipay = init()
    result = alipay.api_alipay_trade_query(out_trade_no = order_id) 
    result['status'] =  'error'
    if result.get("trade_status", "") == "TRADE_SUCCESS":
        paid = True 
        total_amount = result.get("total_amount")
        send_pay_date = result.get("send_pay_date")
        pay_way = 'zhifubao'
         
        pay_result = pay_bill(order_id, pay_way, total_amount, order_id, send_pay_date)
        result['status'] = pay_result['status']
 
    return result
     


def alipay_check_pay(request):
    # 创建用于进行支付宝支付的工具对象
     
    order_id = request.GET['out_trade_no']
    alipay = init()
    while True:
        # 调用alipay工具查询支付结果
        resp = alipay.api_alipay_trade_query(order_id)  # resp是一个字典
        # 判断支付结果
        code = resp.get("code")  # 支付宝接口调用成功或者错误的标志
        trade_status = resp.get("trade_status")  # 用户支付的情况
        
        # {'code': '10000', 'msg': 'Success', 'buyer_logon_id': 'fet***@sandbox.com', 
        # 'buyer_pay_amount': '0.00', 'buyer_user_id': '2088102175947174', 
        # 'buyer_user_type': 'PRIVATE', 'invoice_amount': '0.00', 
        # 'out_trade_no': '3232423111443234ASU', 'point_amount': '0.00', 
        # 'receipt_amount': '0.00', 'send_pay_date': '2018-03-29 23:12:40', 
        # 'total_amount': '0.01', 'trade_no': '2018032921001004170200926730', 
        # 'trade_status': 'TRADE_SUCCESS'}

        
        if code == "10000" and trade_status == "TRADE_SUCCESS":
            # 表示用户支付成功
            # 返回前端json，通知支付成功
            trade_no = resp.get("trade_no")
            total_amount = resp.get("total_amount")
            send_pay_date = resp.get("send_pay_date")
            pay_way = 'zhifubao'
            result = pay_bill(order_id, pay_way, total_amount, trade_no, send_pay_date)
            if result['status'] == 'ok':
                #返回成功页面 
                bill = result['bill'] 
                return redirect(reverse('bill:detail', kwargs={'pk': bill.pk}))
            else:
                return HttpResponse("订单异常...")
            
            return JsonResponse({"code": 0, "message": "支付成功"})

        elif code == "40004" or (code == "10000" and trade_status == "WAIT_BUYER_PAY"):
            # 表示支付宝接口调用暂时失败，（支付宝的支付订单还未生成） 后者 等待用户支付
            # 继续查询
            print(code)
            print(trade_status)
            continue
        else:
            # 支付失败
            # 返回支付失败的通知
            return JsonResponse({"code": 1, "message": "支付失败"})