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
            view.action in ["create", "update", "partial_update"]
            and obj.id == request.user.id
            or request.user.is_staff
        )


class ReviewCondomViewSet(viewsets.ModelViewSet):
    permission_classes = [AnonCreateAndUpdateOwnerOnly]

    def get_serializer_class(self):
        # 리스트, 조회
        if self.action == "list" or self.action == "retrieve":
            return ReviewCondomListSerializer
        # 생성, 수정, 삭제
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
        # 점수를 hash에 담아두기
        condom = {}
        for review in ReviewCondom.objects.all():
            review_score = [review.total, review.oily, review.thickness, review.durability, 1]
            product = review.product.id
            if product in condom:
                old_score = condom[product]
                new_score = []
                for c, t in zip(old_score[:-1], review_score[:-1]):
                    new = c + t
                    new_score.append(new)
                new_score.append(old_score[-1] + 1)
                condom[product] = new_score
            else:
                condom[product] = review_score

        # 점수 업데이트
        for c in Condom.objects.all():
            key = c.id
            num_of_reviews = condom[key][4]

            c.score = condom[key][0] / num_of_reviews
            c.avg_oily = condom[key][1] / num_of_reviews
            c.avg_thickness = condom[key][2] / num_of_reviews
            c.avg_durability = condom[key][3] / num_of_reviews
            c.num_of_reviews = num_of_reviews

            c.save()

        return Response(status=status.HTTP_200_OK, data=condom)
