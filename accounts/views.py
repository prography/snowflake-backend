from django.shortcuts import render

# ViewSets define the view behavior.
from rest_framework import viewsets

from accounts.models import CustomUser
from accounts.serializers.accounts import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
