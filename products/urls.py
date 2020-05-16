from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import CondomListView


app_name = 'products'

urlpatterns = [
    path('condom-list', CondomListView.as_view(), name="condom-list"),
]
