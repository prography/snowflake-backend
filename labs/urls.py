from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EvaluationView, SutraListView, SutraNewCardView

app_name = 'labs'

urlpatterns = [
    path('sutra/', SutraListView.as_view(), name='sutra'),
    path('sutra/evaluation/<int:sutra_id>/',
         EvaluationView.as_view(), name='sutra'),
    path('sutra/new-card/', SutraNewCardView.as_view(), name='sutra')
]
