from rest_framework import serializers
from django.db.models import Count
import random
from ..models import Sutra, SutraComment, Evaluation
from likes.models import Like
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method


def calculate_percentage(recommends_count, unrecommends_count):
    if recommends_count + unrecommends_count == 0:
        percentage = 0
    else:
        percentage = (recommends_count /
                      (recommends_count + unrecommends_count)) * 100

    return percentage


class SutraListSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    recommend_data = serializers.SerializerMethodField()
    is_user_like = serializers.SerializerMethodField()

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

        percentage = calculate_percentage(recommends_count, unrecommends_count)
        purple_count = obj.purple_recommends_count
        sky_count = obj.sky_recommends_count

        return {
            "percentage": percentage,
            "purple_count": purple_count,
            "sky_count": sky_count
        }

    def get_is_user_like(self, obj) -> bool:
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
            "is_user_like"
        ]


class SutraDetailSerializer(serializers.ModelSerializer):
    is_user_like = serializers.SerializerMethodField()
    recommend_data = serializers.SerializerMethodField()

    def get_is_user_like(self, obj) -> bool:
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

    def get_recommend_data(self, obj)->dict:
        user = self.context['request'].user
        try:
            evaluation = Evaluation.objects.get(user=user, sutra=obj)
        except Evaluation.DoesNotExist:
            return None
        recommends_count = obj.purple_recommends_count + obj.sky_recommends_count
        unrecommends_count = obj.purple_unrecommends_count + obj.sky_unrecommends_count

        toal_percentage = calculate_percentage(
            recommends_count,
            unrecommends_count
        )
        purple_count = obj.purple_recommends_count
        sky_count = obj.sky_recommends_count

        purple_percentage = calculate_percentage(
            obj.purple_recommends_count,
            obj.purple_unrecommends_count
        )

        sky_percentage = calculate_percentage(
            obj.sky_recommends_count,
            obj.sky_unrecommends_count
        )

        return {
            "total_percentage": toal_percentage,
            "recommends_count": recommends_count,
            "unrecommends_count": unrecommends_count,
            "purple_percentage": purple_percentage,
            "purple_count": purple_count,
            "sky_percentage": purple_percentage,
            "sky_count": sky_count,
        }

    class Meta:
        model = Sutra
        fields = [
            'id',
            'image',
            'name_kor',
            'name_eng',
            'description',
            'created_at',
            'is_user_like',
            'recommend_data',
            'not_yet_count',
            'likes_count'
        ]


# 1. 이미지
# 2. 체위 한글 이름
# 3. 체위 영어 이름
# 4. 체위 설명
# 5. user가 찜했는지 / user가 찜할 수 있게
# 6. 추천도 & 추천 수 & 비추천 수
# 7. 보라두리의 추천도 & 추천 수
# 8. 하늘이의 추천도 & 추천 수
# 9. 안 해봤어요 비율 & 안 해봤어요 수
# 10. 찜콩 비율 & 찜 수

# 11. user가 추천/비추했는지 / user가 추천, 비추할 수 있게
# 12. user가 안 해봤는지 / user가 안 해봤어요 누를 수 있게
