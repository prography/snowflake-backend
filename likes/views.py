from django.contrib.contenttypes.models import ContentType

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from likes.models import Like
from likes.serializers.like import LikeSerializer, LikeWithProductDetailSerializer


class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        is_product_detail = self.request.query_params.get('is_product_detail', None)
        if is_product_detail and is_product_detail.lower() == 'true':
            return LikeWithProductDetailSerializer
        return LikeSerializer

    def get_queryset(self):
        queryset = Like.objects.filter(user=self.request.user)
        model = self.request.query_params.get('model', None)
        if model is not None:
            ct = ContentType.objects.get(model=model)
            queryset = queryset.filter(content_type=ct.id)
        object_id = self.request.query_params.get('object_id', None)
        if object_id is not None:
            queryset = queryset.filter(object_id=object_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        새 좋아요를 만듭니다.
        """
        data = {'model': request.data.get('model'),
                'object_id': int(request.data.get('object_id')),
                'user': self.request.user.id}
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
