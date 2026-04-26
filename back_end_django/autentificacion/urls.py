# Archivo: autentificacion/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Ruta para obtener un token de acceso y un token de renovación.
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Ruta para refrescar el token de acceso usando un token de renovación válido.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Archivo: back_end_django/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API de Telefonía",
        default_version='v1',
        description="Documentación de la API de Telefonía",
        terms_of_service="https://www.tusitio.com/terms/",
        contact=openapi.Contact(email="soporte@tusitio.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('gestion_usuarios.urls')),
    path('api/productos/', include('gestion_productos.urls')),

    # Registro de las rutas de autenticación JWT definidas en la aplicación 'autentificacion'
    path('api/auth/', include('autentificacion.urls')),

    # FIX (fatal): el nombre del grupo no puede llevar espacio: (?P<format >...) rompe el regex.
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),

    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),

    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]