from django.shortcuts import get_object_or_404
from django.db.models import F, Count
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers.sutra import SutraListSerializer
from .serializers.evaluation import EvaluationSerializer
from .models import Sutra, Evaluation


class SutraListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SutraListSerializer

    def get_queryset(self):
        # filtering : 추천, 비추천, 안해봤어요, 찜
        filtering = self.request.query_params.get("filter", None)
        # ordering : 최신순, 평가개수순, 추천순, 비추천순, 안해봤어요 순, 찜순
        ordering = self.request.query_params.get("order", None)

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
                evaluations__use=self.request.user,
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


class EvaluationView(APIView):
    serializer_class = EvaluationSerializer

    def get_object_evaluation(self, user, sutra_id):
        evaluation = get_object_or_404(
            Evaluation, user=user, sutra__id=sutra_id)
        return evaluation

    def get_object_sutra(self, sutra_id):
        sutra = get_object_or_404(Sutra, id=sutra_id)
        return sutra

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

    def delete(self, request, sutra_id):
        evaluation = self.get_object_evaluation(request.user, sutra_id)
        evaluation.delete()
        return Response({
            "detail": "Evaluation 삭제"
        }, status=status.HTTP_204_NO_CONTENT)
