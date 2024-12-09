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
    telefono = models.CharField(max_length=9)
    plan = models.ForeignKey(PlanPrestamos, on_delete=models.PROTECT)
    entidad = models.ForeignKey(EntidadBancaria, on_delete=models.PROTECT)
