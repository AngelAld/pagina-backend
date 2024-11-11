from django_filters import FilterSet, RangeFilter
from .models import Departamento, Provincia, Distrito


class DepartamentoFilter(FilterSet):
    class Meta:
        model = Departamento
        fields = {
            "nombre": ["exact", "icontains"],
        }
