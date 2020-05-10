import os
from uuid import uuid4

from django.db import models
from django.utils import timezone


def create_path(instance, filename):
    ymd_path = timezone.localtime().strftime("%Y-%m-%d-%H%M%S")
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return "/".join(["home", "welcome_card", 'image', ymd_path + "-" + uuid_name + extension])


# Create your models here.
class WelcomeCard(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # WelcomeCard의 버튼을 클릭하면 redirect할 주소
    button_src = models.URLField(max_length=2000)
    # WelcomeCard의 이미지
    image = models.ImageField(upload_to=create_path, blank=True, null=True)

    # 카드의 메인 화면에서의 위치 지정
    row = models.IntegerField(default=-1)
    col = models.IntegerField(default=0)

    # 이 카드가 보여질지 말지, 삭제된 카드인지 여부
    STATUS_CHOICES = (
        ('DEL', 'Deleted'),
        ('DRAFT', 'Draft'),
        ('PUB', 'Published')
    )
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title
