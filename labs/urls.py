from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SutraListView, EvaluationView, SutraCommentViewSet, SutraCommentLikeViewSet

app_name = 'labs'

comment_router = DefaultRouter()
comment_router.register(r'comments', SutraCommentViewSet, basename='sutracomment')

comment_like_router = DefaultRouter()
comment_like_router.register(r'likes', SutraCommentLikeViewSet, basename='like')

urlpatterns = [
    path("sutras/<int:sutra_id>/", include(comment_router.urls)),
    path("sutras/<int:sutra_id>/comments/<int:comment_id>/", include(comment_like_router.urls)),
    path('sutra/', SutraListView.as_view(), name='sutra'),
    path('sutra/evaluation/<int:sutra_id>/',
         EvaluationView.as_view(), name='sutra'),
]
