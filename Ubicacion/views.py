from rest_framework.viewsets import GenericViewSet
from .models import Departamento, Provincia, Distrito
from .serializers import DepartamentoSerializer, ProvinciaSerializer, DistritoSerializer
from rest_framework.mixins import ListModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination


class DepartamentoViewSet(GenericViewSet, ListModelMixin):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    http_method_names = ["get"]
    filter_backends = [SearchFilter]
    search_fields = ["nombre"]
    pagination_class = LimitOffsetPagination


class ProvinciaViewSet(GenericViewSet, ListModelMixin):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
    http_method_names = ["get"]
    filter_backends = [SearchFilter]
    search_fields = ["nombre"]
    pagination_class = LimitOffsetPagination


class DistritoViewSet(GenericViewSet, ListModelMixin):
    queryset = Distrito.objects.all()
    serializer_class = DistritoSerializer
    http_method_names = ["get"]
    filter_backends = [SearchFilter]
    search_fields = ["nombre"]
    pagination_class = LimitOffsetPagination
