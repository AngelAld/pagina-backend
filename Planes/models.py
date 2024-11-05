from django.db import models


class PlanInmuebles(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    max_propiedades = models.PositiveIntegerField()
    max_empleados = models.PositiveIntegerField()
    max_alertas = models.PositiveIntegerField()
    compartir_comision = models.BooleanField(default=False)


class PlanPrestamos(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    max_clientes = models.PositiveIntegerField()
    max_empleados = models.PositiveIntegerField()
    max_alertas = models.PositiveIntegerField()
    # compartir_comision = models.BooleanField(default=False)


class PlanServicios(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        null=True,
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    max_ocupaciones = models.PositiveIntegerField()
    max_habilidades = models.PositiveIntegerField()
    max_avisos = models.PositiveIntegerField()
    max_alertas = models.PositiveIntegerField()
    # compartir_comision = models.BooleanField(default=False)
