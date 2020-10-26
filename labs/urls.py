from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SutraListView, SutraDetailView, EvaluationView, SutraNewCardView

app_name = 'labs'

urlpatterns = [
    # 추후삭제 예정
    path('sutra/', SutraListView.as_view(), name='sutra'),
    path('sutra/evaluation/<int:sutra_id>/',
         EvaluationView.as_view(), name='sutra'),

    # url name의 문제로 수정
    path('sutras/', SutraListView.as_view(), name='sutra'),
    path('sutras/<int:pk>/', SutraDetailView.as_view(), name='sutra-detail'),
    path('sutras/<int:sutra_id>/evaluations/',
         EvaluationView.as_view(), name='evaluation'),
    path('sutra/new-card/', SutraNewCardView.as_view(), name='sutra')
]
