from rest_framework import serializers
from .models import Departamento, Provincia, Distrito


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = [
            "nombre",
        ]


class ProvinciaSerializer(serializers.ModelSerializer):
    departamento = serializers.StringRelatedField(
        read_only=True, source="departamento.nombre"
    )

    class Meta:
        model = Provincia
        fields = [
            "nombre",
            "departamento",
        ]


class DistritoSerializer(serializers.ModelSerializer):
    departamento = serializers.StringRelatedField(
        read_only=True, source="provincia.departamento.nombre"
    )
    provincia = serializers.StringRelatedField(
        read_only=True, source="provincia.nombre"
    )

    class Meta:
        model = Distrito
        fields = [
            "id",
            "nombre",
            "provincia",
            "departamento",
        ]
