import os
from uuid import uuid4

from django.db import models
from model_utils.managers import InheritanceManager
from django.utils import timezone


def create_path(directory, filename):
    ymd_path = timezone.localtime().strftime("%Y-%m-%d-%H%M%S")
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return "/".join(["products", "product", directory, ymd_path + "-" + uuid_name + extension])


def create_thumbnail_path(instance, filename):
    return create_path("thumbnail", filename)


def create_image_path(instance, filename):
    return create_path("image", filename)


class WelcomeCard(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # WelcomeCard의 버튼을 클릭하면 redirect할 주소
    button_src = models.URLField(max_length=2000)
    # WelcomeCard의 이미지
    image = models.ImageField(upload_to=create_path, blank=True, null=True)

    # 카드의 메인 화면에서의 위치 지정
    col = models.IntegerField(default=0)

    # 이 카드가 보여질지 말지, 삭제된 카드인지 여부
    STATUS_CHOICES = (("DEL", "Deleted"), ("DRAFT", "Draft"), ("PUB", "Published"))
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=create_thumbnail_path, blank=True, null=True)
    image = models.ImageField(upload_to=create_image_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(default=0)
    ingredients = models.TextField(blank=True, null=True)
    num_of_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    num_of_views = models.BigIntegerField(default=0)

    objects = InheritanceManager()

    def __str__(self):
        return self.name


class Condom(Product):
    CATEGORY_CHOICES = ((1, "일반형"), (2, "슬림형"), (3, "초박형"), (4, "돌출형"), (5, "꼭지형"), (6, "사전지연형"))

    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)
    thickness = models.FloatField(default=0, verbose_name="두께")
    length = models.FloatField(default=0, verbose_name="길이")
    width = models.FloatField(default=0, verbose_name="폭")

    avg_oily = models.FloatField(default=0, verbose_name="윤활제 평균")
    avg_thickness = models.FloatField(default=0, verbose_name="두께 평균")
    avg_durability = models.FloatField(default=0, verbose_name="내구성 평균")

    def __str__(self):
        return self.name + " - " + self.manufacturer


class Gel(Product):
    avg_viscosity = models.FloatField(default=0, verbose_name="점성 평균")
