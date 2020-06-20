from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

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
            if order in ["num_of_reviews", "avg_oily", "avg_thickness", "avg_durability"]:
                queryset = queryset.order_by(order)
                queryset = queryset.reverse()
            else:
                raise NotFound()
        return queryset


class CondomDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CondomDetailSerializer
    queryset = Condom.objects.all()



