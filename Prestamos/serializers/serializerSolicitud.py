from math import e
from os import read
from django.http import QueryDict
from rest_framework import serializers
from django.db.transaction import atomic
from Usuarios.models import Usuario
from ..models import (
    EstadoEvaluacion,
    EvaluacionCrediticia,
    EtapaEvaluacion,
    Documento,
    Comentario,
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
    nuevo = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = Documento
        fields = ["id", "nombre", "descripcion", "archivo", "nuevo"]
        extra_kwargs = {
            "id": {"read_only": False},
        }


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ["id", "comentario", "fecha", "visible"]
        extra_kwargs = {
            "id": {"read_only": True},
        }


class EvaluacionSolicitudSerializer(serializers.ModelSerializer):
    """
    este es el serializador para los datos de la etapa de solicitud
    """

    prestatario = PrestatarioDatosSerializer(
        source="prestatario.usuario", read_only=True
    )

    documentos = DocumentoSerializer(
        read_only=False,
        many=True,
    )

    comentarios = ComentarioSerializer(
        read_only=False,
        many=True,
    )

    fecha_inicio = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    fecha_fin_estimada = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    fecha_fin_real = serializers.DateTimeField(
        format="%Y-%m-%d", required=False, allow_null=True, read_only=True
    )

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
            "comentarios",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "prestatario": {"read_only": True},
            "estado": {"read_only": True},
            "etapa": {"read_only": True},
        }

    def validate(self, attrs):
        if self.instance.etapa.nombre != "Solicitud":
            raise serializers.ValidationError(
                "No se puede modificar una evaluación en otra etapa"
            )
        return super().validate(attrs)

    @atomic
    def update(self, instance: EvaluacionCrediticia, validated_data):
        documentos_data = validated_data.pop("documentos", [])
        comentarios_data = validated_data.pop("comentarios", [])
        documentos = Documento.objects.filter(
            etapa__nombre="Solicitud", evaluacion=instance
        )

        usuario = self.context["request"].user

        if hasattr(usuario, "perfil_prestatario"):
            self._update_prestatario_documentos(documentos, documentos_data)
        elif hasattr(usuario, "perfil_agente_hipotecario"):
            self._update_agente_documentos(documentos, documentos_data, instance)
            self._update_comentarios(comentarios_data)

        return super().update(instance, validated_data)

    def _update_comentarios(self, comentarios_data):
        self.instance.comentarios.filter(etapa__nombre="Solicitud").delete()
        for comentario_data in comentarios_data:
            Comentario.objects.create(
                evaluacion=self.instance,
                etapa=EtapaEvaluacion.objects.get(nombre="Solicitud"),
                **comentario_data,
            )

    def _update_prestatario_documentos(self, documentos, documentos_data):
        for documento_data in documentos_data:
            documento_id = documento_data.get("id")
            if documento_id:
                try:
                    documento = documentos.get(id=documento_id)
                    documento.archivo = documento_data.get("archivo", documento.archivo)
                    documento.save()
                except Documento.DoesNotExist:
                    pass

    def _update_agente_documentos(self, documentos, documentos_data, instance):
        documento_ids = [
            doc_data.get("id") for doc_data in documentos_data if doc_data.get("id")
        ]
        documentos.exclude(id__in=documento_ids).delete()

        for documento_data in documentos_data:
            documento_id = documento_data.get("id")
            if documento_data.get("nuevo", False):
                documento_data.pop("nuevo")
                Documento.objects.create(
                    evaluacion=instance,
                    etapa=EtapaEvaluacion.objects.get(nombre="Solicitud"),
                    **documento_data,
                )
            elif documento_id:
                try:
                    documento = documentos.get(id=documento_id)
                    documento.nombre = documento_data.get("nombre", documento.nombre)
                    documento.descripcion = documento_data.get(
                        "descripcion", documento.descripcion
                    )
                    documento.save()
                except Documento.DoesNotExist:
                    pass


class PasarEtapaSerializer(serializers.ModelSerializer):
    """
    este es el serializador para pasar de etapa de solicitud a etapa de evaluación
    """

    etapa = serializers.StringRelatedField(source="etapa.nombre", read_only=True)

    class Meta:
        model = EvaluacionCrediticia
        fields = ["etapa"]

    @atomic
    def update(self, instance: EvaluacionCrediticia, validated_data):
        # primero vamos a validar si tenemos fecha de inicio y fin correctamente ingresadas

        if not instance.fecha_inicio or not instance.fecha_fin_estimada:
            raise serializers.ValidationError(
                "No se puede pasar de etapa sin tener fecha de inicio o fin estimada"
            )

        # ahora vamos a validar si todos los documentos tienen un archivo adjunto

        documentos = Documento.objects.filter(
            etapa__nombre="Solicitud", evaluacion=instance
        )

        for documento in documentos:
            if not documento.archivo:
                raise serializers.ValidationError(
                    f"El documento {documento.nombre} no tiene un archivo adjunto"
                )

        # ahora si vamos a actualizar la etapa de la evaluación

        etapa_evaluacion = EtapaEvaluacion.objects.get(nombre="Evaluación")
        estado_evaluacion = EstadoEvaluacion.objects.get(nombre="En evaluación")
        instance.etapa = etapa_evaluacion
        instance.estado = estado_evaluacion

        instance.save()

        return instance
