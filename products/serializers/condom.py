from rest_framework import serializers
from products.models import Condom


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
    class Meta:
        model = Condom
        fields = condom_fields


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
