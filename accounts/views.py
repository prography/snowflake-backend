from django.shortcuts import render

# ViewSets define the view behavior.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers.accounts import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    # def get_permissions(self):
    #     if self.action == 'create':
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        return Response({"message": "회원가입 완료!"}, status=status.HTTP_201_CREATED)
