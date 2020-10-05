from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers.sutra import SutraListSerializer
from .serializers.evaluation import EvaluationSerializer
from .models import Sutra, Evaluation


class SutraListView(generics.ListAPIView):
    # 이거 왜 AllowAny?
    permission_classes = [AllowAny]
    serializer_class = SutraListSerializer
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
