from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from likes.models import Like
from likes.serializers.like import LikeSerializer
from snowflake.exception import MissingJWTException
from snowflake.permission import AnonCreateAndUpdateOwnerOnly
from .models import Evaluation, Sutra, SutraComment
from .serializers.comment import SutraCommentListSerializer, SutraCommentSerializer
from .serializers.evaluation import EvaluationSerializer
from .serializers.sutra import SutraDetailSerializer, SutraNewCardSerializer
from .serializers.sutra import SutraListSerializer


class SutraListView(generics.ListAPIView):
    """
    눈송수트라 조회

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
    """
    눈송수트라 상세조회

    눈송수트라 상세조회 API
    """
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
    """
    눈송수트라 평가

    눈송수트라 평가 API
    """
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

    토큰 필수! get의 경우 토큰이 없는 경우(로그인 안한 경우)만 토큰 없이 보낼 것
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
        request.data['sutra'] = sutra_id
        request.data['user_position'] = request.user.position
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
