from django.conf.urls import include, url
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User, Icon


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True, style={
                                     "input_type": "password"})

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
            "color",
            "icon",
            "position",
        ]
        depth = 1  # You need only add this sentence.
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


class CustomUserObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['social'] = user.social
        token['birth_year'] = user.birth_year
        token['gender'] = user.gender
        return token
