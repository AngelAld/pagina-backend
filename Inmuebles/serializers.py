from rest_framework import serializers

from Ubicacion.serializers import DistritoSerializer
from Usuarios.models import Usuario
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
            "indice",
            "imagen",
            "titulo",
            "is_portada",
        ]


class PlanoInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoInmueble
        fields = [
            "plano",
            "titulo",
        ]


class UbicacionInmuebleSerializer(serializers.ModelSerializer):
    distrito = DistritoSerializer()

    class Meta:
        model = UbicacionInmueble
        fields = [
            "distrito",
            "calle",
            "numero",
            "latitud",
            "longitud",
        ]


class DueñoSerializer(serializers.ModelSerializer):

    nombre = serializers.SerializerMethodField()
    telefono = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ["nombre", "email", "telefono"]

    def get_nombre(self, obj):
        if hasattr(obj, "perfil_particular"):
            return obj.perfil_particular.usuario.nombre_completo
        elif hasattr(obj, "perfil_empleado"):
            return obj.perfil_empleado.inmobiliaria.razon_social
        elif hasattr(obj, "perfil_inmobiliaria"):
            return obj.perfil_inmobiliaria.razon_social
        else:
            return None

    def get_telefono(self, obj):
        if hasattr(obj, "perfil_particular"):
            return obj.perfil_particular.telefono
        elif hasattr(obj, "perfil_empleado"):
            return obj.perfil_empleado.inmobiliaria.telefono
        elif hasattr(obj, "perfil_inmobiliaria"):
            return obj.perfil_inmobiliaria.telefono
        else:
            return None


class InmuebleDetalleSerializer(serializers.ModelSerializer):
    dueño = DueñoSerializer()
    tipo_operacion = serializers.StringRelatedField()
    estado = serializers.StringRelatedField()
    tipo_antiguedad = serializers.StringRelatedField()
    subtipo_inmueble = serializers.StringRelatedField()
    ubicacion = UbicacionInmuebleSerializer()
    caracteristicas = serializers.StringRelatedField(many=True)
    imagenes = ImagenInmuebleSerializer(many=True)
    planos = PlanoInmuebleSerializer(many=True)

    class Meta:
        model = Inmueble
        fields = [
            "dueño",
            "titulo",
            "slug",
            "descripcion",
            "tipo_operacion",
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
            "portada",
            "num_favoritos",
            "num_visitas",
            "ubicacion",
            "caracteristicas",
            "imagenes",
            "planos",
        ]


class ContactoDueñoSerializer(serializers.Serializer):
    telefono = serializers.CharField(
        write_only=True,
    )
    mensaje = serializers.CharField(
        write_only=True,
    )
    email = serializers.EmailField(
        write_only=True,
    )
    nombre = serializers.CharField(
        write_only=True,
    )
    slug = serializers.CharField(
        write_only=True,
    )
    message = serializers.CharField(
        read_only=True,
    )
