"""
Django settings for store project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https:#docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https:#docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https:#docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cacjwhl1ic189%05f4acy64104056a@fc**7ub^)-%u+g_&ll&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["192.168.1.104",'127.0.0.1','192.168.1.102', "*"]

CORS_ORIGIN_WHITELIST = (
    '192.168.1.105:8000', '192.168.1.103:80','192.168.1.103', '127.0.0.1',  
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'ckeditor',
    'openunipay',
    'rest_framework',
    'appuser',
    'category',
    'product',
    'shopcar',
    'bill',
    'address',
    'area',
    'apis',
    'sitecontent',
    'comment',
    'piclab',
    'coupon',
    'invoice',
    'aftersales',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'store.views.caritems',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',  
            ],
        },
    },
]

WSGI_APPLICATION = 'store.wsgi.application'


# Database
# https:#docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'store',
		'USER':'root',
        'PASSWORD':'sqlroot',
        'HOST':'localhost',
        'PORT':3306, 
    }
}


# Password validation
# https:#docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https:#docs.djangoproject.com/en/1.11/topics/i18n/

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

LANGUAGE_CODE = 'zh-hans'


TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https:#docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static1')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
AUTH_USER_MODEL = 'appuser.AdaptorUser'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
)

AUTHENTICATION_BACKENDS=['store.third_party_backend.PhoneBackend', 'django.contrib.auth.backends.ModelBackend']
SOCIALOAUTH_SITES = (  
    ('weibo', 'socialoauth.sites.weibo.Weibo', u'新浪微博',
        {
          'redirect_uri': 'http://test.codeshift.org/account/oauth/weibo',
          'client_id': 'YOUR ID',
          'client_secret': 'YOUR SECRET',
        }
    ),

    ('qq', 'socialoauth.sites.qq.QQ', u'QQ',
        {
          'redirect_uri': 'http://www.map2family.com/user/portrait/',
          'client_id': '101286196',
          'client_secret': 'fbb548eb2652adf03558e435ffb83c08',
        }
    ),

    ('douban', 'socialoauth.sites.douban.DouBan', u'豆瓣',
        {
          'redirect_uri': 'http://test.codeshift.org/account/oauth/douban',
          'client_id': 'YOUR ID',
          'client_secret': 'YOUR SECRET',
          'scope': ['douban_basic_common']
        }
    ),
)

CKEDITOR_UPLOAD_PATH = 'images/'
CKEDITOR_CONFIGS = {
    'default': { 
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Font','FontSize','Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',  
            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '#cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'font',
            'autolink',
            'autoembed',
             
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

EMAIL_SWITCH = True
SMTP_SERVER         ='smtp.mxhichina.com' #SMTP server IP address
SMTP_SERVER_USER    ='postmaster@map2family.com'  
SMTP_SERVER_PWD     ='Youxiang889886'  


PROJECTNAME = '一数科技商城'

LOGIN_URL = '/users/login/'

FILE_MAX_SIZE = 512*1024 #
FILE_COMPRESSION_RIO = 75 #75%, [0-100]

SMS = {
    'SMS_SN' : "SDK-BBX-010-22746",
    'SMS_PWD' : "76D7DAAC410AF587F0DEEE4F5FA86795",
}
SMS_API = "http://sdk2.entinfo.cn:8061/mdsmssend.ashx?sn=SDK-BBX-010-22746&pwd=76D7DAAC410AF587F0DEEE4F5FA86795&mobile={0}&content={1}"


# 第三方用户登录信息
LOGIN_MASTER = "http://127.0.0.1:7000"
STORE_LOGIN = 'http://127.0.0.1:9000'
LOGIN_APPID = "17ad0726-c535-4acd-96d8-c7cba0784424"
LOGIN_SECRET = "113e2570-970f-4214-87c1-913a765a4bfc"
THIRD_LOGIN_URL = LOGIN_MASTER + "/users/login/?appid="+LOGIN_APPID+"&redirect_url="+STORE_LOGIN+"/users/login/"
THIRD_AUTH_URL = LOGIN_MASTER + "/users/oauth2/authorize/"


#####支付宝支付配置
ALIPAY = {
'partner':'XXX', #支付宝partner ID fetgid1804@sandbox.com
'seller_id':'XXX', #收款方支付宝账号如 pan.weifeng@live.cn
'notify_url':'https:#XXX/notify/alipay/', #支付宝异步通知接收URL
'ali_public_key_pem':'PATH to PEM File', #支付宝公钥的PEM文件路径,在支付宝合作伙伴密钥管理中查看(需要使用合作伙伴支付宝公钥)。如何查看，请参看支付宝文档
'rsa_private_key_pem':'PATH to PEM File',#您自己的支付宝账户的私钥的PEM文件路径。如何设置，请参看支付宝文档
'rsa_public_key_pem':'PATH to PEM File',#您自己的支付宝账户的公钥的PEM文件路径。如何设置，请参看支付宝文档
}

#####微信支付配置
WEIXIN = {
'app_id':'XXX', #微信APPID
'app_seckey':'XXX', #微信APP Sec Key
'mch_id':'XXX', #微信商户ID
'mch_seckey':'XXX',#微信商户seckey
'mch_notify_url':'https:#XXX/notify/weixin/', #微信支付异步通知接收URL
'clientIp':'',#扫码支付时，会使用这个IP地址发送给微信API, 请设置为您服务器的IP 
}

# 支付宝测试-沙箱环境
# 支付宝配置参数
ALIPAY_APPID = "2016091000479829"
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do"
ALI_PUBLIC_KEY = os.path.join(BASE_DIR, 'store', 'alipay_public.pem')
PRIVATE_KEY = os.path.join(BASE_DIR, 'store', 'app_private_key.pem')

PAYHOST = 'http://www.asu.com:9000'
ALIPAY_RETURN_URL = PAYHOST + '/alipay_check_pay'
ALIPAY_NOTIFY_URL = PAYHOST + '/alipay_notify'