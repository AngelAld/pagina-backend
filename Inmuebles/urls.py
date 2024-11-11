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
)

router = DefaultRouter()

router.register(r"caracteristicas", CaracteristicaViewSet)
router.register(r"tipo_antiguedades", TipoAntiguedadViewSet)
router.register(r"tipo_inmuebles", TipoInmuebleViewSet)
router.register(r"sub_tipo_inmuebles", SubTipoInmuebleViewSet)
router.register(r"estado_inmuebles", EstadoInmuebleViewSet)
router.register(r"tipo_operaciones", TipoOperacionViewSet)
router.register(r"avisos", InmuebleListaViewSet)


urlpatterns = [
    path("inmuebles/", include(router.urls)),
]
