from django.shortcuts import get_object_or_404
from django.db.models import F, Count
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers.sutra import SutraListSerializer, SutraDetailSerializer
from .serializers.evaluation import EvaluationSerializer
from .models import Sutra, Evaluation
from rest_framework.exceptions import ValidationError
from snowflake.exception import MissingJWTException


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

    @swagger_auto_schema(responses={201: "{'detail': 'Evaluation 삭제' }"})
    def delete(self, request, sutra_id):
        evaluation = self.get_object_evaluation(request.user, sutra_id)
        evaluation.delete()
        return Response({
            "detail": "Evaluation 삭제"
        }, status=status.HTTP_204_NO_CONTENT)


