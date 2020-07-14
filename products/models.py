import os
from uuid import uuid4

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from model_utils.managers import InheritanceManager
from django.utils import timezone

from likes.models import Like


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
    tag_txt = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # WelcomeCard의 버튼을 클릭하면 redirect할 주소
    button_src = models.URLField(max_length=2000)
    button_txt = models.CharField(max_length=255)
    # WelcomeCard의 이미지
    image = models.ImageField(upload_to=create_path, blank=True, null=True)

    design_type = models.CharField(max_length=50, default="DEFAULT")

    CATEGORY_CHOICES = (("NONE", "지정안됨"), ("PROD", "제품"), ("LAB", "실험실"), ("COMMU", "상담소"))
    # 카드의 메인 화면에서의 위치 지정
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, default="NONE")
    col = models.IntegerField(default=-1)

    # 이 카드가 보여질지 말지, 삭제된 카드인지 여부
    STATUS_CHOICES = (("DEL", "Deleted"), ("DRAFT", "Draft"), ("PUB", "Published"))
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default="DRAFT")

    def __str__(self):
        return self.title


def populate_search_field(search_fields):
    from itertools import permutations
    permute = permutations(search_fields, 2)
    result = ""
    for sf in search_fields:
        if sf is None:
            continue
        result += "{}\n".format(sf.replace(" ", ""))
    for p in permute:
        if None in p:
            continue
        result += "{}{}\n".format(p[0].replace(" ", ""), p[1].replace(" ", ""))
    return result


class Product(models.Model):
    name_kor = models.CharField(max_length=255, null=True, blank=True)
    name_eng = models.CharField(max_length=255, null=True, blank=True)

    thumbnail = models.ImageField(upload_to=create_thumbnail_path, blank=True, null=True)
    image = models.ImageField(upload_to=create_image_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    manufacturer_kor = models.CharField(max_length=100, blank=True, null=True)
    manufacturer_eng = models.CharField(max_length=100, blank=True, null=True)

    score = models.FloatField(default=0)
    ingredients = models.TextField(blank=True, null=True)
    num_of_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="업데이트 시간")
    num_of_views = models.BigIntegerField(default=0)

    search_field = models.TextField(blank=True, null=True, default="")
    likes = GenericRelation(Like)
    num_of_likes = models.IntegerField(default=0)

    objects = InheritanceManager()

    def save(self, *args, **kwargs):
        if len(self.search_field) == 0:
            self.search_field = populate_search_field(
                (self.name_eng, self.name_kor, self.manufacturer_eng, self.manufacturer_kor))
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return "{}({})".format(self.name_kor, self.name_eng)


class Condom(Product):
    CATEGORY_CHOICES = (
        ("NORMAL", "일반형"),
        ("SLIM", "슬림형"),
        ("CHOBAK", "초박형"),
        ("DOLCHUL", "돌출형"),
        ("GGOKJI", "꼭지형"),
        ("DELAY", "사전지연형"),
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="NORMAL")
    thickness = models.FloatField(default=0, verbose_name="두께")
    length = models.FloatField(default=0, verbose_name="길이")
    width = models.FloatField(default=0, verbose_name="폭")

    avg_oily = models.FloatField(default=0, verbose_name="윤활제 평균")
    avg_thickness = models.FloatField(default=0, verbose_name="두께 평균")
    avg_durability = models.FloatField(default=0, verbose_name="내구성 평균")

    def __str__(self):
        return "{} - {}".format(self.name_kor, self.manufacturer_kor)


class Gel(Product):
    avg_viscosity = models.FloatField(default=0, verbose_name="점성 평균")
