from rest_framework.routers import DefaultRouter
from .views import (
    EntidadBancariaViewSet,
    PerfilPrestatarioPrefabViewSet,
    PerfilPrestatarioPrefabDetalleViewSet,
    EtapaEvaluacionViewSet,
)
from django.urls import path, include

router = DefaultRouter()

router.register(r"etapas-evaluacion", EtapaEvaluacionViewSet)
router.register(r"entidades-bancarias", EntidadBancariaViewSet)
router.register(r"prefabs", PerfilPrestatarioPrefabViewSet, basename="prefabs-lista")

router.register(
    r"prefabs-detalle",
    PerfilPrestatarioPrefabDetalleViewSet,
    basename="prefabs-detalle",
)
urlpatterns = [
    path("creditos-hipotecarios/", include(router.urls)),
]
