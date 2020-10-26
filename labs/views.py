import random
from django.db.models import Count, F
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers.sutra import SutraListSerializer, SutraDetailSerializer, SutraNewCardSerializer
from .serializers.evaluation import EvaluationSerializer
from .models import Sutra, Evaluation, SutraComment
from snowflake.exception import MissingJWTException
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from likes.models import Like
from likes.serializers.like import LikeSerializer
from snowflake.permission import AnonCreateAndUpdateOwnerOnly
from .models import Sutra, Evaluation, SutraComment
from .serializers.comment import SutraCommentSerializer, SutraCommentListSerializer
from .serializers.evaluation import EvaluationSerializer
from .serializers.sutra import SutraListSerializer


class SutraListView(generics.ListAPIView):
    """
    order => default: 최신순 | 평가개수순: evaluation | 추천순: recommend | 비추천순: unrecommend | 안해봤어요 순: notyet | 찜순: like
    filter => 추천: recommend | 비추천: unrecommend | 안해봤어요: notyet | 찜: like
    """
    permission_classes = [AllowAny]
    serializer_class = SutraListSerializer

    def get_queryset(self):
        # filtering : 추천, 비추천, 안해봤어요, 찜
        filtering = self.request.query_params.get("filter", None)
        # ordering : 최신순, 평가개수순, 추천순, 비추천순, 안해봤어요 순, 찜순
        ordering = self.request.query_params.get("order", None)
        if filtering and self.request.user.is_anonymous:
            raise MissingJWTException

        queryset = Sutra.objects.all()

        if filtering is None:
            pass
        # 찜
        elif filtering == 'like':
            queryset = Sutra.objects.filter(
                likes__user=self.request.user
            )
        # 추천, 비추천, 안해봤어요
        else:
            recommend_type = filtering.upper()
            queryset = Sutra.objects.filter(
                evaluations__user=self.request.user,
                evaluations__recommend_type=recommend_type)

        # 최신순
        if ordering is None:
            queryset = queryset.order_by('-id')
        # 평가개수순
        elif ordering == 'evaluation':
            queryset = queryset \
                .annotate(eval_count=F("purple_recommends_count") +
                          F("purple_unrecommends_count") +
                          F("sky_recommends_count") +
                          F("sky_unrecommends_count") +
                          F("not_yet_count")) \
                .order_by('-eval_count')
        # 추천순
        elif ordering == 'recommend':
            queryset = queryset \
                .annotate(recommends_count=F("purple_recommends_count")+F("purple_unrecommends_count")) \
                .order_by('-recommends_count')
        # 비추천순
        elif ordering == 'unrecommend':
            queryset = queryset \
                .annotate(unrecommends_count=F("sky_recommends_count")+F("sky_unrecommends_count")) \
                .order_by('-unrecommends_count')
        # 안해봤어요 순
        elif ordering == 'notyet':
            queryset = queryset.order_by('-not_yet_count')

        # 찜순
        elif ordering == 'like':
            queryset = queryset.order_by('-likes_count')

        return queryset

    order_param = openapi.Parameter(
        'order', openapi.IN_QUERY, description="evaluation | recommend | unrecommend | notyet | like", type=openapi.TYPE_STRING)
    filter_param = openapi.Parameter(
        'filter', openapi.IN_QUERY, description="recommend | unrecommend | notyet | like", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[order_param, filter_param])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SutraDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = SutraDetailSerializer
    queryset = Sutra.objects.all()


class SutraNewCardView(APIView):
    """
    가장 최근에 생성된 Sutra를 가져옵니다.
    그것의 댓글이 있으면 랜덤으로 댓글을 가져옵니다.
    """
    permission_classes = [AllowAny]
    serializer_class = SutraNewCardSerializer

    @swagger_auto_schema(responses={200: SutraNewCardSerializer})
    def get(self, request, formant=None):
        latest_sutra = Sutra.objects.order_by('-created_at')[0]
        serializer = self.serializer_class(latest_sutra)
        return Response(serializer.data)


class EvaluationView(APIView):
    serializer_class = EvaluationSerializer

    def get_object_evaluation(self, user, sutra_id):
        evaluation = get_object_or_404(
            Evaluation, user=user, sutra__id=sutra_id)
        return evaluation

    def get_object_sutra(self, sutra_id):
        sutra = get_object_or_404(Sutra, id=sutra_id)
        return sutra

    @swagger_auto_schema(request_body=EvaluationSerializer, responses={201: "{'detail': 'Evaluation 생성' }"})
    def post(self, request, sutra_id):
        sutra = self.get_object_sutra(sutra_id)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, sutra=sutra)

            return Response({
                "detail": "Evaluation 생성"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "detail": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "{'detail': 'Evaluation 삭제' }"})
    def delete(self, request, sutra_id):
        evaluation = self.get_object_evaluation(request.user, sutra_id)
        evaluation.delete()
        return Response({
            "detail": "Evaluation 삭제"
        }, status=status.HTTP_204_NO_CONTENT)


class SutraCommentViewSet(viewsets.ModelViewSet):
    """
    눈송수트라 댓글

    get 제외 토큰 필수!!
    put은 사용하지 않는다. patch로만 업데이트!

    list 정렬은 기본이 최신순. url parameter로 `order=likes_count` 를 해주면 좋아요 순으로 정렬된다.
    """
    permission_classes = [AnonCreateAndUpdateOwnerOnly]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return SutraCommentListSerializer
        return SutraCommentSerializer

    def get_queryset(self):
        sutra_id = self.kwargs.get('sutra_id')
        order = self.request.query_params.get("order")
        if order is None:
            queryset = SutraComment.objects.filter(sutra__id=sutra_id).order_by('-created_at')
        else:
            # order = likes_count
            queryset = SutraComment.objects.filter(sutra__id=sutra_id).order_by(f'-{order}')
        return queryset

    def create(self, request, sutra_id=None, *args, **kwargs):
        request.data._mutable = True
        request.data['sutra'] = sutra_id
        request.data['user_position'] = request.user.position
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SutraCommentLikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    눈송스트라 댓글 좋아요

    token 필수!!
    form 필요 없이 api 요청만 해주면 됨
    """
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()

    @swagger_auto_schema(request_body=LikeSerializer, responses={201: LikeSerializer})
    def create(self, request, comment_id=None, *args, **kwargs):
        data = {'object_id': comment_id, 'user': self.request.user.id}
        content_type = ContentType.objects.get(model='sutracomment')
        data['content_type'] = content_type.id

        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            SutraComment.objects.filter(pk=comment_id).update(likes_count=F('likes_count')+1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "{'message': '삭제 완료!' }"})
    def destroy(self, request, comment_id=None, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        SutraComment.objects.filter(pk=comment_id).update(likes_count=F('likes_count')-1)
        return Response(data={'message': '삭제 완료!'}, status=status.HTTP_204_NO_CONTENT)