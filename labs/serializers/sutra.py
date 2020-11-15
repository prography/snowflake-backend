import random

from rest_framework import serializers

from likes.models import Like
from ..models import Evaluation, Sutra, SutraComment


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
