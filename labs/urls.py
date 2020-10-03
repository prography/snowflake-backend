from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SutraListView

app_name = 'labs'

urlpatterns = [
    path('sutra/', SutraListView.as_view(), name='sutra')
]
