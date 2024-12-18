from django.db import models
from Inmuebles.models import Inmueble
from Planes.models import PlanPrestamos
from Usuarios.models import Usuario


class EntidadBancaria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class PerfilAgenteHipotecario(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_agente_hipotecario"
    )
    avatar = models.ImageField(upload_to="avatar/agentes", null=True, blank=True)
    banner = models.ImageField(upload_to="banner/agentes", null=True, blank=True)
    telefono = models.CharField(max_length=9)
    plan = models.ForeignKey(PlanPrestamos, on_delete=models.PROTECT)
    entidad = models.ForeignKey(EntidadBancaria, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.usuario}"


class PreguntaPerfil(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nombre


class RespuestaPerfil(models.Model):
    pregunta = models.ForeignKey(
        PreguntaPerfil, on_delete=models.CASCADE, related_name="respuestas"
    )
    nombre = models.CharField(max_length=255)

    descripcion = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ("pregunta", "nombre")

    def __str__(self):
        return f"{self.pregunta}: {self.nombre}"


class PerfilPrestatarioPrefab(models.Model):
    dueño = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="prefabs_perfiles"
    )
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    respuestas = models.ManyToManyField(RespuestaPerfil)

    def __str__(self):
        return f"{self.dueño} - {self.nombre}"


class EtapaEvaluacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nombre


class EstadoEvaluacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    is_system_managed = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class DocumentoEvaluacionPrefab(models.Model):
    perfil_prefab = models.ForeignKey(
        PerfilPrestatarioPrefab, on_delete=models.CASCADE, related_name="documentos"
    )
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    etapa = models.ForeignKey(EtapaEvaluacion, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nombre}"


class PerfilPrestatario(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_prestatario"
    )
    inmueble = models.ForeignKey(
        Inmueble,
        on_delete=models.SET_NULL,
        related_name="prestatarios",
        null=True,
        blank=True,
    )
    respuestas = models.ManyToManyField(RespuestaPerfil)

    def __str__(self):
        return f"{self.usuario}"


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

    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin_estimada = models.DateTimeField(null=True, blank=True)
    fecha_fin_real = models.DateTimeField(null=True, blank=True)

    estado = models.ForeignKey(
        EstadoEvaluacion, on_delete=models.PROTECT, null=True, blank=True
    )
    etapa = models.ForeignKey(EtapaEvaluacion, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.prestatario} - {self.agente}"


class Comentario(models.Model):
    evaluacion = models.ForeignKey(
        EvaluacionCrediticia, on_delete=models.CASCADE, related_name="comentarios"
    )
    comentario = models.TextField()
    visible = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    etapa = models.ForeignKey(EtapaEvaluacion, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.evaluacion} - {self.fecha}"


class Documento(models.Model):
    evaluacion = models.ForeignKey(
        EvaluacionCrediticia, on_delete=models.CASCADE, related_name="documentos"
    )
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    archivo = models.FileField(
        upload_to="evaluaciones/documentos", null=True, blank=True
    )
    etapa = models.ForeignKey(EtapaEvaluacion, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre
