from django.shortcuts import render

# ViewSets define the view behavior.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from accounts.models import User
from accounts.serializers.accounts import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    # def get_permissions(self):
    #     if self.action == 'create':
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
