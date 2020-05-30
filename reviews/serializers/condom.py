from rest_framework import serializers

from accounts.serializers import accounts

from reviews.models import ReviewCondom
from accounts.models import User


class ReviewCondomListSerializer(serializers.ModelSerializer):
    user = accounts.ReviewUserSerializer(read_only=True)

    class Meta:
        model = ReviewCondom
        fields = [
            "id",
            "user",
            "total",
            "product",
            "oily",
            "thickness",
            "durability",
        ]


class ReviewCondomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewCondom
        fields = [
            "id",
            "user",
            "total",
            "product",
            "oily",
            "thickness",
            "durability",
            "created_at",
            "updated_at",
        ]
