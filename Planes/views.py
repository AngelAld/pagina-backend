from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from .models import PlanInmuebles, PlanPrestamos, PlanServicios
from .serializers import (
    PlanInmueblesSerializer,
    PlanPrestamosSerializer,
    PlanServiciosSerializer,
)


class PlanInmueblesViewSet(GenericViewSet, ListModelMixin):
    queryset = PlanInmuebles.objects.all()
    serializer_class = PlanInmueblesSerializer
    http_method_names = ["get"]


class PlanPrestamosViewSet(GenericViewSet, ListModelMixin):
    queryset = PlanPrestamos.objects.all()
    serializer_class = PlanPrestamosSerializer
    http_method_names = ["get"]


class PlanServiciosViewSet(GenericViewSet, ListModelMixin):
    queryset = PlanServicios.objects.all()
    serializer_class = PlanServiciosSerializer
    http_method_names = ["get"]
