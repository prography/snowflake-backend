from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from accounts.models import User
from products.models import Product


class Review(models.Model):
    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE, related_name="user")
    product = models.ForeignKey(Product, verbose_name="제품", on_delete=models.CASCADE, related_name="product")
    content = models.TextField()

    def __str__(self):
        return self.product.name
