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
            queryset = queryset.filter(product=product)

        order = self.request.query_params.get("order", None)
        gender = self.request.query_params.get("gender", None)
        partner = self.request.query_params.get("partner", None)

        if order is not None:
            if order == "high_score":
                queryset = queryset.order_by("-total")
            elif order == "low_score":
                queryset = queryset.order_by("total")
            else:
                raise NotFound()

        if gender is not None:
            if gender == "man":
                queryset = queryset.filter(user__gender="MAN")
            elif gender == "woman":
                queryset = queryset.filter(user__gender="WOMAN")
            else:
                raise NotFound()

        if partner is not None:
            if partner == "man":
                queryset = queryset.filter(user__partner_gender="MAN")
            elif partner == "woman":
                queryset = queryset.filter(user__partner_gender="WOMAN")
            else:
                raise NotFound()

        return queryset.order_by("-id")
