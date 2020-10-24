import random

from django.db.models import Count
from drf_yasg import openapi
from rest_framework import serializers

from accounts.serializers.accounts import UserSerializer

from ..models import Evaluation, Sutra, SutraComment


class SutraListSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    recommend_data = serializers.SerializerMethodField()

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

    def get_recommend_data(self, obj):
        user = self.context['request'].user
        try:
            evaluation = Evaluation.objects.get(user=user, sutra=obj)
        except Evaluation.DoesNotExist:
            return None
        recommends_count = obj.purple_recommends_count + obj.sky_recommends_count
        unrecommends_count = obj.purple_unrecommends_count + obj.sky_unrecommends_count

        percentage = (recommends_count /
                        (recommends_count + unrecommends_count)) * 100
        purple_count = obj.purple_recommends_count
        sky_count = obj.sky_recommends_count

        return {
            "percentage": percentage,
            "purple_count": purple_count,
            "sky_count": sky_count
        }

    class Meta:
        model = Sutra

        fields = [
            "id",
            "name_kor",
            "thumbnail",
            "comment",
            "recommend_data"
        ]

class SutraNewCardSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    def get_comment(self, obj):
        comment_count = obj.sutracomment_set.count()
        if comment_count == 0:
            return None
        random_idx = random.randint(0, comment_count-1)

        comment = SutraComment.objects \
            .select_related('user') \
            .values('user__username', 'content') \
            .filter(sutra=obj)[random_idx]
        
        return {
            "username": comment["user__username"],
            "content": comment["content"]
        }

    class Meta:
        model = Sutra
        fields = [
            'id',
            'name_kor',
            'thumbnail',
            'comment'
        ]
