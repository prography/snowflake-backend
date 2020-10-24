from rest_framework import serializers

from accounts.models import User
from labs.models import SutraComment


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
        model = User
        fields = [
            "id",
            "username",
            "position",
            "image",
        ]


class SutraCommentListSerializer(serializers.ModelSerializer):
    user = SutraCommentUserSerializer(read_only=True)

    class Meta:
        model = SutraComment
        fields = [
            "id",
            "user",
            "user_position",
            "content",
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
        ]

