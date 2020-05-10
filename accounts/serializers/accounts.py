from django.conf.urls import url, include
from accounts.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "nickname",
            "image",
            "social",
            "gender",
            "partner_gender",
            "date_joined",
        ]
