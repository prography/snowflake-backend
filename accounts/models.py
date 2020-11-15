import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import UserManager


def create_icon_path(instance, filename):
    ymd_path = timezone.localtime().strftime("%Y-%m-%d-%H%M%S")
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return "/".join(["accounts", "icon", ymd_path + "-" + uuid_name + extension])


class Icon(models.Model):
    # name
    name = models.CharField(max_length=100, blank=True,
                            null=True, default="제목없는아이콘")
    # Image field
    image = models.ImageField(
        upload_to=create_icon_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}_{}".format(self.id, self.name)


def create_image_path(instance, filename):
    ymd_path = timezone.localtime().strftime("%Y-%m-%d-%H%M%S")
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return "/".join(["accounts", "user", ymd_path + "-" + uuid_name + extension])


class User(AbstractUser):
    SOCIAL_CHOICES = (("KAKAO", "kakao"), ("NAVER", "naver"), ("APPLE", "apple"), ("NONE", "none"))
    GENDER_CHOICES = (("MAN", "남"), ("WOMAN", "여"), ("BOTH", "모두"), ("SECRET", "비공개"), ("NONE", "none"))
    POSITION_CHOICES = (("PURPLE", "보라두리"), ("SKY", "하늘이"), ("NONE", "선택안함"))

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    # Image field
    image = models.ImageField(upload_to=create_image_path, blank=True, null=True)

    social = models.CharField(max_length=20, choices=SOCIAL_CHOICES, null=True, blank=True, default="NONE")
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="NONE")
    partner_gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="NONE")
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default="NONE")
    birth_year = models.IntegerField(default=0)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # icon
    icon = models.ForeignKey(Icon, verbose_name="icon", related_name="user", on_delete=models.SET_NULL, null=True, blank=True)
    # RGB value
    color = models.CharField(max_length=20, null=True, blank=True, default="FFFFFF")

    objects = UserManager()

    def __str__(self):
        return self.email

    @classmethod
    def get_user_or_none(cls, email):
        try:
            user = cls.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        return user
