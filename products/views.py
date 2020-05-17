from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from products.serializers.condom import CondomListSerializer
from products.models import Condom


class CondomListView(generics.ListAPIView):
    """
    콘돔의 랭킹을 보여주는 API.
    """

    permission_classes = [AllowAny]
    serializer_class = CondomListSerializer

    def get_queryset(self):
        order = self.request.query_params.get("order", None)
        category = self.request.query_params.get("category", None)

        queryset = Condom.objects.all()

        if category is not None:
            if category == "1":
                queryset = queryset.filter(category=1)
            elif category == "2":
                queryset = queryset.filter(category=2)
            elif category == "3":
                queryset = queryset.filter(category=3)
            elif category == "4":
                queryset = queryset.filter(category=4)
            elif category == "5":
                queryset = queryset.filter(category=5)
            elif category == "6":
                queryset = queryset.filter(category=6)
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
