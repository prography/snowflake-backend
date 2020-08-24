from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from accounts.serializers import accounts

from reviews.models import ReviewCondom
from likes.models import Like


condom_fields = [
    "id",
    "product",
    "user",
    "gender",
    "partner_gender",
    "total",
    "created_at",
    "updated_at",
    "oily",
    "thickness",
    "durability",
    "content",
    "num_of_likes",
]


class ReviewCondomListSerializer(serializers.ModelSerializer):
    user = accounts.ReviewUserSerializer(read_only=True)

    class Meta:
        model = ReviewCondom
        fields = condom_fields


class ReviewCondomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReviewCondom
        fields = condom_fields
