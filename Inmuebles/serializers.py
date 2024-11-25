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
from drf_extra_fields.fields import Base64ImageField
from django.db.transaction import atomic


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


class InmueblePreviewSerializer(serializers.ModelSerializer):
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
            "id",
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


class CRUDListaSerializer(serializers.ModelSerializer):
    portada = serializers.StringRelatedField()
    tipo_inmueble = serializers.StringRelatedField(
        source="tipo_inmueble.nombre",
    )
    calle = serializers.StringRelatedField(
        source="ubicacion.calle",
    )
    distrito = serializers.StringRelatedField(
        source="ubicacion.distrito.nombre",
    )
    num_visitas = serializers.StringRelatedField()
    num_favoritos = serializers.StringRelatedField()
    estado = serializers.StringRelatedField(
        source="estado.nombre",
    )

    class Meta:
        model = Inmueble
        fields = [
            "id",
            "slug",
            "portada",
            "tipo_inmueble",
            "precio_soles",
            "precio_dolares",
            "calle",
            "distrito",
            "num_visitas",
            "num_favoritos",
            "estado",
        ]


class PublicarInmuebleSerializer(serializers.ModelSerializer):
    publicado = serializers.BooleanField(
        write_only=True,
    )

    class Meta:
        model = Inmueble
        fields = [
            "estado",
            "publicado",
        ]
        read_only_fields = [
            "estado",
        ]

    def update(self, instance, validated_data):
        try:
            if validated_data["publicado"]:
                instance.estado = EstadoInmueble.objects.get(nombre="Publicado")
            else:
                instance.estado = EstadoInmueble.objects.get(nombre="En borrador")
            instance.save()
        except EstadoInmueble.DoesNotExist:
            raise serializers.ValidationError("Estado no encontrado")
        return instance


class ImagenCrudSerializer(serializers.ModelSerializer):
    imagen = Base64ImageField()

    class Meta:
        model = ImagenInmueble
        fields = [
            "id",
            "indice",
            "imagen",
            "titulo",
            "is_portada",
        ]
        extra_kwargs = {
            "id": {"read_only": False},
        }


class PlanoCrudSerializer(serializers.ModelSerializer):
    plano = Base64ImageField()

    class Meta:
        model = PlanoInmueble
        fields = [
            "id",
            "plano",
            "titulo",
        ]
        extra_kwargs = {
            "id": {"read_only": False},
        }


class UbicacionCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbicacionInmueble
        fields = [
            "distrito",
            "calle",
            "numero",
            "latitud",
            "longitud",
        ]


class CaracteristicaCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristica
        fields = [
            "id",
        ]


class InmuebleCrudSerializer(serializers.ModelSerializer):
    caracteristicas = CaracteristicaCrudSerializer(many=True, required=False)
    imagenes = ImagenCrudSerializer(many=True, required=False)
    planos = PlanoCrudSerializer(many=True, required=False)
    ubicacion = UbicacionCrudSerializer(required=False)

    class Meta:
        model = Inmueble
        fields = [
            "id",
            "titulo",
            "descripcion",
            "tipo_operacion",
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
            "imagenes",
            "planos",
            "ubicacion",
        ]
        extra_kwargs = {
            "titulo": {"required": False},
            "descripcion": {"required": False},
            "tipo_operacion": {"required": False},
            "habitaciones": {"required": False},
            "baños": {"required": False},
            "pisos": {"required": False},
            "ascensores": {"required": False},
            "estacionamientos": {"required": False},
            "area_construida": {"required": False},
            "area_total": {"required": False},
            "precio_soles": {"required": False},
            "precio_dolares": {"required": False},
            "mantenimiento": {"required": False},
            "tipo_antiguedad": {"required": False},
            "años": {"required": False},
            "tipo_inmueble": {"required": False},
            "subtipo_inmueble": {"required": False},
        }

    @atomic
    def create(self, validated_data):
        # caracteristicas_data = validated_data.pop("caracteristicas")
        # imagenes_data = validated_data.pop("imagenes")
        # planos_data = validated_data.pop("planos")
        # ubicacion_data = validated_data.pop("ubicacion")
        estado = EstadoInmueble.objects.get(nombre="En borrador")
        inmueble = Inmueble.objects.create(estado=estado, **validated_data)
        # ubicacion = UbicacionInmueble.objects.create(
        #     inmueble=inmueble, **ubicacion_data
        # )
        # for caracteristica_data in caracteristicas_data:
        #     caracteristica = Caracteristica.objects.get(**caracteristica_data)
        #     inmueble.caracteristicas.add(caracteristica)
        # for imagen_data in imagenes_data:
        #     ImagenInmueble.objects.create(inmueble=inmueble, **imagen_data)
        # for plano_data in planos_data:
        #     PlanoInmueble.objects.create(inmueble=inmueble, **plano_data)
        return inmueble

    @atomic
    def update(self, instance, validated_data):
        caracteristicas_data = validated_data.pop("caracteristicas", [])
        imagenes_data = validated_data.pop("imagenes", [])
        planos_data = validated_data.pop("planos", [])
        ubicacion_data = validated_data.pop("ubicacion", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        for caracteristica_data in caracteristicas_data:
            caracteristica = Caracteristica.objects.get(**caracteristica_data)
            instance.caracteristicas.add(caracteristica)
        for imagen_data in imagenes_data:
            ImagenInmueble.objects.create(inmueble=instance, **imagen_data)
        for plano_data in planos_data:
            PlanoInmueble.objects.create(inmueble=instance, **plano_data)

        if ubicacion_data is not None:

            try:
                ubicacion = UbicacionInmueble.objects.get(inmueble=instance)
                for key, value in ubicacion_data.items():
                    setattr(ubicacion, key, value)
                ubicacion.save()
            except UbicacionInmueble.DoesNotExist:
                ubicacion = UbicacionInmueble.objects.create(
                    inmueble=instance, **ubicacion_data
                )

        return instance
