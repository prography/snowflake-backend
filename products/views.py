from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from likes.models import Like
from products.serializers.condom import CondomListSerializer, CondomTopNSerailzier, CondomDetailSerializer
from products.serializers.welcome_card import ProductWelcomeCardSerializer
from products.models import WelcomeCard, Condom


class WelcomeCardListReadView(generics.ListAPIView):
    """
    상품 처음 화면에서, 카드 형태의 컨텐츠를 반환하는 API.
    """

    permission_classes = [AllowAny]
    serializer_class = ProductWelcomeCardSerializer
    queryset = WelcomeCard.objects.filter(status="PUB").order_by("col", "category")


class CondomTopNListView(generics.ListAPIView):
    """
    상품 처음 화면에서, 카드 형태의 컨텐츠를 반환하는 API.
    """

    permission_classes = [AllowAny]
    serializer_class = CondomTopNSerailzier
    queryset = Condom.objects.order_by("-score")[:5]


class CondomTrioView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        avg_thickness = Condom.objects.order_by("-avg_thickness")[:1]
        avg_durability = Condom.objects.order_by("-avg_durability")[:1]
        avg_oily = Condom.objects.order_by("-avg_oily")[:1]

        thickness_serializer = CondomTopNSerailzier(avg_thickness, many=True)
        durability_serializer = CondomTopNSerailzier(avg_durability, many=True)
        oily_serializer = CondomTopNSerailzier(avg_oily, many=True)

        data = {
            "thickness": thickness_serializer.data,
            "durability": durability_serializer.data,
            "oily": oily_serializer.data,
        }
        return Response(data)


class CondomListView(generics.ListAPIView):
    """
    콘돔의 전체 랭킹을 보여주는 API.
    """

    permission_classes = [AllowAny]
    serializer_class = CondomListSerializer
    condom_category = [c[0] for c in Condom.CATEGORY_CHOICES]

    def get_queryset(self):
        order = self.request.query_params.get("order", None)
        category = self.request.query_params.get("category", None)

        queryset = Condom.objects.all()
        if category is not None:
            if category in self.condom_category:
                queryset = queryset.filter(category=category)
            else:
                raise NotFound()

        if order is None:
            queryset = queryset.order_by("-score")
        else:
            if order in ["num_of_reviews", "avg_oily", "avg_thickness", "avg_durability", "num_of_views", 'num_of_likes']:
                queryset = queryset.order_by(f'-{order}')
            else:
                raise NotFound()
        return queryset


class CondomDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CondomDetailSerializer
    queryset = Condom.objects.all()

    def get_object(self):
        obj = super().get_object()
        obj.num_of_views += 1
        obj.save()
        return obj


class SearchView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CondomListSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get("keyword", None)
        queryset = Condom.objects.filter(search_field__icontains=keyword)
        return queryset


class NumOfLikesUpdateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        for condom in Condom.objects.all():
            content_type = ContentType.objects.get(model='review')
            num_of_likes = Like.objects.filter(content_type=content_type.id, object_id=condom.id).count()
            condom.num_of_likes = num_of_likes
            condom.save()
        return Response({"message": "Complete"}, status=status.HTTP_200_OK)
