from base64 import b64encode
import json
import urllib
import OpenSSL

def sign(params):
    sort_param = sorted([(key, unicode(value, 'UTF-8').encode('UTF-8')) for key, value in params.iteritems()], key=lambda x: x[0])
    content = '&'.join(['='.join(x) for x in sort_param]) 
    priKey = '''-----BEGIN RSA PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCeVJSELwIMQlc3H5iA4Yl8YBP/a0nwaXYaaCsytyHtjVxXuhq8Ce3bKODzEj4nvoYm8IwF/dcmdO8/9k87+0WM0kBELk+mCBmMMi++TzK/blwjh3A91QqqUvGPQ77LxZTSVBAxLiJllqfcCz3o5wdNTzKsmoDl0TSJM63uSjWI1gw6SbRTcRYXPUqFBwOseKv++Q/senDZDP9fdCk348Hyl7HSTILnYg0s2HSxHo1rA11DxlVduNqAo2HWAjCgFS3FXZDJqhQb0QPgIGEUhVm0Uutlo/qpw0xH8iJOr60T2yZKaxmQ+z9SQ4pDIMVF5afdPVkKWFyCO1zF3GyTlZu7AgMBAAECggEAcJIqViEmD5lLcUHhqCCzI98b2Mprc6dH9VaDADf8w21ybl0/jNpyZxQVfD1IO/HWZ/E3XTsxsYIKaSuzAi6RMKJ8Vv2mW6H+qBM2ptSgfEL297vgLdY/EwKOBRJhoXgFa9Wg/ZaTli8bgfPsPJ+mLW1V1iqz4rJv6+z2iSnyDisjamJlxMND1+LGzZaC9QFk3ORvIGfCbX6NzJollL4/5xEiQ+cLN/duZEED72MbgjMCMYtLVnc9+i1RNfAZiQGfNKr9WEVmwDVmgSIotVYZg7f6JK/LtOq29Kwcm7wfKddjChqGOvVXuP7LjMiq0nbo0gbGU/GMfQPT/6h+ehY2AQKBgQDQUtsJON731xSdYakqQLKxsij8jjXsl/YoGcbjw3CbQWKMkrTTisxbWEyYuE6Qz0HrqiTmHLTGE/19iJO6wNvgkwPyGavdaJsj0/QzcAoZC0z5YizOvRcM7P5nJlfLA5+BkTYbhP3nqioFmHcMJBU1OOsdYXqg1kHKtjUKI9+AewKBgQDCkL+bCznK8ZoO87Fxit4ehrDY83hBPfw1r7CkxX+siqfgJlWyDFXXTSH0if33hlZJNHdeDxgNvGGdhXxDrCJKl0Y/cmw7SMHZJ7R8c6KS/q2RsEDSiyxkGk2sIHMpV9x1wJUXmNCmc0FWA31Egm8Ns0oItDp98t4/p0lWP1aNwQKBgQCFhAT0JSnqKEQDFjuIZAzjDG9uZmqzJzXRv6uUAIekScSymbghOHz/MlltK/rWnq7+Ln8VqGJH7TnzAdzEvaRui2rk+IUJE2kTDl4dtXoTUQXVc5GKMvCaDS6Dx7RO3hSVww6tlo/wsUPbcDskYd/hy4gMvZQNjyR9mkfmJtWxDwKBgEkbPHOUbz27NEjj9kuUg0tzDqYmLYxOLyM5BaWT9Bov605E+TQygFqqx9RruTq1hlxxU1zLTR10KDWY/40p86SVXLbgVpycBQKEccPFa1PSUAOK94Bk/OQMIh1IAB2LvvGb0CmSqOuyKN2Z6ArC+9lpAattlQDYLfw67kpy+CHBAoGBAIz/Bm0ALaixk96/VTN+dasanNvKBt2LBBcuThTazHy7LZGcS1AbcnDdAasvWL+5VB/GeCL1FgIq9aZhf71wEtw23amPVuzXo1Bg9eJF96lOF3udtlwQVomBRjTB1nWGt4zeT0j3WDKKTuAUhMstC3bHGR8wZQh7XvHkuRefp2D4
-----END RSA PRIVATE KEY-----'''
   
    private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, priKey)
    return b64encode(OpenSSL.crypto.sign(private_key, content, 'sha256'))


if '__main__' == __name__:
    params = {} 
    params['app_id'] = 'XXX'
    params['method'] = 'alipay.trade.app.pay'
    params['format'] = 'json'
    params['timestamp'] = '2017-07-07 10:05:56'
    params['charset'] = 'UTF-8'
    params['version'] = '1.0'
    params['sign_type'] = 'RSA2'
       
    params['biz_content'] = {}
    params['biz_content']['body'] = '非sdk原生php服务端生成请求订单'
    params['biz_content']['subject'] = 'php代码示例'
    params['biz_content']['out_trade_no'] = '201723123123124124'
    params['biz_content']['timeout_express']='10m'
    params['biz_content']['total_amount'] = '0.01'
    params['biz_content']['product_code'] = 'QUICK_MSECURITY_PAY'
    params['biz_content']['goods_type'] = '0'
    params['biz_content']=json.dumps(params['biz_content'], separators=(',', ':')) 
    params['sign']=rsa_sign(params);
    sort_param = sorted([(key, unicode(value, 'UTF-8').encode('UTF-8')) for key, value in params.iteritems()], key=lambda x: x[0])
    file = open('./signThing.txt', 'wb')
    file.write(urllib.urlencode(sort_param))
    file.close()
