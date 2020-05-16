from django.conf.urls import url, include
from accounts.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password1",
            "password2",
            "username",
            "image",
            "social",
            "gender",
            "partner_gender",
            "date_joined",
        ]
        extra_kwargs = {"date_joined": {"read_only": True}}

    def create(self, validated_data):
        password1 = validated_data.pop("password1", "")
        password2 = validated_data.pop("password2", "")

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")

        user = User.objects.create(**validated_data)
        user.set_password(password1)
        user.save()
        return user
