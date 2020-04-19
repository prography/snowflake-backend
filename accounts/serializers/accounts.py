from django.conf.urls import url, include
from accounts.models import CustomUser
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'nickname', 'date_joined']
