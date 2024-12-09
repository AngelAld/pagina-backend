from django.db import models

from Planes.models import PlanPrestamos
from Usuarios.models import Usuario


class EntidadBancaria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    estado = models.BooleanField(default=True)


class PerfilAgenteHipotecario(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_agente_hipotecario"
    )
    avatar = models.ImageField(upload_to="avatar/agentes", null=True, blank=True)
    banner = models.ImageField(upload_to="banner/agentes", null=True, blank=True)
    telefono = models.CharField(max_length=9)
    plan = models.ForeignKey(PlanPrestamos, on_delete=models.PROTECT)
    entidad = models.ForeignKey(EntidadBancaria, on_delete=models.PROTECT)


class PerfilPrestatarioPrefab(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="prefabs_perfiles"
    )
    # resto de campos a definir


class EtapaEvaluacion(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )


class EstadoEvaluacion(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )


class DocumentoEvaluacionPrefab(models.Model):
    perfil_prefab = models.ForeignKey(PerfilPrestatarioPrefab, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    etapa = models.ForeignKey(EtapaEvaluacion, on_delete=models.PROTECT)


class PerfilPrestatario(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_prestatario"
    )
    # resto de campos a definir


class EvaluacionCrediticia(models.Model):
    prestatario = models.ForeignKey(
        PerfilPrestatario,
        on_delete=models.CASCADE,
        related_name="evaluaciones",
    )
    agente = models.ForeignKey(
        PerfilAgenteHipotecario,
        on_delete=models.CASCADE,
        related_name="evaluaciones",
    )


class Comentario(models.Model):
    evaluacion = models.ForeignKey(EvaluacionCrediticia, on_delete=models.CASCADE)
    comentario = models.TextField()
    visible = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    etapa = models.ForeignKey(EtapaEvaluacion, on_delete=models.PROTECT)


class Documento(models.Model):
    evaluacion = models.ForeignKey(EvaluacionCrediticia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    archivo = models.FileField(
        upload_to="evaluaciones/documentos", null=True, blank=True
    )
    etapa = models.ForeignKey(EtapaEvaluacion, on_delete=models.PROTECT)
