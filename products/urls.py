from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import CondomListView, WelcomeCardListReadView


app_name = 'products'

urlpatterns = [
    path('welcome-cards/', WelcomeCardListReadView.as_view(), name='welcome-cards'),
    path('condom-list', CondomListView.as_view(), name="condom-list"),
]
