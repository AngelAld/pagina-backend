from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from Planes.models import PlanInmuebles, PlanPrestamos, PlanServicios
from Prestamos.models import EntidadBancaria
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


class AuthProvider(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    dni = models.CharField(max_length=8, unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    provider = models.ManyToManyField(AuthProvider, related_name="usuarios")
    tipo_usuario = models.ManyToManyField(TipoUsuario, related_name="usuarios")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombres", "apellidos"]

    objects = UserManager()

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")

    def __str__(self):
        return self.email

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class CodigoUnUso(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="contraseñas_temporales"
    )
    codigo = models.CharField(max_length=6)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.email} - {self.codigo}"


class PerfilCliente(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_cliente"
    )
    telefono = models.CharField(max_length=9)
    plan_inmuebles = models.ForeignKey(
        PlanInmuebles, on_delete=models.PROTECT, related_name="clientes"
    )
    plan_prestamos = models.ForeignKey(
        PlanPrestamos, on_delete=models.PROTECT, related_name="clientes"
    )

    def __str__(self):
        return self.usuario.nombre_completo


class PerfilParticularInmuebles(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_particular"
    )
    avatar = models.ImageField(upload_to="avatar/particulares", null=True, blank=True)
    telefono = models.CharField(max_length=9)
    plan = models.ForeignKey(
        PlanInmuebles, on_delete=models.PROTECT, related_name="particulares"
    )

    def __str__(self):
        return self.usuario.nombre_completo


class PerfilInmobiliaria(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_inmobiliaria"
    )
    avatar = models.ImageField(upload_to="avatar/inmobiliarias", null=True, blank=True)
    razon_social = models.CharField(max_length=255)
    ruc = models.CharField(max_length=11, unique=True)
    telefono = models.CharField(max_length=9)
    plan = models.ForeignKey(PlanInmuebles, on_delete=models.PROTECT)
    aprobada = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.nombre_completo


class PerfilEmpleadoInmobiliaria(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_empleado"
    )
    avatar = models.ImageField(upload_to="avatar/empleados", null=True, blank=True)

    telefono = models.CharField(max_length=9)
    inmobiliaria = models.ForeignKey(
        PerfilInmobiliaria, on_delete=models.CASCADE, related_name="empleados"
    )

    def __str__(self):
        return self.usuario.nombre_completo


class PerfilAgentePrestamos(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_agente"
    )
    avatar = models.ImageField(upload_to="avatar/agentes", null=True, blank=True)
    telefono = models.CharField(max_length=9)
    plan = models.ForeignKey(PlanPrestamos, on_delete=models.PROTECT)
    entidad = models.ForeignKey(EntidadBancaria, on_delete=models.PROTECT)


class PerfilProfesionalServicios(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_profesional"
    )

    telefono = models.CharField(max_length=9)
    plan = models.ForeignKey(PlanServicios, on_delete=models.PROTECT)
