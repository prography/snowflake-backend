from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from labs.models import SutraComment
from likes.models import Like

comment_fields = [
    "id",
    "sutra",
    "user",
    "user_position",
    "content",
    "likes_count",
    "created_at",
    "updated_at"
]


class SutraCommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "position",
            "image",
        ]


class SutraCommentListSerializer(serializers.ModelSerializer):
    user = SutraCommentUserSerializer(read_only=True)
    is_user_like = serializers.SerializerMethodField()

    def get_is_user_like(self, obj) -> bool:
        user = self.context['request'].user
        if user.is_anonymous:
            return False

        try:
            Like.objects.get(
                user=user,
                object_id=obj.id,
                content_type=ContentType.objects.get(model='sutracomment').id
            )
        except Like.DoesNotExist:
            return False
        return True

    class Meta:
        model = SutraComment
        fields = [
            "id",
            "user",
            "user_position",
            "content",
            "is_user_like",
            "likes_count",
            "created_at",
            "updated_at"
        ]


class SutraCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SutraComment
        fields = [
            "user",
            "content",
        ] + comment_fields
