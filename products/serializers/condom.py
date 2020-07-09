from rest_framework import serializers

from products.models import Condom


class CondomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condom
        fields = [
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
        ]


class CondomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condom
        fields = [
            "id",
            "name_kor",
            "name_eng",
            "thumbnail",
            "image",
            "description",
            "manufacturer_kor",
            "manufacturer_eng",
            "ingredients",
            "num_of_reviews",
            "num_of_views",
            "category",
            "thickness",
            "length",
            "width",
            "score",
            "avg_oily",
            "avg_thickness",
            "avg_durability",
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
