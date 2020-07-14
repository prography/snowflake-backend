import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False
# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('MYSQL_NAME'),
        'USER': env('MYSQL_USER'),
        'PASSWORD': env('MYSQL_PASSWORD'),
        'HOST': env('MYSQL_HOST'),
        'PORT': env('MYSQL_PORT'),
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}

def sentry_before_send(event, hint):
    ignored_exceptions = [KeyboardInterrupt]
    if 'exc_info' in hint:
        _, exc_value, _ = hint['exc_info']

        for exception in ignored_exceptions:
            if isinstance(exc_value, exception):
                return
    return event

sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
    attach_stacktrace=True,
    before_send=sentry_before_send,
    environment='production'
)
