"""
URL configuration for Api project.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", include("Usuarios.urls")),
    path("", include("Prestamos.urls")),
    path("", include("Ubicacion.urls")),
    path("", include("Inmuebles.urls")),
]
