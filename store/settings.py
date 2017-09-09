"""
Django settings for store project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cacjwhl1ic189%05f4acy64104056a@fc**7ub^)-%u+g_&ll&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["192.168.1.104",'127.0.0.1','192.168.1.102']

CORS_ORIGIN_WHITELIST = (
    '192.168.1.105:8000', 
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
    'appuser',
    'category',
    'product',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'store.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

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
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


AUTH_USER_MODEL = 'appuser.AdaptorUser'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend']
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

EMAIL_SWITCH = True
SMTP_SERVER         ='smtp.mxhichina.com' #SMTP server IP address
SMTP_SERVER_USER    ='postmaster@map2family.com'  
SMTP_SERVER_PWD     ='Youxiang889886'  


PROJECTNAME = '共享商城'

LOGIN_URL = '/users/login/'