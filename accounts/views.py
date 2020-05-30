from django.shortcuts import render

# ViewSets define the view behavior.
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers.accounts import UserSerializer


class AnonCreateAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return view.action == 'create' or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return view.action in ['retrieve', 'update',
                               'partial_update'] and obj.id == request.user.id or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    # def get_permissions(self):
    #     if self.action == 'create':
    permission_classes = [AnonCreateAndUpdateOwnerOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response({"message": "회원가입 완료!"}, status=status.HTTP_201_CREATED)
