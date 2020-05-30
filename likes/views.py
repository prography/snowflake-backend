from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from likes.models import Like
from likes.serializers.like import LikeSerializer


class LikeViewSet(viewsets.ModelViewSet):
    # def get_permissions(self):
    #     if self.action == 'create':
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     self.perform_create(serializer)
    #     return Response({"message": "회원가입 완료!"}, status=status.HTTP_201_CREATED)
    # def delete(self, request, *args, **kwargs):
    #     print("1")
    #     pass