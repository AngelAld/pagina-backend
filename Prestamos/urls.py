from rest_framework.routers import DefaultRouter
from .views import (
    EntidadBancariaViewSet,
    EvaluacionSolicitudView,
    PerfilPrestatarioPrefabViewSet,
    PerfilPrestatarioPrefabDetalleViewSet,
    EtapaEvaluacionViewSet,
    PreguntaPerfilViewSet,
    NuevosClientesListModelViewSet,
    NuevosClientesDetalleModelViewSet,
    EvaluacionCrediticiaListViewSet,
)
from django.urls import path, include

router = DefaultRouter()

crud = DefaultRouter()

router.register(r"etapas-evaluacion", EtapaEvaluacionViewSet)
router.register(r"entidades-bancarias", EntidadBancariaViewSet)
router.register(r"prefabs", PerfilPrestatarioPrefabViewSet, basename="prefabs-lista")
router.register(r"preguntas", PreguntaPerfilViewSet)
router.register(r"nuevos-clientes", NuevosClientesListModelViewSet)
router.register(
    r"detalle-nuevos-clientes",
    NuevosClientesDetalleModelViewSet,
    basename="nuevos-clientes-detalle",
)
router.register(
    r"evaluaciones-crediticias",
    EvaluacionCrediticiaListViewSet,
    basename="evaluaciones-crediticias",
)

router.register(
    r"prefabs-detalle",
    PerfilPrestatarioPrefabDetalleViewSet,
    basename="prefabs-detalle",
)

crud.register(r"solicitud", EvaluacionSolicitudView, basename="solicitud")


urlpatterns = [
    path("creditos-hipotecarios/", include(router.urls)),
    path("evaluacion-credito/", include(crud.urls)),
]
