from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from products.serializers.condom import CondomListSerializer, CondomTopNSerailzier
from products.serializers.welcome_card import ProductWelcomeCardSerializer
from products.models import WelcomeCard, Condom


class WelcomeCardListReadView(generics.ListAPIView):
    """
    상품 처음 화면에서, 카드 형태의 컨텐츠를 반환하는 API.
    """

    permission_classes = [AllowAny]
    serializer_class = ProductWelcomeCardSerializer
    queryset = WelcomeCard.objects.filter(status='PUB').order_by('col', 'category')


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

    def get_queryset(self):
        order = self.request.query_params.get("order", None)
        category = self.request.query_params.get("category", None)

        queryset = Condom.objects.all()

        if category is not None:
            if category == "NORMAL":
                queryset = queryset.filter(category="NORMAL")
            elif category == "SLIM":
                queryset = queryset.filter(category="SLIM")
            elif category == "CHOBAK":
                queryset = queryset.filter(category="CHOBAK")
            elif category == "DOLCHUL":
                queryset = queryset.filter(category="DOLCHUL")
            elif category == "GGOKJI":
                queryset = queryset.filter(category="GGOKJI")
            elif category == "DELAY":
                queryset = queryset.filter(category="DELAY")
            else:
                raise NotFound()

        if order is None:
            queryset = queryset.order_by("-score")
        else:
            if order == "review":
                queryset = queryset.order_by("-num_of_reviews")
            elif order == "oily":
                queryset = queryset.order_by("-avg_oily")
            elif order == "thickness":
                queryset = queryset.order_by("-avg_thickness")
            elif order == "durability":
                queryset = queryset.order_by("-avg_durability")
            else:
                raise NotFound()
        return queryset
