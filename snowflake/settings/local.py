from .base import *


DEBUG = True

ALLOWED_HOSTS = ["*", ]



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
            'charset' : 'utf8mb4'
        }
    }
}

AWS_STORAGE_BUCKET_NAME=env("TEST_AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME