from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from likes.models import Like
from products.models import Condom
from reviews.models import Review, ReviewCondom, ReviewGel
from reviews.serializers.condom import ReviewCondomListSerializer, ReviewCondomSerializer
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

        self._check_parameter_validation()

        _valid_param = {
            'filter': self.request.query_params.get("filter", None),
            'order': self.request.query_params.get("order", None)
        }

        if _valid_param['filter'] is not None:
            queryset = self._queryset_filter(queryset, _valid_param['filter'])
        if _valid_param['order'] is not None:
            queryset = self._queryset_order(queryset, _valid_param['order'])

        return queryset

    def _check_parameter_validation(self):
        if not self._is_valid_filter_param():
            raise ValidationError('Invalid partner parameter value')
        if not self._is_valid_order_param():
            raise ValidationError('Invalid order parameter value')


    def _is_valid_filter_param(self):
        _valid_partner_param = ["gender_MAN", "gender_WOMAN", 'partner_MAN', 'partner_WOMAN']
        filter = self.request.query_params.get("filter", None)

        if filter is None or filter in _valid_partner_param:
            return True
        return False

    def _is_valid_order_param(self):
        _valid_order_param = ['num_of_likes', 'total', '-total']
        order = self.request.query_params.get("order", None)

        if order is None or order in _valid_order_param:
            return True
        return False

    def _queryset_filter(self, queryset, _valid_param):
        _db_filed_name_per_target_filter = {
            'gender_MAN': ('gender', 'MAN'),
            'gender_WOMAN': ('gender', 'WOMAN'),
            'partner_MAN': ('partner_gender', 'MAN'),
            'partner_WOMAN': ('partner_gender', 'WOMAN')
        }

        key = _db_filed_name_per_target_filter[_valid_param][0]
        value = _db_filed_name_per_target_filter[_valid_param][1]

        if key == 'gender':
            queryset = queryset.filter(gender=value)
        elif key == 'partner':
            queryset = queryset.filter(partner_gender=value)
        return queryset

    def _queryset_order(self, queryset, _valid_param):
        return queryset.order_by(_valid_param)


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
