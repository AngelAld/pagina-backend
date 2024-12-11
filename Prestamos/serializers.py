from os import read
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    PrimaryKeyRelatedField,
)
from .models import (
    EntidadBancaria,
    PerfilPrestatarioPrefab,
    EstadoEvaluacion,
    EtapaEvaluacion,
    DocumentoEvaluacionPrefab,
    PreguntaPerfil,
    RespuestaPerfil,
)
from django.db.transaction import atomic


class RespuestaPerfilSerializer(ModelSerializer):
    class Meta:
        model = RespuestaPerfil
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class PreguntaPerfilSerializer(ModelSerializer):
    respuestas = RespuestaPerfilSerializer(many=True, read_only=True)

    class Meta:
        model = PreguntaPerfil
        fields = [
            "id",
            "nombre",
            "descripcion",
            "respuestas",
        ]


class EntidadBancariaSerializer(ModelSerializer):
    class Meta:
        model = EntidadBancaria
        fields = [
            "id",
            "nombre",
        ]


class DocumentoEvaluacionPrefabSerializer(ModelSerializer):
    class Meta:
        model = DocumentoEvaluacionPrefab
        fields = [
            "id",
            "nombre",
            "descripcion",
            "etapa",
        ]


class PerfilPrestatarioPrefabListSerializer(ModelSerializer):
    documentos = SerializerMethodField()

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


class PerfilPrestatarioPrefabSerializer(ModelSerializer):
    documentos = DocumentoEvaluacionPrefabSerializer(many=True, required=False)
    respuestas = PrimaryKeyRelatedField(
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
        for respuesta in respuestas_data:
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


class EtapaEvalucionSerializer(ModelSerializer):
    class Meta:
        model = EtapaEvaluacion
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]


class EstadoEvaluacionSerializer(ModelSerializer):
    class Meta:
        model = EstadoEvaluacion
        fields = [
            "id",
            "nombre",
            "descripcion",
        ]
