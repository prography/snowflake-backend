from rest_framework import serializers

from products.models import Condom


class CondomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condom
        fields = [
            "name",
            "thumbnail",
            "manufacturer",
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
            "name",
            "thumbnail",
            "image",
            "description",
            "manufacturer",
            "ingredients",
            "num_of_reviews",
            "category",
            "thickness",
            "length",
            "width",
            "score",
            "avg_oily",
            "avg_thickness",
            "avg_durability",
        ]
