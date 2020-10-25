from rest_framework import serializers
from django.db.models import Count
import random
from ..models import Sutra, SutraComment, Evaluation
from likes.models import Like
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method


class SutraListSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    recommend_data = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    def get_comment(self, obj)->dict:
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

    def get_recommend_data(self, obj)->dict:
        user = self.context['request'].user
        try:
            evaluation = Evaluation.objects.get(user=user, sutra=obj)
        except Evaluation.DoesNotExist:
            return None
        recommends_count = obj.purple_recommends_count + obj.sky_recommends_count
        unrecommends_count = obj.purple_unrecommends_count + obj.sky_unrecommends_count

        if recommends_count + unrecommends_count == 0:
            percentage = 0
            purple_count = 0
            sky_count = 0
        else:
            percentage = (recommends_count /
                          (recommends_count + unrecommends_count)) * 100
            purple_count = obj.purple_recommends_count
            sky_count = obj.sky_recommends_count

        return {
            "percentage": percentage,
            "purple_count": purple_count,
            "sky_count": sky_count
        }

    def get_like(self, obj) -> bool:
        user = self.context['request'].user
        if user.is_anonymous:
            return False

        try:
            Like.objects.get(
                user=user,
                object_id=obj.id,
                content_type=19
            )
        except Like.DoesNotExist:
            return False
        return True

    class Meta:
        model = Sutra

        fields = [
            "id",
            "name_kor",
            "thumbnail",
            "comment",
            "recommend_data",
            "like"
        ]
