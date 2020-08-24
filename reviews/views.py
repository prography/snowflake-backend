from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from reviews.serializers.condom import ReviewCondomSerializer, ReviewCondomListSerializer

from reviews.models import ReviewCondom, ReviewGel, Review
from products.models import Condom
from likes.models import Like

from django.db.models import F, Avg

from snowflake.exception import MissingProductIdException


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

        product = self.request.query_params.get("product")
        if product is None:
            raise MissingProductIdException()
        queryset = queryset.filter(product=product).order_by("-id")

        score = self.request.query_params.get("score", None)
        gender = self.request.query_params.get("gender", None)
        partner = self.request.query_params.get("partner", None)
        order = self.request.query_params.get("order", None)

        if score is not None:
            if score in ["-total", "total"]:
                queryset = queryset.order_by(score)
            else:
                raise NotFound()

        if gender is not None:
            if gender in ["MAN", "WOMAN"]:
                queryset = queryset.filter(gender=gender)
            else:
                raise NotFound()

        if partner is not None:
            if partner in ["MAN", "WOMAN"]:
                queryset = queryset.filter(partner_gender=partner)
            else:
                raise NotFound()

        if order is not None:
            if order in ['num_of_likes']:
                queryset = queryset.order_by('num_of_likes').reverse()
            else:
                raise NotFound()
        return queryset


class UpdateCondomScore(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        condoms = Condom.objects.all()
        for condom in condoms:
            # ReviewCondom filtering
            queryset = ReviewCondom.objects.filter(product__id=condom.id)
            # num_of_reviews update
            queryset_cnt = queryset.count()
            condom.num_of_reviews = queryset_cnt
            # average score update
            aggs_result = queryset.aggregate(Avg('oily'), Avg('thickness'), Avg('durability'), Avg('total'))
            condom.avg_durability = aggs_result['durability__avg'] if aggs_result['durability__avg'] is not None else 0
            condom.avg_oily = aggs_result['oily__avg'] if aggs_result['oily__avg'] is not None else 0
            condom.avg_thickness = aggs_result['thickness__avg'] if aggs_result['thickness__avg'] is not None else 0
            condom.score = aggs_result['total__avg'] if aggs_result['total__avg'] is not None else 0
            condom.save()

        return Response("Complete", status=status.HTTP_200_OK)


class NumOfLikesUpdateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        for review in Review.objects.all():
            content_type = ContentType.objects.get(model='review')
            num_of_likes = Like.objects.filter(content_type=content_type.id, object_id=review.id).count()
            review.num_of_likes = num_of_likes
            review.save()
        return Response({"message": "Complete"}, status=status.HTTP_200_OK)
