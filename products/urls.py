from django.urls import path

from products.views import (CondomDetailView, CondomListView, CondomTopNListView, CondomTrioView, NumOfLikesUpdateView, SearchView, WelcomeCardListReadView)

app_name = "products"

urlpatterns = [
    path("welcome-cards/", WelcomeCardListReadView.as_view(), name="welcome-cards"),
    path("condom/", CondomListView.as_view(), name="condom-list"),
    path("condom/top-n/", CondomTopNListView.as_view(), name="condom-top-n"),
    path("condom/trio/", CondomTrioView.as_view(), name="condom-trio"),
    path("condom/<int:pk>/", CondomDetailView.as_view(), name="condom-detail"),

    # 검색
    path("search/", SearchView.as_view(), name="search"),

    path("update-likes-count", NumOfLikesUpdateView.as_view()),
]
