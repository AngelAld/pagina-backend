from django.http import QueryDict
from rest_framework import serializers

from Usuarios.models import Usuario
from .models import (
    EvaluacionCrediticia,
    EtapaEvaluacion,
    EstadoEvaluacion,
    Documento,
    Comentario,
    PerfilPrestatario,
    RespuestaPerfil,
)


class RespuestasSerializer(serializers.ModelSerializer):
    pregunta = serializers.StringRelatedField(read_only=True, source="pregunta.nombre")
    respuesta = serializers.StringRelatedField(source="nombre")

    class Meta:
        model = RespuestaPerfil
        fields = ["pregunta", "respuesta"]


class PrestatarioDatosSerializer(serializers.ModelSerializer):
    perfil = RespuestasSerializer(
        many=True, read_only=True, source="perfil_prestatario.respuestas"
    )

    class Meta:
        model = Usuario
        fields = [
            "email",
            "dni",
            "nombres",
            "apellidos",
            "perfil",
        ]


class DocumentoSerializer(serializers.ModelSerializer):
    etapa = serializers.StringRelatedField(source="etapa.nombre")

    class Meta:
        model = Documento
        fields = [
            "id",
            "nombre",
            "descripcion",
            "archivo",
            "etapa",
        ]


class EvaluacionSolicitudSerializer(serializers.ModelSerializer):
    """
    este es el serializador para los datos de la etapa de solicitud
    """

    prestatario = PrestatarioDatosSerializer(
        source="prestatario.usuario", read_only=True
    )

    documentos = serializers.SerializerMethodField(
        method_name="get_documentos",
    )

    def get_documentos(self, obj) -> DocumentoSerializer:
        documentos = Documento.objects.filter(etapa__nombre="Solicitud")
        return DocumentoSerializer(documentos, many=True).data

    class Meta:
        model = EvaluacionCrediticia
        fields = [
            "id",
            "prestatario",
            "fecha_inicio",
            "fecha_fin_estimada",
            "fecha_fin_real",
            "estado",
            "etapa",
            "documentos",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "prestatario": {"read_only": True},
            "estado": {"read_only": True},
            "etapa": {"read_only": True},
        }
