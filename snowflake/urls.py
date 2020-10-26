"""snowflake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Swagger part
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # swagger
    url(r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0), name="schema-json"),
    url(r"^swagger/$", schema_view.with_ui("swagger",
                                           cache_timeout=0), name="schema-swagger-ui"),
    url(r"^redoc/$", schema_view.with_ui("redoc",
                                         cache_timeout=0), name="schema-redoc"),
    # admin
    path("admin/", admin.site.urls),
    # JWT v2: simple jwt token
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # app
    path("accounts/", include("accounts.urls")),
    path("home/", include("home.urls")),
    path("products/", include("products.urls")),
    path("reviews/", include("reviews.urls")),
    path("likes/", include("likes.urls")),
    path("labs/", include("labs.urls")),
    path("reports/", include('reports.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.index_title = "눈송이 v1.1.2"

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
