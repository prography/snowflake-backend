from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from home.models import DesignType
from likes.models import Like
import os
from uuid import uuid4


def create_path(instance, filename):
    ymd_path = timezone.localtime().strftime("%Y-%m-%d-%H%M%S")
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return "/".join(["labs", "welcome_card", "image", ymd_path + "-" + uuid_name + extension])


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

    design_type = models.ForeignKey(
        DesignType, on_delete=models.SET_NULL, null=True, related_name="lab_welcome_card")

    CATEGORY_CHOICES = (("NONE", "지정안됨"), ("SUTRA", "눈송수트라"),
                        ("ATOZ", "A to Z"), ("SONG_DOCTOR", "송박사의 연구소"))
    # 카드의 메인 화면에서의 위치 지정
    category = models.CharField(
        max_length=30, choices=CATEGORY_CHOICES, default="NONE")
    sequence = models.IntegerField(default=-1)

    # 이 카드가 보여질지 말지, 삭제된 카드인지 여부
    STATUS_CHOICES = (("DEL", "Deleted"), ("DRAFT", "Draft"),
                      ("PUB", "Published"))
    status = models.CharField(
        max_length=5, choices=STATUS_CHOICES, default="DRAFT")

    def __str__(self):
        return self.title


def create_path(directory, filename):
    ymd_path = timezone.localtime().strftime("%Y-%m-%d-%H%M%S")
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return "/".join(["labs", "sutra", directory, ymd_path + "-" + uuid_name + extension])


def create_thumbnail_path(instance, filename):
    return create_path("thumbnail", filename)


def create_image_path(instance, filename):
    return create_path("image", filename)

    STATUS_CHOICES = (("DEL", "Deleted"), ("DRAFT", "Draft"),
                      ("PUB", "Published"))
    status = models.CharField(
        max_length=5, choices=STATUS_CHOICES, default="DRAFT")


class Evaluation(models.Model):
    RECOMMEND_TYPE_CHOICES = (
        ("RECOMMEND", "추천"), ("UNRECOMMEND", "비추천"), ("NOTYET", "안해봄"))
    USER_TYPE_CHOICES = (("PURPLE", "보라두리"), ("SKY", "하늘이"))

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    sutra = models.ForeignKey(
        'Sutra', related_name='evaluations', on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES)
    recommend_type = models.CharField(
        max_length=20, choices=RECOMMEND_TYPE_CHOICES)

    class Meta:
        unique_together = [['user', 'sutra']]

    def __str__(self):
        return f'{self.user}의 {self.sutra}에 대한 eval'


class Sutra(models.Model):
    name_kor = models.CharField(max_length=255, null=True, blank=True)
    name_eng = models.CharField(max_length=255, null=True, blank=True)

    thumbnail = models.ImageField(
        upload_to=create_thumbnail_path, blank=True, null=True)
    image = models.ImageField(
        upload_to=create_image_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    likes = GenericRelation(Like)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    purple_recommends_count = models.IntegerField(
        default=0, help_text="보라두리의 추천수")
    purple_unrecommends_count = models.IntegerField(
        default=0, help_text="보라두리의 비추천수")
    sky_recommends_count = models.IntegerField(default=0, help_text="하늘이의 추천수")
    sky_unrecommends_count = models.IntegerField(
        default=0, help_text="하늘이의 비추천수")
    not_yet_count = models.IntegerField(default=0, help_text="안해봤어요 수")
    likes_count = models.IntegerField(default=0, help_text="찜 수")

    def __str__(self):
        return self.name_kor


class SutraComment(models.Model):
    USER_POSITION_CHOICES = (
        ("PURPLE", "보라두리"), ("SKY", "하늘이"), ("NONE", "선택안함"))

    sutra = models.ForeignKey(
        Sutra, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    user_position = models.CharField(
        max_length=20, choices=USER_POSITION_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like)
    likes_count = models.IntegerField(default=0, help_text="찜 수")

    def __str__(self):
        return self.content[:20]
