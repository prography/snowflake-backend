from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reports.views import ReportViewSet

app_name = 'reports'

router = DefaultRouter()
router.register(r"", ReportViewSet, basename="report")

urlpatterns = [
    path("", include(router.urls)),
]
