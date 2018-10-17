"""
Django settings for crawl project.

Generated by 'django-admin startproject' using Django 1.8.19.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')  # TRUE: 開發環境, FALSE: Production

print('[django settings.py]\tRunning on devserver:', RUNNING_DEVSERVER)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8(m)8e5a0*xt5q3(=63pgt2erwr!7r36!6dz=$f8o69$1qu9$8'

ALLOWED_HOSTS = ['*', 'localhost', 'ngrok.io', 'crawl-curation.appspot.com']

# SECURITY WARNING: don't run with debug turned on in production!
if RUNNING_DEVSERVER:
    DEBUG = True
else:
    DEBUG = False

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'memoize',
    'CrawlCuration',
    'DataProcessing',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'crawl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates').replace('\\', '/')],
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

WSGI_APPLICATION = 'crawl.wsgi.application'

# Session settings
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hant'

USE_TZ = True
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
# 本地端使用'/static/'
# Google端使用'https://storage.googleapis.com/crawl-curation.appspot.com/static/'
if RUNNING_DEVSERVER:
    STATIC_URL = '/static/'
    # STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
elif not RUNNING_DEVSERVER:
    STATIC_URL = 'https://storage.googleapis.com/crawl-curation.appspot.com/static/'
    