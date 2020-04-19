from django.urls import path, include
from .views import CustomUserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'accounts'

router = DefaultRouter()
router.register(r'', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
