from django.urls import path, include
from rest_framework.routers import DefaultRouter

from likes.views import LikeViewSet

app_name = 'likes'

router = DefaultRouter()
router.register(r"", LikeViewSet, basename="like")
urlpatterns = [
    path("", include(router.urls)),
]
