from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.views import WelcomeCardListReadView

app_name = 'home'

urlpatterns = [
    path('welcome-cards/', WelcomeCardListReadView.as_view())
]
