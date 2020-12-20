from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from likes.models import Like
from products.models import Condom
from reviews.models import Review, ReviewCondom, ReviewGel
from reviews.serializers.condom import ReviewCondomListSerializer, ReviewCondomSerializer
from snowflake.exception import MissingProductIdException
from snowflake.permission import AnonCreateAndUpdateOwnerOnly


class ReviewViewset(viewsets.ModelViewSet):
    """
    제품의 리뷰

    여러 제품의 리뷰
    """

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

        self._check_parameter_validation()

        _valid_param = {
            'gender': self.request.query_params.get("gender", None),
            'partner': self.request.query_params.get("partner", None),
            'order': self.request.query_params.get("order", None)
        }

        queryset = self._queryset_filter(queryset, _valid_param)
        return queryset

    def _check_parameter_validation(self):
        if self._is_valid_filter_param() is False or self._is_valid_order_param() is False:
            raise ValidationError('Invalid partner parameter value')

    def _is_valid_filter_param(self):
        _valid_partner_param = ["MAN", "WOMAN"]
        gender = self.request.query_params.get("gender")
        partner = self.request.query_params.get("partner")

        if (gender is None or gender in _valid_partner_param) and (partner is None or partner in _valid_partner_param):
            return True
        return False

    def _is_valid_order_param(self):
        _valid_order_param = ['likes_count', "-likes_count", 'total', '-total']
        order = self.request.query_params.get("order", None)

        if order is None or order in _valid_order_param:
            return True
        return False

    def _queryset_filter(self, queryset, _valid_param):
        if _valid_param.get('gender') is not None:
            queryset = queryset.filter(gender=_valid_param.get('gender'))
        if _valid_param.get('partner') is not None:
            queryset = queryset.filter(partner_gender=_valid_param.get('partner'))
        if _valid_param.get('order') is not None:
            queryset = queryset.order_by(f'-{_valid_param.get("order")}')
        return queryset

    product_type_param = openapi.Parameter(
        'product_type', openapi.IN_QUERY, description="condom | gel - 제품의 타입", type=openapi.TYPE_STRING)
    product_param = openapi.Parameter(
        'product', openapi.IN_QUERY, description="제품의 id", type=openapi.TYPE_INTEGER)
    order_param = openapi.Parameter(
        'order', openapi.IN_QUERY, description="likes_count | -likes_count | total | -total", type=openapi.TYPE_STRING)
    gender_param = openapi.Parameter(
        'gender', openapi.IN_QUERY, description="MAN | WOMAN", type=openapi.TYPE_STRING)
    partner_param = openapi.Parameter(
        'partner', openapi.IN_QUERY, description="MAN | WOMAN", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[product_type_param, product_param, order_param, gender_param, partner_param])
    def list(self, request, *args, **kwargs):
        response = super(ReviewViewset, self).list(self, request, *args, **kwargs)
        return response


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
            review.likes_count = num_of_likes
            review.save()
        return Response({"message": "Complete"}, status=status.HTTP_200_OK)
