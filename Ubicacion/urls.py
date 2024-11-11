from rest_framework.routers import DefaultRouter
from .views import DepartamentoViewSet, ProvinciaViewSet, DistritoViewSet
from django.urls import path, include

router = DefaultRouter()

router.register("departamentos", DepartamentoViewSet, basename="departamentos")
router.register("provincias", ProvinciaViewSet, basename="provincias")
router.register("distritos", DistritoViewSet, basename="distritos")

urlpatterns = [
    path("ubicacion/", include(router.urls)),
]
