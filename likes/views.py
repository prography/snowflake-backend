from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from likes.models import Like
from likes.serializers.like import LikeSerializer


class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        """
        새 좋아요를 만듭니다.
        """
        data = {'model': request.data.get('model'),
                'object_id': int(request.data.get('object_id')),
                'user': int(request.data.get('user'))}
        model = data.pop('model')
        try:
            ct = ContentType.objects.get(model=model)
        # django.contrib.contenttypes.models.ContentType.DoesNotExist:
        except:
            return Response("content_type 이름이 잘못되었습니다.", status=status.HTTP_400_BAD_REQUEST)
        data['content_type'] = ct.id

        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
