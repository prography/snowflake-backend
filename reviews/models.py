from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from model_utils.managers import InheritanceManager

from accounts.models import User
from likes.models import Like
from products.models import Product, Condom, Gel


class Review(models.Model):
    GENDER_CHOICES = (("MAN", "남"), ("WOMAN", "여"), ("NONE", "none"))

    user = models.ForeignKey(
        User, verbose_name="작성자", on_delete=models.CASCADE, related_name="review"
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="NONE")
    partner_gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="NONE")

    content = models.TextField(verbose_name="내용")
    total = models.FloatField(default=0, verbose_name="종합 별점")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="업데이트 시간")

    product = models.ForeignKey(
        Product, verbose_name="제품", on_delete=models.CASCADE, related_name="review",
    )
    objects = InheritanceManager()

    likes = GenericRelation(Like)

    # def __str__(self):
    #     return self.user


class ReviewCondom(Review):
    oily = models.FloatField(default=0, verbose_name="윤활제 별점")
    thickness = models.FloatField(default=0, verbose_name="두께 별점")
    durability = models.FloatField(default=0, verbose_name="내구성 별점")

    def __str__(self):
        return "{} | {}".format(self.product, self.user)


class ReviewGel(Review):
    # product = models.ForeignKey(
    #     Gel, verbose_name="젤", on_delete=models.CASCADE, related_name="review_gel",
    # )
    viscosity = models.FloatField(default=0, verbose_name="점성")

    def __str__(self):
        return "{} | {}".format(self.product, self.user)
