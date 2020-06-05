from rest_framework import serializers

from accounts.serializers import accounts

from reviews.models import ReviewCondom


condom_filelds = [
    "id",
    "user",
    "gender",
    "partner_gender",
    "total",
    "product",
    "created_at",
    "updated_at",
    "oily",
    "thickness",
    "durability",
    "content",
]


class ReviewCondomListSerializer(serializers.ModelSerializer):
    user = accounts.ReviewUserSerializer(read_only=True)

    class Meta:
        model = ReviewCondom
        fields = condom_filelds


class ReviewCondomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReviewCondom
        fields = condom_filelds
