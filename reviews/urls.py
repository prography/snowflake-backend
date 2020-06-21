from django.urls import path, include
from reviews.views import ReviewCondomViewSet, UpdateCondomScore

from rest_framework.routers import DefaultRouter

app_name = "reviews"

router = DefaultRouter()
router.register(r"", ReviewCondomViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),
]
