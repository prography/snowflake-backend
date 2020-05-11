from django.db import models

from model_utils.managers import InheritanceManager

from accounts.models import User
from products.models import Product, Condom, Gel


class Review(models.Model):
    user = models.ForeignKey(
        User, verbose_name="작성자", on_delete=models.CASCADE, related_name="user"
    )
    content = models.TextField()
    total = models.FloatField(default=0, verbose_name="종합 별점")

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
