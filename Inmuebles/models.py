from django.db import models
from Ubicacion.models import Distrito
from Usuarios.models import Usuario
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.text import slugify


# Create your models here.
class Caracteristica(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class TipoAntiguedad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class SubTipoInmueble(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre


class EstadoInmueble(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class TipoOperacion(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Inmueble(models.Model):
    dueño = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="inmuebles"
    )
    titulo = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(10), MaxLengthValidator(100)],
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    descripcion = models.TextField(blank=True, null=True)
    tipo_operacion = models.ForeignKey(TipoOperacion, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.ForeignKey(EstadoInmueble, on_delete=models.PROTECT)
    habitaciones = models.PositiveIntegerField(blank=True, null=True, default=0)
    baños = models.PositiveIntegerField(blank=True, null=True, default=0)
    pisos = models.PositiveIntegerField(blank=True, null=True, default=1)
    ascensores = models.PositiveIntegerField(blank=True, null=True, default=0)
    estacionamientos = models.PositiveIntegerField(blank=True, null=True, default=0)
    area_construida = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    area_total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    precio_soles = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    precio_dolares = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    mantenimiento = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    tipo_antiguedad = models.ForeignKey(
        TipoAntiguedad, on_delete=models.PROTECT, blank=True, null=True
    )
    años = models.PositiveIntegerField(blank=True, null=True, default=0)
    tipo_inmueble = models.ForeignKey(
        TipoInmueble,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    subtipo_inmueble = models.ForeignKey(
        SubTipoInmueble, on_delete=models.PROTECT, blank=True, null=True
    )
    caracteristicas = models.ManyToManyField(Caracteristica, blank=True)

    @property
    def portada(self) -> str:
        return (
            ImagenInmueble.objects.filter(inmueble=self, is_portada=True)
            .first()
            .imagen.url
        )

    @property
    def num_favoritos(self) -> int:
        return self.favoritos.count()

    @property
    def num_visitas(self) -> int:
        return self.visitas.count()

    def save(self, **kwargs):
        slug_base = slugify(self.titulo or "Inmueble")
        if not self.slug or self.slug != slug_base:
            slug = slug_base
            original_slug = slug
            counter = 1
            while Inmueble.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            self.slug = slug

        super(Inmueble, self).save(**kwargs)

    def __str__(self):
        return f"{self.dueño} - {self.id}"


class ImagenInmueble(models.Model):
    indice = models.PositiveIntegerField(default=0)
    inmueble = models.ForeignKey(
        Inmueble, on_delete=models.CASCADE, related_name="imagenes"
    )
    imagen = models.ImageField(upload_to="inmuebles/")
    titulo = models.CharField(max_length=100, blank=True)
    is_portada = models.BooleanField(default=False)

    def __str__(self):
        return self.imagen.url


class PlanoInmueble(models.Model):
    inmueble = models.ForeignKey(
        Inmueble, on_delete=models.CASCADE, related_name="planos"
    )
    plano = models.ImageField(upload_to="planos/")
    titulo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.plano.url


class UbicacionInmueble(models.Model):
    inmueble = models.OneToOneField(
        Inmueble, on_delete=models.CASCADE, related_name="ubicacion"
    )
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return f"{self.distrito}, {self.calle} {self.numero}"


# TODO: Modelo de alertas


class Favorito(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="favoritos"
    )
    inmueble = models.ForeignKey(
        Inmueble, on_delete=models.CASCADE, related_name="favoritos"
    )

    def __str__(self):
        return f"{self.usuario} - {self.inmueble}"


class Visita(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="visitas"
    )
    inmueble = models.ForeignKey(
        Inmueble, on_delete=models.CASCADE, related_name="visitas"
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.inmueble} - {self.fecha}"
