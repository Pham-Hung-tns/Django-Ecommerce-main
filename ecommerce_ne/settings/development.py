from .base import *


DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1',"82cb-2405-4802-8156-24f0-3414-35bd-b40e-35d3.ngrok-free.app"]

INSTALLED_APPS += [
    'debug_toolbar'
]




# DEBUG TOOLBAR SETTINGS

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'mysql_db': {  # MySQL (database dùng để backup)
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': 'Hungpham0112.tns',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

import os

#tao key cho vnpay
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_TEST_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY')
VNP_TMNCODE= os.getenv('VNP_TMNCODE')
VNP_HASHSECRET= os.getenv('VNP_HASHSECRET')
VNP_URL=os.getenv('VNP_URL')
VNP_RETURN_URL=os.getenv('VNP_RETURN_URL')


