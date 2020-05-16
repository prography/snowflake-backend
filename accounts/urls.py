from django.urls import path, include
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'accounts'

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
