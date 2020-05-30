from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from reviews.serializers.condom import ReviewCondomSerializer, ReviewCondomListSerializer

from accounts.models import User
from reviews.models import ReviewCondom


class ReviewViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ReviewCondomListSerializer
        return ReviewCondomSerializer
    permission_classes = [AllowAny]
    queryset = ReviewCondom.objects.all()
