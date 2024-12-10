from pydoc import doc
from rest_framework.serializers import ModelSerializer
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


class PerfilPrestatarioPrefabSerializer(ModelSerializer):
    documentos = DocumentoEvaluacionPrefabSerializer(many=True)

    class Meta:
        model = PerfilPrestatarioPrefab
        fields = [
            "id",
            "documentos",
        ]

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

        # TODO: logica del resto de campos de PerfilPrestatarioPrefab

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
