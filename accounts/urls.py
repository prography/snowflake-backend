from django.urls import path, include, re_path
from .views import UserViewSet, check_duplicates_email, check_duplicates_username, UserGetUpdateView
from rest_framework.routers import DefaultRouter

app_name = 'accounts'

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    re_path('check-duplicates/email/', check_duplicates_email),
    re_path('check-duplicates/username/', check_duplicates_username),
    path('info/', UserGetUpdateView.as_view()),
    path('', include(router.urls))
]
