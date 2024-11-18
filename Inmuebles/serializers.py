from rest_framework import serializers
from .models import (
    Caracteristica,
    TipoAntiguedad,
    TipoInmueble,
    SubTipoInmueble,
    EstadoInmueble,
    TipoOperacion,
    Inmueble,
    ImagenInmueble,
    PlanoInmueble,
    UbicacionInmueble,
)


class CaracteristicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristica
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class TipoAntiguedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAntiguedad
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class TipoInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInmueble
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class SubTipoInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTipoInmueble
        fields = [
            "id",
            "nombre",
            "descripcion",
            "tipo_inmueble",
        ]


class EstadoInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoInmueble
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class TipoOperacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoOperacion
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class InmuebleSerializer(serializers.ModelSerializer):
    caracteristicas = CaracteristicaSerializer(many=True)

    class Meta:
        model = Inmueble
        fields = [
            "id",
            "dueño",
            "titulo",
            "slug",
            "descripcion",
            "tipo_operacion",
            "fecha_creacion",
            "fecha_actualizacion",
            "estado",
            "habitaciones",
            "baños",
            "pisos",
            "ascensores",
            "estacionamientos",
            "area_construida",
            "area_total",
            "precio_soles",
            "precio_dolares",
            "mantenimiento",
            "tipo_antiguedad",
            "años",
            "tipo_inmueble",
            "subtipo_inmueble",
            "caracteristicas",
            "portada",
            "num_favoritos",
            "num_visitas",
        ]
        read_only_fields = [
            "portada",
            "dueño",
            "slug",
            "fecha_creacion",
            "fecha_actualizacion",
            "num_favoritos",
            "num_visitas",
            "estado",
        ]


class InmuebleListSerializer(serializers.ModelSerializer):
    tipo_operacion = serializers.StringRelatedField()
    estado = serializers.StringRelatedField()
    tipo_antiguedad = serializers.StringRelatedField()
    subtipo_inmueble = serializers.StringRelatedField()
    portada = serializers.StringRelatedField(allow_null=True)
    ubicacion = serializers.StringRelatedField(
        source="ubicacion.distrito", allow_null=True
    )

    class Meta:
        model = Inmueble
        fields = [
            "titulo",
            "slug",
            "tipo_operacion",
            "fecha_actualizacion",
            "estado",
            "habitaciones",
            "area_total",
            "precio_soles",
            "precio_dolares",
            "tipo_antiguedad",
            "años",
            "subtipo_inmueble",
            "portada",
            "num_favoritos",
            "num_visitas",
            "ubicacion",
        ]


class ImagenInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenInmueble
        fields = [
            "id",
            "indice",
            "inmueble",
            "imagen",
            "titulo",
            "is_portada",
        ]


class PlanoInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoInmueble
        fields = [
            "id",
            "inmueble",
            "imagen",
            "titulo",
        ]


class UbicacionInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbicacionInmueble
        fields = [
            "id",
            "inmueble",
            "distrito",
            "calle",
            "numero",
            "latitud",
            "longitud",
        ]
