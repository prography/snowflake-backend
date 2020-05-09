from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


class Product(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="products/thumbnail/", blank=True, null=True)
    image = models.ImageField(upload_to="products/image/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(default=0)
    ingredients = models.TextField(blank=True, null=True)
    num_of_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    num_of_views = models.BigIntegerField(default=0)

    # content_type definition
    limit = models.Q(app_label='products', model='condom') | models.Q(app_label='products', model='gel')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name


class Condom(models.Model):
    oily = models.FloatField(default=0, verbose_name="윤활제")
    thickness = models.FloatField(default=0, verbose_name="두께")
    durability = models.FloatField(default=0, verbose_name="내구성")

    # Reverse to content_type parent object
    product = GenericRelation(Product, related_query_name='product')

    def __str__(self):
        p = self.product.first()
        return "{}_{}".format(p.manufacturer, p.name) or "!!!"


class Gel(models.Model):
    viscosity = models.FloatField(default=0, verbose_name="점성")

    # Reverse to content_type parent object
    product = GenericRelation(Product, related_query_name='product')
