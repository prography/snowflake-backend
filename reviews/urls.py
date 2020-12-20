from django.urls import path, include
from reviews.views import ReviewViewset, UpdateCondomScore, NumOfLikesUpdateView

from rest_framework.routers import DefaultRouter

app_name = "reviews"

router = DefaultRouter()
router.register(r"", ReviewViewset, basename="review")

urlpatterns = [
    path("", include(router.urls)),
    path("update-condom-score", UpdateCondomScore.as_view()),
    path("update-likes-count", NumOfLikesUpdateView.as_view()),
]
