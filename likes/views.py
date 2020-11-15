from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from likes.models import Like
from likes.serializers.like import LikeSerializer, LikeWithProductDetailSerializer


class LikeView(APIView):
    """
    좋아요

    여러 모델에 대한 범용적인 좋아요 기능
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        is_product_detail = self.request.query_params.get(
            'is_product_detail', None)
        if is_product_detail and is_product_detail.lower() == 'true':
            return LikeWithProductDetailSerializer
        return LikeSerializer

    model_param = openapi.Parameter(
        'model', openapi.IN_QUERY, description="product | review | sutra | sutracomment", type=openapi.TYPE_STRING)
    object_id_param = openapi.Parameter(
        'object_id', openapi.IN_QUERY, description="해당 객체의 id", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[model_param, object_id_param])
    def post(self, request):
        data = {
            'object_id': int(request.data.get('object_id')),
            'user': request.user.id
        }
        model = request.data.get('model')
        try:
            ct = ContentType.objects.get(model=model)
        except ContentType.DoesNotExist:
            return Response({"message": "model 이름이 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        data['content_type'] = ct.id

        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[model_param, object_id_param])
    def delete(self, request):
        object_id = request.data.get('object_id')
        user = request.user
        model = request.data.get('model')

        try:
            ct = ContentType.objects.get(model=model)
        except ContentType.DoesNotExist:
            return Response({"message": "model 이름이 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            like = Like.objects.get(
                object_id=object_id,
                user=user,
                content_type=ct
            )
            like.delete()
        except Like.DoesNotExist:
            return Response({"message": "해당 좋아요가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "like를 삭제하였습니다."}, status=status.HTTP_204_NO_CONTENT)
