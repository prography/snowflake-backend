from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import (
    CondomListView,
    WelcomeCardListReadView,
    CondomTopNListView,
    CondomTrioView,
    CondomDetailView,
)


app_name = "products"

urlpatterns = [
    path("welcome-cards/", WelcomeCardListReadView.as_view(), name="welcome-cards"),
    path("condom/list/", CondomListView.as_view(), name="condom-list"),
    path("condom/top-n/", CondomTopNListView.as_view(), name="condom-top-n"),
    path("condom/trio/", CondomTrioView.as_view(), name="condom-trio"),
    path("condom/<int:pk>/", CondomDetailView.as_view(), name="condom-detail"),
]
