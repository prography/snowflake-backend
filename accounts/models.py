import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import UserManager


def create_image_path(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime("%Y/%m/%d")
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return "/".join(["user", ymd_path, uuid_name + extension])


class User(AbstractUser):
    SOCIAL_CHOICES = ((1, "kakao"), (2, "naver"))
    GENDER_CHOICES = ((1, "남"), (2, "여"), (3, "선택안함"))
    PARTNER_GENDER_CHOICES = ((1, "남"), (2, "여"), (3, "모두"), (4, "선택안함"))
    username = None
    email = models.EmailField(_("email address"), unique=True)
    nickname = models.CharField(max_length=255)
    image = models.ImageField(upload_to=create_image_path, blank=True, null=True)
    social = models.IntegerField(choices=SOCIAL_CHOICES, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    partner_gender = models.IntegerField(choices=PARTNER_GENDER_CHOICES)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
