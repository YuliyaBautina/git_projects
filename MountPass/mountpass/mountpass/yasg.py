from django.urls import path
from rest_framework import permissions
from drf_yasg import views, openapi


schema_view = views.get_schema_view(
    openapi.Info(
        title='MountPass',
        default_version='v1',
        description='Educational project, API for uploading information into given system',
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema_redoc'),
]