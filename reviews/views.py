from rest_framework import viewsets
from rest_framework import generics

from rest_framework.permissions import AllowAny

from reviews.serializers.condom import ReviewCondomSerializer, ReviewCondomListSerializer

from accounts.models import User
from reviews.models import ReviewCondom, Review


class ReviewCondomViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ReviewCondomListSerializer
        return ReviewCondomSerializer

    permission_classes = [AllowAny]
    queryset = Review.objects.all()


class ReviewProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewCondomListSerializer

    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs["product"])
