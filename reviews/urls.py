from django.urls import path, include
from reviews.views import ReviewCondomViewSet, ReviewProductListView

from rest_framework.routers import DefaultRouter

app_name = "reviews"

router = DefaultRouter()
router.register(r"", ReviewCondomViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),
    path('product/<int:product>', ReviewProductListView.as_view(), name="product-reivews"),
]
