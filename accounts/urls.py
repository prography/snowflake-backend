from django.urls import path, include, re_path
from .views import UserSocialViewSet, check_duplicates_email, check_duplicates_username, UserAPIView
from rest_framework.routers import DefaultRouter

app_name = 'accounts'

router = DefaultRouter()
router.register(r'', UserSocialViewSet)

urlpatterns = [
    re_path('check-duplicates/email/', check_duplicates_email),
    re_path('check-duplicates/username/', check_duplicates_username),
    path('', UserAPIView.as_view()),
    path('social/', include(router.urls))
]
