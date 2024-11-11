from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from .models import (
    Caracteristica,
    TipoAntiguedad,
    TipoInmueble,
    SubTipoInmueble,
    EstadoInmueble,
    TipoOperacion,
    Inmueble,
)
from .serializers import (
    CaracteristicaSerializer,
    TipoAntiguedadSerializer,
    TipoInmuebleSerializer,
    SubTipoInmuebleSerializer,
    EstadoInmuebleSerializer,
    TipoOperacionSerializer,
    InmuebleListSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin


class CaracteristicaViewSet(ModelViewSet):
    queryset = Caracteristica.objects.all()
    serializer_class = CaracteristicaSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ["nombre", "descripcion"]


class TipoAntiguedadViewSet(ModelViewSet):
    queryset = TipoAntiguedad.objects.all()
    serializer_class = TipoAntiguedadSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ["nombre", "descripcion"]


class TipoInmuebleViewSet(ModelViewSet):
    queryset = TipoInmueble.objects.all()
    serializer_class = TipoInmuebleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ["nombre", "descripcion"]


class SubTipoInmuebleViewSet(ModelViewSet):
    queryset = SubTipoInmueble.objects.all()
    serializer_class = SubTipoInmuebleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ["nombre", "descripcion", "tipo_Inmueble__nombre"]


class EstadoInmuebleViewSet(ModelViewSet):
    queryset = EstadoInmueble.objects.all()
    serializer_class = EstadoInmuebleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ["nombre", "descripcion"]


class TipoOperacionViewSet(ModelViewSet):
    queryset = TipoOperacion.objects.all()
    serializer_class = TipoOperacionSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ["nombre", "descripcion"]


class InmuebleListaViewSet(ListModelMixin, GenericViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleListSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ["get"]


# TODO: vistas para imagenes, planos y ubicaciones
