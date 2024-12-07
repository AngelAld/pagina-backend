from django_filters import FilterSet, RangeFilter

from Usuarios.models import Usuario
from .models import Inmueble
from django_filters.rest_framework import CharFilter
from django.db.models import Count, Q


class InmuebleFilterSet(FilterSet):
    precio_soles = RangeFilter()
    precio_dolares = RangeFilter()
    habitaciones = RangeFilter()
    baños = RangeFilter()
    pisos = RangeFilter()
    ascensores = RangeFilter()
    estacionamientos = RangeFilter()
    area_total = RangeFilter()
    area_construida = RangeFilter()
    mantenimiento = RangeFilter()
    caracteristicas = CharFilter(method="filter_caracteristicas")
    ubicacion__distrito = CharFilter(method="filter_distrito")
    ubicacion__distrito__provincia = CharFilter(method="filter_provincia")
    ubicacion__distrito__provincia__departamento = CharFilter(
        method="filter_departamento"
    )
    dueño = CharFilter(method="filter_dueño")

    class Meta:
        model = Inmueble
        fields = [
            "precio_soles",
            "precio_dolares",
            "habitaciones",
            "baños",
            "ascensores",
            "pisos",
            "estacionamientos",
            "area_total",
            "area_construida",
            "mantenimiento",
            "tipo_operacion",
            "tipo_antiguedad",
            "subtipo_inmueble",
            "tipo_inmueble",
            "caracteristicas",
            "ubicacion__distrito",
            "ubicacion__distrito__provincia",
            "ubicacion__distrito__provincia__departamento",
            "dueño",
        ]

    def filter_dueño(self, queryset, name, value):
        dueño = Usuario.objects.get(pk=value)
        if hasattr(dueño, "perfil_inmobiliaria"):
            queryset = queryset.filter(
                dueño__perfil_empleado__inmobiliaria=dueño.perfil_inmobiliaria
            ) | queryset.filter(dueño=dueño)
        else:
            queryset = queryset.filter(dueño=dueño)
        return queryset

    def filter_caracteristicas(self, queryset, name, value):
        pks = value.split(",")
        queryset = queryset.annotate(
            num_caracteristicas=Count(
                "caracteristicas",
                filter=Q(caracteristicas__pk__in=pks),
            )
        )
        filtered_queryset = queryset.filter(num_caracteristicas=len(pks)).distinct()
        return filtered_queryset

    def filter_distrito(self, queryset, name, value):
        nombres = value.split(",")
        queryset = queryset.filter(ubicacion__distrito__nombre__in=nombres)
        return queryset

    def filter_provincia(self, queryset, name, value):
        nombres = value.split(",")
        queryset = queryset.filter(ubicacion__distrito__provincia__nombre__in=nombres)
        return queryset

    def filter_departamento(self, queryset, name, value):
        nombres = value.split(",")
        queryset = queryset.filter(
            ubicacion__distrito__provincia__departamento__nombre__in=nombres
        )
        return queryset
