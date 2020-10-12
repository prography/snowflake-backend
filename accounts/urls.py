from django.urls import path, include, re_path
from .views import UserSocialViewSet, check_duplicates_email, check_duplicates_username, UserAPIView
from rest_framework.routers import DefaultRouter

app_name = 'accounts'

# accounts/social/kakao-login-callback로만 요청해야함.
# accounts/social/kakao-login-callback/ 로 요청하면 에러 발생함.
router = DefaultRouter(trailing_slash=False)
router.register(r'', UserSocialViewSet)

urlpatterns = [
    re_path('check-duplicates/email/', check_duplicates_email),
    re_path('check-duplicates/username/', check_duplicates_username),
    path('', UserAPIView.as_view()),
    path('social/', include(router.urls))
]
