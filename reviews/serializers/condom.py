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
    num_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = ReviewCondom
        fields = condom_fields

    def get_num_of_likes(self, obj):
        content_type = ContentType.objects.get(model='review')
        num_of_likes = Like.objects.filter(content_type=content_type.id, object_id=obj.id).count()
        return num_of_likes


class ReviewCondomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReviewCondom
        fields = condom_fields
