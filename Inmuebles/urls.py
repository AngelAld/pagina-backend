from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CaracteristicaViewSet,
    TipoAntiguedadViewSet,
    TipoInmuebleViewSet,
    SubTipoInmuebleViewSet,
    EstadoInmuebleViewSet,
    TipoOperacionViewSet,
    InmuebleListaViewSet,
    InmuebleDetalleViewSet,
)

router = DefaultRouter()

router.register(r"caracteristicas", CaracteristicaViewSet)
router.register(r"tipo-antiguedades", TipoAntiguedadViewSet)
router.register(r"tipo-inmuebles", TipoInmuebleViewSet)
router.register(r"sub-tipo-inmuebles", SubTipoInmuebleViewSet)
router.register(r"estado-inmuebles", EstadoInmuebleViewSet)
router.register(r"tipo-operaciones", TipoOperacionViewSet)
router.register(r"avisos", InmuebleListaViewSet)
router.register(r"aviso-detalle", InmuebleDetalleViewSet, basename="aviso-detalle")


urlpatterns = [
    path("inmuebles/", include(router.urls)),
]
