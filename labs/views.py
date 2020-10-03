from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers.sutra import SutraListSerializer
from .models import Sutra


class SutraListView(generics.ListAPIView):
    # 이거 왜 AllowAny?
    permission_classes = [AllowAny]
    serializer_class = SutraListSerializer
    queryset = Sutra.objects.all()
