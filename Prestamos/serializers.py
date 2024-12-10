from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (
    EntidadBancaria,
    PerfilPrestatarioPrefab,
    EstadoEvaluacion,
    EtapaEvaluacion,
    DocumentoEvaluacionPrefab,
)
from django.db.transaction import atomic


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

    class Meta:
        model = PerfilPrestatarioPrefab
        fields = [
            "id",
            "nombre",
            "descripcion",
            "documentos",
        ]
        extra_kwargs = {
            "descripcion": {"required": False},
        }

    @atomic
    def create(self, validated_data):
        dueño = self.context["request"].user
        documentos_data = validated_data.pop("documentos", [])
        perfil_prefab = PerfilPrestatarioPrefab.objects.create(
            dueño=dueño, **validated_data
        )
        for documento_data in documentos_data:
            DocumentoEvaluacionPrefab.objects.create(
                perfil_prefab=perfil_prefab, **documento_data
            )
        return perfil_prefab

    @atomic
    def update(self, instance, validated_data):
        instance.documentos.all().delete()
        documentos_data = validated_data.pop("documentos", [])

        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.descripcion = validated_data.get("descripcion", instance.descripcion)

        # TODO: resto de campos de PerfilPrestatarioPrefab

        instance.save()

        for documento_data in documentos_data:
            DocumentoEvaluacionPrefab.objects.create(
                perfil_prefab=instance, **documento_data
            )
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
