from django.db import models

from model_utils.managers import InheritanceManager

from accounts.models import User
from products.models import Product, Condom, Gel


class Review(models.Model):
    GENDER_CHOICES = ((1, "남"), (2, "여"), (3, "선택안함"))

    user = models.ForeignKey(
        User, verbose_name="작성자", on_delete=models.CASCADE, related_name="user"
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name="성별")
    partner_gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name="상대방 성별")
    content = models.TextField(verbose_name="내용")
    total = models.FloatField(default=0, verbose_name="종합 별점")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="업데이트 시간")

    objects = InheritanceManager()

    # def __str__(self):
    #     return self.user


class ReviewCondom(Review):
    product = models.ForeignKey(
        Condom, verbose_name="콘돔", on_delete=models.CASCADE, related_name="condom",
    )
    oily = models.FloatField(default=0, verbose_name="윤활제 별점")
    thickness = models.FloatField(default=0, verbose_name="두께 별점")
    durability = models.FloatField(default=0, verbose_name="내구성 별점")

    def __str__(self):
        return "{} | {}".format(self.product, self.user)


class ReviewGel(Review):
    product = models.ForeignKey(
        Gel, verbose_name="젤", on_delete=models.CASCADE, related_name="gel",
    )
    viscosity = models.FloatField(default=0, verbose_name="점성")

    def __str__(self):
        return "{} | {}".format(self.product, self.user)
