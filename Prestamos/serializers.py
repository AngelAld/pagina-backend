from importlib.metadata import requires
from os import read
from pyexpat import model

from rest_framework import serializers
from Usuarios.models import Usuario
from .models import (
    EntidadBancaria,
    PerfilPrestatarioPrefab,
    EstadoEvaluacion,
    EtapaEvaluacion,
    DocumentoEvaluacionPrefab,
    PreguntaPerfil,
    RespuestaPerfil,
    PerfilPrestatario,
)
from django.db.transaction import atomic


class RespuestaPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaPerfil
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class PreguntaPerfilSerializer(serializers.ModelSerializer):
    respuestas = RespuestaPerfilSerializer(many=True, read_only=True)

    class Meta:
        model = PreguntaPerfil
        fields = [
            "id",
            "nombre",
            "descripcion",
            "respuestas",
        ]


class EntidadBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntidadBancaria
        fields = [
            "id",
            "nombre",
        ]


class DocumentoEvaluacionPrefabSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoEvaluacionPrefab
        fields = [
            "id",
            "nombre",
            "descripcion",
            "etapa",
        ]


class PerfilPrestatarioPrefabListSerializer(serializers.ModelSerializer):
    documentos = serializers.SerializerMethodField()

    def get_documentos(self, obj) -> int:
        return obj.documentos.count()

    class Meta:
        model = PerfilPrestatarioPrefab
        fields = [
            "id",
            "nombre",
            "descripcion",
            "documentos",
        ]


class PerfilPrestatarioPrefabSerializer(serializers.ModelSerializer):
    documentos = DocumentoEvaluacionPrefabSerializer(many=True, required=False)
    respuestas = serializers.PrimaryKeyRelatedField(
        queryset=RespuestaPerfil.objects.all(), many=True, required=False
    )

    class Meta:
        model = PerfilPrestatarioPrefab
        fields = [
            "id",
            "nombre",
            "descripcion",
            "documentos",
            "respuestas",
        ]
        extra_kwargs = {
            "descripcion": {"required": False},
        }

    @atomic
    def create(self, validated_data):
        dueño = self.context["request"].user
        documentos_data = validated_data.pop("documentos", [])
        respuestas_data = validated_data.pop("respuestas", [])
        perfil_prefab = PerfilPrestatarioPrefab.objects.create(
            dueño=dueño, **validated_data
        )
        for documento_data in documentos_data:
            DocumentoEvaluacionPrefab.objects.create(
                perfil_prefab=perfil_prefab, **documento_data
            )
        num_preguntas = PreguntaPerfil.objects.count()
        for index, respuesta in enumerate(respuestas_data, start=1):
            if index > num_preguntas:
                break
            perfil_prefab.respuestas.add(respuesta)
        perfil_prefab.save()
        return perfil_prefab

    @atomic
    def update(self, instance, validated_data):
        instance.documentos.all().delete()
        documentos_data = validated_data.pop("documentos", [])
        respuestas_data = validated_data.pop("respuestas", [])
        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.descripcion = validated_data.get("descripcion", instance.descripcion)
        instance.respuestas.clear()

        num_preguntas = PreguntaPerfil.objects.count()
        for index, respuesta in enumerate(respuestas_data, start=1):
            if index > num_preguntas:
                break
            instance.respuestas.add(respuesta)

        for documento_data in documentos_data:
            DocumentoEvaluacionPrefab.objects.create(
                perfil_prefab=instance, **documento_data
            )
        print("###########################")
        print(instance.respuestas.all())
        print("###########################")
        instance.save()
        return instance


class EtapaEvalucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapaEvaluacion
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class EstadoEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoEvaluacion
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class PerfilPrestatarioSerializer(serializers.ModelSerializer):
    respuestas = serializers.PrimaryKeyRelatedField(
        queryset=RespuestaPerfil.objects.all(), many=True, required=True
    )

    class Meta:
        model = PerfilPrestatario
        fields = [
            "id",
            "inmueble",
            "respuestas",
        ]
        extra_kwargs = {
            "inmueble": {"required": False},
        }


class PerfilPrestatarioUserSerializer(serializers.ModelSerializer):
    perfil_prestatario = PerfilPrestatarioSerializer(required=True)

    class Meta:
        model = Usuario
        fields = [
            "perfil_prestatario",
        ]

    @atomic
    def create(self, validated_data):
        usuario = self.context["request"].user
        request = self.context.get("request")
        if request is None or not hasattr(request, "user"):
            raise serializers.ValidationError("No se ha iniciado sesión")
        if hasattr(usuario, "perfil_prestatario"):
            raise serializers.ValidationError(
                "El usuario ya tiene un perfil prestario asociado"
            )
        perfil_data = validated_data.pop("perfil_prestatario")
        respuestas_data = perfil_data.pop("respuestas", [])
        perfil_prestatario = PerfilPrestatario.objects.create(usuario=usuario)
        num_preguntas = PreguntaPerfil.objects.count()
        for index, respuesta in enumerate(respuestas_data, start=1):
            if index > num_preguntas:
                break
            perfil_prestatario.respuestas.add(respuesta)
        perfil_prestatario.save()
        return usuario

    @atomic
    def update(self, instance, validated_data):
        perfil = instance.perfil_prestatario
        perfil_data = validated_data["perfil_prestatario"]
        respuestas_data = perfil_data.pop("respuestas", [])
        perfil.respuestas.clear()
        num_preguntas = PreguntaPerfil.objects.count()
        for index, respuesta in enumerate(respuestas_data, start=1):
            if index > num_preguntas:
                break
            perfil.respuestas.add(respuesta)
        inmueble = perfil_data.get("inmueble", None)
        if inmueble is not None:
            perfil.inmueble = inmueble
        perfil.save()
        return instance
