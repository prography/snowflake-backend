from django.conf.urls import url, include
from accounts.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})
    # password2 = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "username",
            "birth_year",
            "image",
            "social",
            "gender",
            "partner_gender",
            "date_joined",
        ]
        extra_kwargs = {"date_joined": {"read_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", "")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "birth_year",
            "image",
        ]
