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
    "likes_count",
]


class ReviewCondomListSerializer(serializers.ModelSerializer):
    user = accounts.ReviewUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = ReviewCondom
        fields = condom_fields

    def get_likes_count(self, obj):
        content_type = ContentType.objects.get(model='review')
        likes_count = Like.objects.filter(content_type=content_type.id, object_id=obj.id).count()
        return likes_count


class ReviewCondomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReviewCondom
        fields = condom_fields
