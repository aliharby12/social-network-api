"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
]

if settings.DEBUG:  # pragma: no cover

    schema_view = get_schema_view(
        openapi.Info(
            title="Social API",
            default_version="1.2",
            description="Social API",
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    urlpatterns = (
        [
            # Swagger
            path(
                "swagger",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            ),
            path(
                "redoc/",
                schema_view.with_ui("redoc", cache_timeout=0),
                name="schema-redoc",
            ),
        ]
        + urlpatterns
        + static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
    )