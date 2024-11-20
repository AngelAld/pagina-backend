from .models import PlanInmuebles, PlanPrestamos, PlanServicios
from rest_framework import serializers


class PlanInmueblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanInmuebles
        fields = "__all__"


class PlanPrestamosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPrestamos
        fields = "__all__"


class PlanServiciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanServicios
        fields = "__all__"
