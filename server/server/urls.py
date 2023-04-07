"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from server.views import CustomOpenAPISchemaGenerator

router = routers.DefaultRouter()

router.get_api_root_view().cls.__name__ = "Whoosh API"
router.get_api_root_view().cls.__doc__ = "Доступные API методы сервиса"

urlpatterns = []

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Доступные API методы сервиса",
    ),
    public=True,
    generator_class=CustomOpenAPISchemaGenerator,
)

urlpatterns += [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('api/', include(router.urls)),
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
