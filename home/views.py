from rest_framework import generics
from rest_framework.permissions import AllowAny

from home.serializers.welcome_card import WelcomeCardSerializer
from home.models import WelcomeCard


class WelcomeCardListReadView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = WelcomeCardSerializer
    queryset = WelcomeCard.objects.filter(status='PUB').order_by('row')
