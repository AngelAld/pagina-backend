from rest_framework import serializers
from .models import Departamento, Provincia, Distrito


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = [
            "id",
            "nombre",
        ]


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = [
            "id",
            "nombre",
        ]


class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        fields = [
            "id",
            "nombre",
        ]
