from rest_framework import serializers
from django.db.models import Count
import random
from ..models import Sutra, SutraComment


class SutraListSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    def get_comment(self, obj):
        comment_count = obj.sutracomment_set.count()
        if comment_count == 0:
            return None
        random_idx = random.randint(0, comment_count-1)

        comment = SutraComment.objects \
            .select_related('user') \
            .values('user__username', 'content') \
            .all()[random_idx]

        return {
            "username": comment["user__username"],
            "content": comment["content"]
        }

    class Meta:
        model = Sutra
        fields = [
            "id",
            "name_kor",
            "thumbnail",
            "comment"
        ]
