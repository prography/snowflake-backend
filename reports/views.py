from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reports.models import Report
from reports.serializer import ReportSerializer


class ReportViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    신고하기

    token 필수!!

    post 요청 시, {'model': string, 'object_id': string} 이렇게만 넣어주면 됨
    content_type이 필수라고 되어있는데, model 이름을 통해 content_type을 찾아주어서 모델 이름만 넣어주면 됨

    눈송수트라 댓글 모델 이름: sutracomment

    model을 잘못 넣었을 경우, {'message': "content_type 이름이 잘못되었습니다."} 메시지와 함께 400에러 발생
    """
    permission_classes = [IsAuthenticated]
    queryset = Report.objects.all()

    @swagger_auto_schema(request_body=ReportSerializer, responses={201: ReportSerializer})
    def create(self, request, *args, **kwargs):
        data = {'model': request.data.get('model'), 'object_id': int(request.data.get('object_id')), 'user': self.request.user.id}
        model = data.pop('model')
        try:
            content_type = ContentType.objects.get(model=model)
        except ValueError:
            return Response({'message': "content_type 이름이 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        data['content_type'] = content_type.id

        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "{'message': '삭제 완료!' }"})
    def destroy(self, request, comment_id=None, *args, **kwargs):
        response = super()
        response.data = {'message': '삭제 완료!'}
        return response
