from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from products.models import Condom
from likes.models import Like


condom_fields = [
    "id",
    "name_kor",
    "name_eng",
    "thumbnail",
    "manufacturer_kor",
    "manufacturer_eng",
    "num_of_views",
    "num_of_reviews",
    "category",
    "score",
    "avg_oily",
    "avg_thickness",
    "avg_durability",
    "likes_count",
]

class CondomListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Condom
        fields = condom_fields

    def get_likes_count(self, obj):
        content_type = ContentType.objects.get(model='product')
        likes_count = Like.objects.filter(content_type=content_type.id, object_id=obj.id).count()
        return likes_count


class CondomDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Condom
        fields = condom_fields + [
            "image",
            "description",
            "ingredients",
            "thickness",
            "length",
            "width",
        ]

    def get_likes_count(self, obj):
        content_type = ContentType.objects.get(model='product')
        likes_count = Like.objects.filter(content_type=content_type.id, object_id=obj.id).count()
        return likes_count


class CondomTopNSerailzier(serializers.ModelSerializer):
    class Meta:
        model = Condom
        fields = [
            "id",
            "name_kor",
            "name_eng",
            "thumbnail",
            "manufacturer_kor",
            "manufacturer_eng",
            "score",
        ]
