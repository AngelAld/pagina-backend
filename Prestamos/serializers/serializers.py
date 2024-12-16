from django.db.transaction import atomic
from rest_framework import serializers

from Inmuebles.serializers import InmuebleListSerializer
from Usuarios.models import Usuario

from ..models import (
    Documento,
    DocumentoEvaluacionPrefab,
    EntidadBancaria,
    EstadoEvaluacion,
    EtapaEvaluacion,
    EvaluacionCrediticia,
    PerfilPrestatario,
    PerfilPrestatarioPrefab,
    PreguntaPerfil,
    RespuestaPerfil,
)


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


class RespuestaListSerializer(serializers.ModelSerializer):
    pregunta = serializers.StringRelatedField()
    # descripcion_pregunta = serializers.StringRelatedField(source="pregunta.descripcion")
    respuesta = serializers.StringRelatedField(source="nombre")

    class Meta:
        model = RespuestaPerfil
        fields = [
            "pregunta",
            # "descripcion_pregunta",
            "respuesta",
            # "descripcion",
        ]


class RespuestaDetalleSerializer(serializers.ModelSerializer):
    pregunta = serializers.StringRelatedField()
    descripcion_pregunta = serializers.StringRelatedField(source="pregunta.descripcion")
    respuesta = serializers.StringRelatedField(source="nombre")

    class Meta:
        model = RespuestaPerfil
        fields = [
            "pregunta",
            "descripcion_pregunta",
            "respuesta",
            "descripcion",
        ]


class EvaluacionListSerializer(serializers.ModelSerializer):
    entidad = serializers.StringRelatedField(source="agente.entidad")

    class Meta:
        model = EvaluacionCrediticia
        fields = [
            "entidad",
        ]


class EvaluacionDetalleSerializer(serializers.ModelSerializer):
    entidad = serializers.StringRelatedField(source="agente.entidad")
    estado = serializers.StringRelatedField(source="estado.nombre")
    etapa = serializers.StringRelatedField(source="etapa.nombre")

    class Meta:
        model = EvaluacionCrediticia
        fields = [
            "entidad",
            "estado",
            "etapa",
        ]


class PerfilPrestatarioListSerializer(serializers.ModelSerializer):
    respuestas = RespuestaListSerializer(
        many=True,
        read_only=True,
    )
    inmueble = serializers.StringRelatedField(source="inmueble.slug")
    evaluaciones = EvaluacionListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = PerfilPrestatario
        fields = ["inmueble", "respuestas", "evaluaciones"]


class PerfilPrestatarioDetalleSerializer(serializers.ModelSerializer):
    respuestas = RespuestaDetalleSerializer(
        many=True,
        read_only=True,
    )
    inmueble = InmuebleListSerializer()
    evaluaciones = EvaluacionDetalleSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = PerfilPrestatario
        fields = ["inmueble", "respuestas", "evaluaciones"]


class NuevosClientesListSerializer(serializers.ModelSerializer):
    perfil_prestatario = PerfilPrestatarioListSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "dni",
            "perfil_prestatario",
        ]


class NuevoClienteDetalleSerializer(serializers.ModelSerializer):

    perfil_prestatario = PerfilPrestatarioDetalleSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "dni",
            "perfil_prestatario",
        ]
        extra_kwargs = {
            "id": {"read_only": False},
            "email": {"read_only": True},
            "nombres": {"read_only": True},
            "apellidos": {"read_only": True},
            "dni": {"read_only": True},
        }

    @atomic
    def update(self, instance: Usuario, validated_data):
        usuario: Usuario = self.context["request"].user

        # TODO: refactorizar esto en un permiso

        if not hasattr(usuario, "perfil_agente_hipotecario"):
            raise serializers.ValidationError(
                "No tienes permisos para realizar esta acción"
            )

        #

        if not hasattr(instance, "perfil_prestatario"):
            raise serializers.ValidationError(
                "El cliente no tiene un perfil de prestatario"
            )

        prestatario: PerfilPrestatario = instance.perfil_prestatario

        entidad: EntidadBancaria = usuario.perfil_agente_hipotecario.entidad

        if prestatario.evaluaciones.filter(
            agente__entidad=entidad,
        ).exists():
            raise serializers.ValidationError(
                "El cliente ya está siendo evaluado por tu entidad"
            )

        evaluacion = EvaluacionCrediticia.objects.create(
            prestatario=prestatario,
            agente=usuario.perfil_agente_hipotecario,
            estado=EstadoEvaluacion.objects.get(nombre="En solicitud"),
            etapa=EtapaEvaluacion.objects.get(nombre="Solicitud"),
        )

        prefabs = PerfilPrestatarioPrefab.objects.filter(dueño=usuario)

        for prefab in prefabs:
            if not self._respuestas_match(
                prefab.respuestas.all(), prestatario.respuestas.all()
            ):
                continue
            self._create_documentos_from_prefab(prefab, evaluacion)

        return instance

    def _respuestas_match(self, respuestas_prefab, prestatario_respuestas):
        if respuestas_prefab.count() != prestatario_respuestas.count():
            return False
        return not respuestas_prefab.exclude(
            id__in=prestatario_respuestas.values_list("id", flat=True)
        ).exists()

    def _create_documentos_from_prefab(self, prefab, evaluacion):
        for documento in prefab.documentos.all():
            Documento.objects.create(
                evaluacion=evaluacion,
                nombre=documento.nombre,
                descripcion=documento.descripcion,
                etapa=documento.etapa,
            )


class PerfilPrestatarioEvaluacionListSerializer(serializers.ModelSerializer):
    respuestas = RespuestaListSerializer(
        many=True,
        read_only=True,
    )
    # inmueble = serializers.StringRelatedField(source="inmueble.slug")

    class Meta:
        model = PerfilPrestatario
        fields = [
            # "inmueble",
            "respuestas",
        ]


class PrestatarioEvaluacionListSerializer(serializers.ModelSerializer):
    perfil_prestatario = PerfilPrestatarioEvaluacionListSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "dni",
            "perfil_prestatario",
        ]


class EvaluacionCrediticiaListSerializer(serializers.ModelSerializer):
    prestatario = PrestatarioEvaluacionListSerializer(
        source="prestatario.usuario", read_only=True
    )
    estado = serializers.StringRelatedField(
        source="estado.nombre",
    )
    etapa = serializers.StringRelatedField(
        source="etapa.nombre",
    )

    class Meta:
        model = EvaluacionCrediticia
        fields = [
            "id",
            "prestatario",
            "estado",
            "etapa",
            "fecha_inicio",
            "fecha_fin_estimada",
        ]
