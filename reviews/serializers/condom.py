from rest_framework import serializers

from accounts.serializers import accounts

from reviews.models import ReviewCondom


condom_filelds = [
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


class ReviewCondomListSerializer(serializers.ModelSerializer):
    user = accounts.ReviewUserSerializer(read_only=True)

    class Meta:
        model = ReviewCondom
        fields = condom_filelds


class ReviewCondomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewCondom
        fields = condom_filelds
