from rest_framework import generics
from rest_framework.permissions import AllowAny

from home.serializers.welcome_card import WelcomeCardSerializer
from home.models import WelcomeCard


class WelcomeCardListReadView(generics.ListAPIView):
    """
    사용자 처음 어플리케이션 진입 화면에서, 카드 형태의 컨텐츠를 반환하는 API.
        row: 최상단부터 몇번째 row 인지 의미
        col: 좌측부터 몇번째 col 인지 의미(row 가 같은 경우, 같은 row 에 위치하며 슬라이더 형태로 카드가 나열되는 것을 의미)
    """
    permission_classes = [AllowAny]
    serializer_class = WelcomeCardSerializer
    queryset = WelcomeCard.objects.filter(status='PUB', col__gte='0').order_by('col', 'category')
