from rest_framework.routers import DefaultRouter
from .views import EntidadBancariaViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r"entidades-bancarias", EntidadBancariaViewSet)

urlpatterns = [
    path("prestamos/", include(router.urls)),
]
