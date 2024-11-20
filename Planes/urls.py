from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanInmueblesViewSet, PlanPrestamosViewSet, PlanServiciosViewSet

router = DefaultRouter()

router.register(r"inmuebles", PlanInmueblesViewSet)
router.register(r"prestamos", PlanPrestamosViewSet)
router.register(r"servicios", PlanServiciosViewSet)

urlpatterns = [
    path("planes/", include(router.urls)),
]
