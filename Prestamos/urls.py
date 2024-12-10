from rest_framework.routers import DefaultRouter
from .views import EntidadBancariaViewSet, PerfilPrestatarioPrefabViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r"entidades-bancarias", EntidadBancariaViewSet)
router.register(r"prefabs", PerfilPrestatarioPrefabViewSet)

urlpatterns = [
    path("creditos-hipotecarios/", include(router.urls)),
]
