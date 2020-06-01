from rest_framework import viewsets, permissions, generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from reviews.serializers.condom import ReviewCondomSerializer, ReviewCondomListSerializer

from accounts.models import User
from reviews.models import ReviewCondom, Review, ReviewGel
from products.models import Condom

from django.db.models import F


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
            view.action in ["create", "update",
                            "partial_update"] and obj.id == request.user.id or request.user.is_staff
        )


class ReviewCondomViewSet(viewsets.ModelViewSet):
    permission_classes = [AnonCreateAndUpdateOwnerOnly]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ReviewCondomListSerializer
        return ReviewCondomSerializer

    def get_queryset(self):
        product_type = self.request.query_params.get("product_type", "condom")
        queryset = ReviewCondom.objects.all()
        if product_type == "gel":
            queryset = ReviewGel.objects.all()

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


class UpdateCondomScore(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        # condom 점수, 리뷰 개수 초기화
        for condom in Condom.objects.all():
            condom.score = 0
            condom.avg_oily = 0
            condom.avg_durability = 0
            condom.avg_thickness = 0
            condom.num_of_reviews = 0
            condom.save()

        # condom 점수, 래뷰 개수 업데이트
        for review in ReviewCondom.objects.all():
            total = review.total
            oily = review.oily
            thickness = review.thickness
            durability = review.durability
            product = review.product
            condom = Condom.objects.filter(pk=product).update(
                score=F("score") + total,
                avg_oily=F("avg_oily") + oily,
                avg_thickness=F("avg_thickness") + thickness,
                avg_durability=F("avg_durability") + durability,
                num_of_reviews=F("num_of_reviews") + 1,
            )
        return Response(status=status.HTTP_200_OK)
