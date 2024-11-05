from django.db import models


class EntidadBancaria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    estado = models.BooleanField(default=True)
