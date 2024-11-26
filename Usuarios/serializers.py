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
    PerfilAgentePrestamos,
    PerfilEmpleadoInmobiliaria,
    PerfilProfesionalServicios,
)
from django.contrib.auth.password_validation import validate_password
from google.oauth2 import id_token
from google.auth.transport import requests
from Api.settings import GOOGLE_CLIENT_ID
from django.contrib.auth import login
from django.db.transaction import atomic
from django.contrib.auth import authenticate
from Planes.models import PlanInmuebles, PlanPrestamos
from drf_extra_fields.fields import Base64ImageField


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

    def validate(self, attrs):
        usuario: Usuario = self.context.get("request").user
        if usuario is None:
            raise ValidationError("No se ha iniciado sesión")
        return attrs

    @atomic
    def create(self, validated_data):
        usuario: Usuario = self.context.get("request").user
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
    avatar = Base64ImageField(required=False)

    class Meta:
        model = PerfilParticularInmuebles
        fields = [
            "avatar",
            "telefono",
            "plan",
        ]
        extra_kwargs = {
            "avatar": {"required": False},
        }


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

    def validate(self, attrs):
        usuario: Usuario = self.context.get("request").user
        if usuario is None:
            raise ValidationError("No se ha iniciado sesión")
        if hasattr(usuario, "perfil_particular"):
            raise ValidationError("Ya tienes un perfil de inmuebles")
        return attrs

    @atomic
    def create(self, validated_data):
        usuario: Usuario = self.context.get("request").user
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


class PerfilInmobiliariaSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = PerfilInmobiliaria
        fields = [
            "avatar",
            "razon_social",
            "ruc",
            "telefono",
            "aprobada",
            "plan",
        ]

        read_only_fields = [
            "aprobada",
        ]


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

    def validate(self, attrs):
        usuario: Usuario = self.context.get("request").user
        if usuario is None:
            raise ValidationError("No se ha iniciado sesión")
        if hasattr(usuario, "perfil_inmobiliaria"):
            raise ValidationError("Ya tienes un perfil de inmobiliaria")
        return attrs

    @atomic
    def create(self, validated_data):
        usuario: Usuario = self.context.get("request").user
        dni = validated_data.pop("dni")

        usuario.dni = dni
        perfil_data = validated_data.pop("perfil_inmobiliaria")
        perfil = PerfilInmobiliaria.objects.create(
            usuario=usuario,
            **perfil_data,
        )
        usuario.save()
        return usuario


class PerfilEmpleadoInmobiliariaSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(
        required=False,
        write_only=True,
    )
    avatar_url = serializers.StringRelatedField(
        source="avatar", read_only=True, allow_null=True
    )

    class Meta:
        model = PerfilEmpleadoInmobiliaria
        fields = [
            "avatar",
            "avatar_url",
            "telefono",
        ]


class UsuarioEmpleadoInmobiliariaSerializer(serializers.ModelSerializer):
    perfil_empleado = PerfilEmpleadoInmobiliariaSerializer(
        required=False,
    )

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
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        usuario: Usuario = self.context.get("request").user
        if not hasattr(usuario, "perfil_inmobiliaria"):
            raise ValidationError("No tienes un perfil de inmobiliaria")
        return attrs

    @atomic
    def create(self, validated_data):
        inmobiliaria = self.context.get("request").user.perfil_inmobiliaria
        perfil_data = validated_data.pop("perfil_empleado")
        tipo_usuario = TipoUsuario.objects.get(nombre="Empleado Inmobiliaria")
        password = validated_data.pop("password")
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
        if perfil_data is not None:
            perfil.telefono = perfil_data.get("telefono")
            if "avatar" in perfil_data:
                perfil.avatar = perfil_data.get("avatar")
            perfil.save()
        return instance


class PerfilAgentePrestamosSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = PerfilAgentePrestamos
        fields = ["avatar", "telefono", "plan", "entidad"]


class UsuarioAgentePrestamosSerializer(serializers.ModelSerializer):
    perfil_agente = PerfilAgentePrestamosSerializer()
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
            "perfil_agente",
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

    def validate(self, attrs):
        usuario: Usuario = self.context.get("request").user
        if usuario is None:
            raise ValidationError("No se ha iniciado sesión")
        if hasattr(usuario, "perfil_agente"):
            raise ValidationError("Ya tienes un perfil de agente de prestamos")
        return attrs

    @atomic
    def create(self, validated_data):
        usuario: Usuario = self.context.get("request").user
        dni = validated_data.pop("dni")

        usuario.dni = dni
        perfil_data = validated_data.pop("perfil_agente")
        PerfilAgentePrestamos.objects.create(
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

    def validate(self, attrs):
        usuario: Usuario = self.context.get("request").user
        if usuario is None:
            raise ValidationError("No se ha iniciado sesión")
        if hasattr(usuario, "perfil_profesional"):
            raise ValidationError("Ya tienes un perfil de profesional de servicios")
        return attrs

    @atomic
    def create(self, validated_data):
        usuario: Usuario = self.context.get("request").user
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
    perfil_agente = PerfilAgentePrestamosSerializer(required=False, allow_null=True)
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
            "perfil_agente",
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
        credential = validated_data.get("credential")
        request = self.context.get("request")
        google_user_data = id_token.verify_oauth2_token(credential, requests.Request())
        tipo_usuario = validated_data.pop("tipo_usuario", None)
        email = google_user_data.get("email")
        nombres = google_user_data.get("given_name")
        apellidos = google_user_data.get("family_name")

        usuario, created = Usuario.objects.get_or_create(
            email=email,
            defaults={
                "nombres": nombres,
                "apellidos": apellidos,
            },
        )
        if created:
            if not tipo_usuario:
                tipo_usuario = TipoUsuario.objects.get(nombre="Cliente")
            usuario.tipo_usuario.add(tipo_usuario)
        provider = AuthProvider.objects.get(nombre="google")
        usuario.provider.add(provider)
        usuario.is_verified = True
        usuario.save()
        login(request, usuario)
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
    perfil_agente = PerfilAgentePrestamosSerializer(required=False, allow_null=True)
    perfil_profesional = PerfilProfesionalServiciosSerializer(
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
            "perfil_agente",
            "perfil_profesional",
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

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        usuario = authenticate(email=email, password=password)
        if usuario is None:
            raise ValidationError("Credenciales inválidas")
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        usuario = authenticate(
            email=validated_data.get("email"), password=validated_data.get("password")
        )
        login(request, usuario)
        return usuario
