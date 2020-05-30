from django.urls import path, include
from reviews.views import ReviewViewSet

from rest_framework.routers import DefaultRouter

app_name = 'reviews'

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]