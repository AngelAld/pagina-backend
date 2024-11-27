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
    InmueblePreViewSet,
    ContactoDueñoView,
    CRUDListaViewSet,
    PublicarInmuebleView,
    CrudInmuebleViewSet,
    FavoritoViewSet,
    VisitaViewSet,
    MisFavoritosViewSet,
    InmuebleMapaViewSet,
)

router = DefaultRouter()

router.register(r"caracteristicas", CaracteristicaViewSet)
router.register(r"tipo-antiguedades", TipoAntiguedadViewSet)
router.register(r"tipo-inmuebles", TipoInmuebleViewSet)
router.register(r"sub-tipo-inmuebles", SubTipoInmuebleViewSet)
router.register(r"estado-inmuebles", EstadoInmuebleViewSet)
router.register(r"tipo-operaciones", TipoOperacionViewSet)
router.register(r"avisos", InmuebleListaViewSet)
router.register(r"mapa", InmuebleMapaViewSet, basename="mapa")
router.register(r"aviso-detalle", InmuebleDetalleViewSet, basename="aviso-detalle")
router.register(r"crud-lista", CRUDListaViewSet, basename="crud-lista")
router.register(r"previsualizar", InmueblePreViewSet, basename="previsualizacion")
router.register(r"publicar", PublicarInmuebleView, basename="publicar")
router.register(r"crud", CrudInmuebleViewSet, basename="crud")
router.register(r"favoritos", FavoritoViewSet, basename="favoritos")
router.register(r"mis-favoritos", MisFavoritosViewSet, basename="mis-favoritos")
router.register(r"visitas", VisitaViewSet, basename="visitas")
urlpatterns = [
    path("inmuebles/", include(router.urls)),
    path("inmuebles/contactar/", ContactoDueñoView.as_view()),
]
