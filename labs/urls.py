from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import SutraListView, EvaluationView, SutraCommentViewSet

app_name = 'labs'

comment_router = DefaultRouter()
comment_router.register(r'comments', SutraCommentViewSet, basename='sutracomment')

urlpatterns = [
    path("sutras/<int:sutra_id>/", include(comment_router.urls)),
    path('sutra/', SutraListView.as_view(), name='sutra'),
    path('sutra/evaluation/<int:sutra_id>/',
         EvaluationView.as_view(), name='sutra'),
]
