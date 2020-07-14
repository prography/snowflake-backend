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
    "num_of_likes",
]

class CondomListSerializer(serializers.ModelSerializer):
    num_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Condom
        fields = condom_fields

    def get_num_of_likes(self, obj):
        content_type = ContentType.objects.get(model='product')
        num_of_likes = Like.objects.filter(content_type=content_type.id, object_id=obj.id).count()
        obj.num_of_likes = num_of_likes
        obj.save()
        return num_of_likes


class CondomDetailSerializer(serializers.ModelSerializer):
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
