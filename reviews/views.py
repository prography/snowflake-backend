from rest_framework import viewsets, permissions
from rest_framework import generics

from reviews.serializers.condom import ReviewCondomSerializer, ReviewCondomListSerializer

from accounts.models import User
from reviews.models import ReviewCondom, Review


class AnonCreateAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        # 익명 유저를 위한 조회
        return (
            view.action in ["list", "retrieve"] or request.user and request.user.is_authenticated
        )  # 유저에 의한 수정

    def has_object_permission(self, request, view, obj):
        if view.action in ["list", "retrieve"]:
            return True
        return (
            view.action in ["create", "update", "partial_update"]
            and obj.id == request.user.id
            or request.user.is_staff
        )


class ReviewCondomViewSet(viewsets.ModelViewSet):
    permission_classes = [AnonCreateAndUpdateOwnerOnly]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ReviewCondomListSerializer
        return ReviewCondomSerializer

    def get_queryset(self):
        queryset = Review.objects.all()

        product = self.request.query_params.get("product", None)
        if product is not None:
            return queryset.filter(product=product)
        return queryset
