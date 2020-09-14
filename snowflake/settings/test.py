import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *
import pymysql

DEBUG = False
# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['*']

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('TEST_MYSQL_NAME'),
        'USER': env('MYSQL_USER'),
        'PASSWORD': env('MYSQL_PASSWORD'),
        'HOST': env('TEST_MYSQL_HOST'),
        'PORT': env('MYSQL_PORT'),
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"',
            'charset' : 'utf8mb4',
        }
    }
}


AWS_STORAGE_BUCKET_NAME=env("TEST_AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME


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
    environment='test'
)
