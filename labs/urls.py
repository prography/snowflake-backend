from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SutraListView, SutraDetailView, EvaluationView, SutraNewCardView, SutraCommentViewSet

app_name = 'labs'

comment_router = DefaultRouter()
comment_router.register(r'', SutraCommentViewSet,
                        basename='sutracomment')

urlpatterns = [
    path('sutras/', SutraListView.as_view(), name='sutra'),
    path('sutras/<int:pk>/', SutraDetailView.as_view(), name='sutra-detail'),
    path("sutras/<int:sutra_id>/comments/", include(comment_router.urls)),
    path('sutras/<int:sutra_id>/evaluations/',
         EvaluationView.as_view(), name='evaluation'),
    path('sutras/new-card/', SutraNewCardView.as_view(), name='sutra')
]
