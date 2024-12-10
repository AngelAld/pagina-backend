from rest_framework import serializers
from rest_framework.serializers import ValidationError
from Usuarios.util import enviar_correo_otp
from .models import (
    AuthProvider,
    CodigoUnUso,
    PerfilCliente,
    Usuario,
    TipoUsuario,
    PerfilParticularInmuebles,
    PerfilInmobiliaria,
    PerfilEmpleadoInmobiliaria,
    PerfilProfesionalServicios,
)
from django.contrib.auth.password_validation import validate_password
from google.oauth2 import id_token
from google.auth.transport import requests
from Api.settings import GOOGLE_CLIENT_ID
from django.db.transaction import atomic
from django.contrib.auth import authenticate
from Planes.models import PlanInmuebles, PlanPrestamos
from drf_extra_fields.fields import Base64ImageField

from Prestamos.models import PerfilAgenteHipotecario


class OnlyMessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class CodigoUnUsoSerializer(serializers.ModelSerializer):
    message = serializers.CharField(read_only=True)

    class Meta:
        model = CodigoUnUso
        fields = ["codigo", "message"]


class TipoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUsuario
        fields = ["id", "nombre"]


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class RegistrarUsuarioSerializer(serializers.ModelSerializer):
    tipo_usuario = TipoUsuarioSerializer(many=True, read_only=True)
    id_tipo_usuario = serializers.PrimaryKeyRelatedField(
        queryset=TipoUsuario.objects.all(), write_only=True, source="tipo_usuario"
    )
    confirm_password = serializers.CharField(write_only=True)
    tokens = TokenSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "password",
            "confirm_password",
            "nombres",
            "apellidos",
            "is_verified",
            "id_tipo_usuario",
            "tipo_usuario",
            "tokens",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_verified": {"read_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        validate_password(attrs["password"])
        return attrs

    @atomic
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        tipo_usuario = validated_data.pop("tipo_usuario")
        provider = AuthProvider.objects.get(nombre="email")
        usuario = Usuario.objects.create(
            is_staff=False,
            is_superuser=False,
            is_verified=False,
            **validated_data,
        )
        enviar_correo_otp(usuario)
        usuario.set_password(validated_data["password"])
        usuario.provider.add(provider)
        usuario.tipo_usuario.add(tipo_usuario)
        usuario.save()
        return usuario


class PerfilClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilCliente
        fields = [
            "telefono",
        ]


class UsuarioClienteSerializer(serializers.ModelSerializer):
    perfil_cliente = PerfilClienteSerializer()
    tipo_usuario = TipoUsuarioSerializer(many=True, read_only=True)
    tokens = TokenSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "dni",
            "is_verified",
            "tipo_usuario",
            "perfil_cliente",
            "tokens",
        ]
        read_only_fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "is_verified",
            "tipo_usuario",
        ]

    @atomic
    def create(self, validated_data):
        request = self.context.get("request")
        if request is None or not hasattr(request, "user"):
            raise ValidationError("No se ha iniciado sesión")
        usuario: Usuario = request.user
        if hasattr(usuario, "perfil_cliente"):
            raise ValidationError("Ya tienes un perfil de cliente")
        dni = validated_data.pop("dni")
        plan_inmuebles = PlanInmuebles.objects.get(nombre="Plan Cliente")
        plan_prestamos = PlanPrestamos.objects.get(nombre="Plan Cliente")
        tipo_usuario = TipoUsuario.objects.get(nombre="Cliente")
        usuario.dni = dni
        usuario.tipo_usuario.add(tipo_usuario)
        perfil_data = validated_data.pop("perfil_cliente")
        PerfilCliente.objects.create(
            usuario=usuario,
            plan_inmuebles=plan_inmuebles,
            plan_prestamos=plan_prestamos,
            **perfil_data,
        )
        usuario.save()
        return usuario

    @atomic
    def update(self, instance, validated_data):
        print(validated_data)
        usuario: Usuario = instance
        if not hasattr(usuario, "perfil_cliente"):
            raise ValidationError("No tienes un perfil de cliente")
        dni = validated_data.pop("dni")
        plan_inmuebles = PlanInmuebles.objects.get(nombre="Plan Cliente")
        plan_prestamos = PlanPrestamos.objects.get(nombre="Plan Cliente")
        usuario.dni = dni
        perfil_data = validated_data.pop("perfil_cliente")
        perfil_cliente = PerfilCliente.objects.get(usuario=usuario)
        perfil_cliente.plan_inmuebles = plan_inmuebles
        perfil_cliente.plan_prestamos = plan_prestamos
        perfil_cliente.telefono = perfil_data.get("telefono")
        perfil_cliente.save()
        usuario.save()
        perfil_cliente.refresh_from_db()
        return usuario


class PerfilParticularInmueblesSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(
        required=False,
        allow_null=True,
    )
    banner = Base64ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = PerfilParticularInmuebles
        fields = [
            "avatar",
            "banner",
            "telefono",
            "plan",
        ]


class UsuarioParticularInmueblesSerializer(serializers.ModelSerializer):
    perfil_particular = PerfilParticularInmueblesSerializer()
    tokens = TokenSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "dni",
            "is_verified",
            "tipo_usuario",
            "perfil_particular",
            "tokens",
        ]
        read_only_fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "is_verified",
            "tipo_usuario",
        ]

    @atomic
    def create(self, validated_data):
        request = self.context.get("request")
        if request is None or not hasattr(request, "user"):
            raise ValidationError("No se ha iniciado sesión")
        usuario: Usuario = request.user
        if hasattr(usuario, "perfil_cliente"):
            raise ValidationError("Ya tienes este perfil")
        dni = validated_data.pop("dni")
        usuario.dni = dni
        perfil_data = validated_data.pop("perfil_particular")
        PerfilParticularInmuebles.objects.create(
            usuario=usuario,
            **perfil_data,
        )
        usuario.save()
        PerfilParticularInmuebles.objects.update(
            usuario=usuario,
        )
        return usuario

    @atomic
    def update(self, instance: Usuario, validated_data):
        instance.email = validated_data.get("email")
        instance.nombres = validated_data.get("nombres")
        instance.apellidos = validated_data.get("apellidos")
        instance.save()
        perfil = PerfilParticularInmuebles.objects.get(usuario=instance)
        perfil_data = validated_data.get("perfil_particular", None)
        if perfil_data is not None:
            if "plan" in perfil_data:
                perfil.plan = perfil_data.get("plan")
            if "telefono" in perfil_data:
                perfil.telefono = perfil_data.get("telefono")
            if "avatar" in perfil_data:
                perfil.avatar = perfil_data.get("avatar")
            if "banner" in perfil_data:
                perfil.banner = perfil_data.get("banner")
            perfil.save()
        return instance


class PerfilInmobiliariaSerializer(serializers.ModelSerializer):

    avatar = Base64ImageField(
        required=False,
    )

    banner = Base64ImageField(
        required=False,
    )

    class Meta:
        model = PerfilInmobiliaria
        fields = [
            "avatar",
            "banner",
            "razon_social",
            "ruc",
            "telefono",
            "aprobada",
            "plan",
        ]

        extra_kwargs = {
            "aprobada": {"read_only": True},
            "razon_social": {"required": False},
            "ruc": {"required": False},
        }

    def validate_razon_social(self, value):
        if self.context["request"]._request.method == "POST":
            if self.Meta.model.objects.filter(razon_social=value).exists():
                raise ValidationError("Esta razon social ya esta registrada")
        return value

    def validate_ruc(self, value):
        if self.context["request"]._request.method == "POST":
            if self.Meta.model.objects.filter(ruc=value).exists():
                raise ValidationError("Este ruc ya esta registrado")
        return value


class UsuarioInmobiliariaSerializer(serializers.ModelSerializer):
    perfil_inmobiliaria = PerfilInmobiliariaSerializer()
    tokens = TokenSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "dni",
            "is_verified",
            "tipo_usuario",
            "perfil_inmobiliaria",
            "tokens",
        ]
        read_only_fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "is_verified",
            "tipo_usuario",
        ]

    @atomic
    def create(self, validated_data):
        request = self.context.get("request")
        if request is None or not hasattr(request, "user"):
            raise ValidationError("No se ha iniciado sesión")
        usuario: Usuario = request.user
        if hasattr(usuario, "perfil_cliente"):
            raise ValidationError("Ya tienes este perfil")
        dni = validated_data.pop("dni")

        usuario.dni = dni
        perfil_data = validated_data.pop("perfil_inmobiliaria")
        perfil = PerfilInmobiliaria.objects.create(
            usuario=usuario,
            **perfil_data,
        )
        usuario.save()
        return usuario

    @atomic
    def update(self, instance: Usuario, validated_data):
        print(validated_data)
        instance.email = validated_data.get("email", instance.email)
        instance.nombres = validated_data.get("nombres", instance.nombres)
        instance.apellidos = validated_data.get("apellidos", instance.apellidos)

        instance.save()
        perfil = PerfilInmobiliaria.objects.get(usuario=instance)
        perfil_data = validated_data.get("perfil_inmobiliaria", None)
        if perfil_data is None:
            return instance
        perfil.telefono = perfil_data.get("telefono", perfil.telefono)
        perfil.avatar.delete(save=True)
        perfil.banner.delete(save=True)
        if "avatar" in perfil_data:
            perfil.avatar = perfil_data.get("avatar")
        if "banner" in perfil_data:
            perfil.banner = perfil_data.get("banner")
        perfil.save()
        return instance


class PerfilEmpleadoInmobiliariaSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(
        required=False,
        allow_null=True,
    )
    inmobiliaria = PerfilInmobiliariaSerializer(
        read_only=True,
    )

    inmobiliaria_id = serializers.CharField(
        source="inmobiliaria.usuario.id", read_only=True
    )

    class Meta:
        model = PerfilEmpleadoInmobiliaria
        fields = [
            "inmobiliaria_id",
            "avatar",
            "telefono",
            "inmobiliaria",
        ]


class UsuarioEmpleadoInmobiliariaSerializer(serializers.ModelSerializer):
    perfil_empleado = PerfilEmpleadoInmobiliariaSerializer()

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "password",
            "nombres",
            "apellidos",
            "dni",
            "perfil_empleado",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }

    @atomic
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if password is None:
            raise ValidationError("Se necesita una contraseña")
        request = self.context.get("request")
        if request is None or not hasattr(request, "user"):
            raise ValidationError("No se ha iniciado sesión")
        inmobiliaria = request.user.perfil_inmobiliaria
        perfil_data = validated_data.pop("perfil_empleado")
        tipo_usuario = TipoUsuario.objects.get(nombre="Empleado Inmobiliaria")

        usuario = Usuario.objects.create(
            **validated_data,
        )
        usuario.set_password(password)
        usuario.tipo_usuario.add(tipo_usuario)

        PerfilEmpleadoInmobiliaria.objects.create(
            usuario=usuario,
            inmobiliaria=inmobiliaria,
            **perfil_data,
        )

        usuario.is_verified = True

        provider = AuthProvider.objects.get(nombre="email")
        usuario.provider.add(provider)

        usuario.save()
        return usuario

    @atomic
    def update(self, instance: Usuario, validated_data):
        instance.email = validated_data.get("email")
        instance.nombres = validated_data.get("nombres")
        instance.apellidos = validated_data.get("apellidos")
        instance.dni = validated_data.get("dni")
        instance.save()
        perfil = PerfilEmpleadoInmobiliaria.objects.get(usuario=instance)
        perfil_data = validated_data.get("perfil_empleado", None)
        perfil.avatar.delete(save=True)
        if perfil_data is None:
            return instance
        perfil.telefono = perfil_data.get("telefono", perfil.telefono)
        if "avatar" in perfil_data:
            perfil.avatar = perfil_data.get("avatar")
        perfil.save()

        return instance


class PerfilAgenteHipotecarioSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(
        required=False,
        allow_null=True,
    )
    entidad_nombre = serializers.StringRelatedField(
        source="entidad.nombre", read_only=True
    )

    class Meta:
        model = PerfilAgenteHipotecario
        fields = ["avatar", "telefono", "plan", "entidad", "entidad_nombre"]
        extra_kwargs = {
            "entidad": {"write_only": True},
        }


class UsuarioAgenteHipotecarioSerializer(serializers.ModelSerializer):
    perfil_agente_hipotecario = PerfilAgenteHipotecarioSerializer(
        required=False,
    )
    tokens = TokenSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "dni",
            "is_verified",
            "tipo_usuario",
            "perfil_agente_hipotecario",
            "tokens",
        ]
        read_only_fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "is_verified",
            "tipo_usuario",
        ]

    @atomic
    def create(self, validated_data):
        print("##########")
        print(validated_data)
        print("##########")
        request = self.context.get("request")
        if request is None or not hasattr(request, "user"):
            raise ValidationError("No se ha iniciado sesión")
        usuario: Usuario = request.user
        if hasattr(usuario, "perfil_cliente"):
            raise ValidationError("Ya tienes este perfil")
        dni = validated_data.pop("dni")

        usuario.dni = dni
        perfil_data = validated_data.pop("perfil_agente_hipotecario")
        PerfilAgenteHipotecario.objects.create(
            usuario=usuario,
            **perfil_data,
        )
        usuario.save()
        return usuario


class PerfilProfesionalServiciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilProfesionalServicios
        fields = ["telefono", "plan"]


class UsuarioProfesionalServiciosSerializer(serializers.ModelSerializer):
    perfil_profesional = PerfilProfesionalServiciosSerializer()
    tokens = TokenSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "dni",
            "is_verified",
            "tipo_usuario",
            "perfil_profesional",
            "tokens",
        ]
        read_only_fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "is_verified",
            "tipo_usuario",
        ]

    @atomic
    def create(self, validated_data):
        request = self.context.get("request")
        if request is None or not hasattr(request, "user"):
            raise ValidationError("No se ha iniciado sesión")
        usuario: Usuario = request.user
        if hasattr(usuario, "perfil_cliente"):
            raise ValidationError("Ya tienes este perfil")
        dni = validated_data.pop("dni")

        usuario.dni = dni
        perfil_data = validated_data.pop("perfil_profesional")
        PerfilProfesionalServicios.objects.create(
            usuario=usuario,
            **perfil_data,
        )
        usuario.save()
        return usuario


class GoogleAuthSerializer(serializers.ModelSerializer):
    credential = serializers.CharField(write_only=True)
    tipo_usuario = TipoUsuarioSerializer(many=True, read_only=True)
    id_tipo_usuario = serializers.PrimaryKeyRelatedField(
        queryset=TipoUsuario.objects.all(),
        write_only=True,
        source="tipo_usuario",
        required=False,
    )
    perfil_cliente = PerfilClienteSerializer(required=False, allow_null=True)
    perfil_particular = PerfilParticularInmueblesSerializer(
        required=False, allow_null=True
    )
    perfil_inmobiliaria = PerfilInmobiliariaSerializer(required=False, allow_null=True)
    perfil_agente_hipotecario = PerfilAgenteHipotecarioSerializer(
        required=False, allow_null=True
    )
    perfil_profesional = PerfilProfesionalServiciosSerializer(
        required=False, allow_null=True
    )
    tokens = TokenSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "credential",
            "email",
            "nombres",
            "apellidos",
            "is_verified",
            "id_tipo_usuario",
            "tipo_usuario",
            "perfil_cliente",
            "perfil_particular",
            "perfil_inmobiliaria",
            "perfil_agente_hipotecario",
            "perfil_profesional",
            "tokens",
        ]
        extra_kwargs = {
            "email": {"read_only": True},
            "nombres": {"read_only": True},
            "apellidos": {"read_only": True},
            "is_verified": {"read_only": True},
            "tokens": {"read_only": True},
        }

    def validate(self, attrs):
        print("####################")
        print(attrs)
        print("Estamos validando")
        credential = attrs.get("credential")
        try:
            google_user_data = id_token.verify_oauth2_token(
                credential, requests.Request()
            )
            if not google_user_data.get("aud") == GOOGLE_CLIENT_ID:
                raise ValidationError("Token inválido")
            if not google_user_data.get("email"):
                raise ValidationError("El token no contiene un email válido")
            attrs["google_user_data"] = google_user_data
        except ValueError as e:
            raise ValidationError(f"Token inválido: {e}")
        return attrs

    @atomic
    def create(self, validated_data):
        print("####################")
        print(validated_data)
        print("Estamos logeando")
        credential = validated_data.get("credential")
        print("Estamos logeando 1")
        google_user_data = id_token.verify_oauth2_token(credential, requests.Request())
        print("Estamos logeando 2")
        email = google_user_data.get("email")
        print("Estamos logeando 3 ")
        nombres = google_user_data.get("given_name")
        print("Estamos logeando 4")
        apellidos = google_user_data.get("family_name", "")
        print("Estamos logeando 5")
        tipo_usuario = validated_data.pop("tipo_usuario", None)
        print("Estamos logeando 6")
        if tipo_usuario is None:
            print("Estamos logeando 7")
            try:
                print("Estamos logeando 8")
                usuario = Usuario.objects.get(email=email)
                return usuario
            except Usuario.DoesNotExist:
                raise ValidationError("Este email no está registrado")

        print("Estamos logeando 7")
        usuario, _ = Usuario.objects.get_or_create(
            email=email,
            defaults={
                "nombres": nombres,
                "apellidos": apellidos,
            },
        )
        usuario.tipo_usuario.add(tipo_usuario)
        print("Estamos logeando 8")
        provider = AuthProvider.objects.get(nombre="google")
        usuario.provider.add(provider)
        usuario.is_verified = True
        usuario.save()
        return usuario


class LoginEmailSerializer(serializers.ModelSerializer):
    tipo_usuario = TipoUsuarioSerializer(many=True, read_only=True)
    tokens = TokenSerializer(read_only=True)
    email = serializers.EmailField()
    perfil_cliente = PerfilClienteSerializer(required=False, allow_null=True)
    perfil_particular = PerfilParticularInmueblesSerializer(
        required=False, allow_null=True
    )
    perfil_inmobiliaria = PerfilInmobiliariaSerializer(required=False, allow_null=True)
    perfil_agente_hipotecario = PerfilAgenteHipotecarioSerializer(
        required=False, allow_null=True
    )
    perfil_profesional = PerfilProfesionalServiciosSerializer(
        required=False, allow_null=True
    )
    perfil_empleado = PerfilEmpleadoInmobiliariaSerializer(
        required=False, allow_null=True
    )

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "password",
            "nombres",
            "apellidos",
            "is_verified",
            "tipo_usuario",
            "perfil_cliente",
            "perfil_particular",
            "perfil_inmobiliaria",
            "perfil_agente_hipotecario",
            "perfil_profesional",
            "perfil_empleado",
            "tokens",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "nombres": {"read_only": True},
            "apellidos": {"read_only": True},
            "is_verified": {"read_only": True},
            "tipo_usuario": {"read_only": True},
            "tokens": {"read_only": True},
        }

    def create(self, validated_data):
        usuario = authenticate(
            email=validated_data.get("email"), password=validated_data.get("password")
        )
        if usuario is None:
            raise ValidationError("Credenciales inválidas")
        return usuario


class PerfilVistaSerializer(serializers.ModelSerializer):
    perfil_particular = PerfilParticularInmueblesSerializer(allow_null=True)
    perfil_inmobiliaria = PerfilInmobiliariaSerializer(allow_null=True)
    perfil_empleado = PerfilEmpleadoInmobiliariaSerializer(allow_null=True)
    tipo_usuario = TipoUsuarioSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "nombres",
            "apellidos",
            "perfil_particular",
            "perfil_inmobiliaria",
            "perfil_empleado",
            "tipo_usuario",
        ]
