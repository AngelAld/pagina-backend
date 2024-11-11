from django_filters import FilterSet
from .models import Provincia, Distrito
from django_filters import rest_framework as filters


class ProvinciaFilter(FilterSet):
    departamento = filters.CharFilter(method="filter_departamento")

    class Meta:
        model = Provincia
        fields = ["departamento"]

    def filter_departamento(self, queryset, name, value):
        nombres = value.split(",")
        queryset = queryset.filter(departamento__nombre__in=nombres)
        return queryset


class DistritoFilter(FilterSet):
    nombre = filters.CharFilter(lookup_expr="icontains")
    provincia = filters.CharFilter(method="filter_provincia")

    class Meta:
        model = Distrito
        fields = ["nombre", "provincia"]

    def filter_provincia(self, queryset, name, value):
        nombres = value.split(",")
        queryset = queryset.filter(provincia__nombre__in=nombres)
        return queryset
