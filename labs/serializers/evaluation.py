from rest_framework import serializers
from ..models import Evaluation, Sutra
from django.db.utils import IntegrityError


class EvaluationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        user = validated_data["user"]
        sutra = validated_data["sutra"]
        evaluation = Evaluation(
            user=user,
            sutra=sutra,
            user_type=user.position,
            recommend_type=validated_data["recommend_type"],
        )

        try:
            evaluation.save()
        except IntegrityError:
            raise serializers.ValidationError(
                {"message": f"{user}의 {sutra}에 대한 evaluation이 이미 존재합니다."})
        return evaluation
