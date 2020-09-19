import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .local import *
import pymysql

DEBUG = False
# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['*']


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
