# coding=utf-8
"""
Django settings for ggxxBBS project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wy)q87p@9ny105=*66ym8y5hy(df02$9u+nyv6u9$ylpe=0-ns'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# ALLOWED_HOSTS = '*'
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# 默认就是true
# APPEND_SLASH = True

# Application definition

INSTALLED_APPS = (
    'account',
    'forum',
    'uuidfield',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'ckeditor',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.SetLastVisitMiddleware',
)

DEFAULT_FILE_STORAGE = 'forum.storage.FileStorage'

AUTH_USER_MODEL = 'account.MyUser'

ROOT_URLCONF = 'ggxxBBS.urls'

WSGI_APPLICATION = 'ggxxBBS.wsgi.application'

LOGIN_URL = '/user/login/'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ggxxBBS',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh_CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\','/'),
STATIC_ROOT = ''

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static").replace('\\', '/'),  # 保留此条为第一行，在代码中引用了settings.STATICFILES_DIRS[0]
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'upload').replace('\\', '/')

MEDIA_URL = '/upload/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates').replace('\\', '/'),
)

# FILE_UPLOAD_PERMISSIONS = 0644

# dt = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m')

# ckeditor config
now = datetime.datetime.now()
CKEDITOR_UPLOAD_PATH = "ck_upload/"
# CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_JQUERY_URL = 'static/js/jquery-1.11.2.min.js'
# CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

# All uploaded files are slugified by defaults, to disable this feature set
# ``CKEDITOR_UPLOAD_SLUGIFY_FILENAME`` to ``False``

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': (
            ['div', 'Source', '-'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'],
            ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat'],
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks'],
        ),
        'skin': 'office2013',
        'language': 'zh-cn',
    },
    'basic': {
        'toolbar': (
            # ['div', 'Source', '-'],
            ['Cut', 'Copy', 'Paste', 'PasteText'],
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Font'],
            ['TextColor', 'BGColor'],
        ),
        'skin': 'office2013',
        'language': 'zh-cn',
        'height':100,
    },
}