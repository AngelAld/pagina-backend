from rest_framework import serializers
from rest_framework.serializers import ValidationError
from Usuarios.util import enviar_correo_otp
from .models import AuthProvider, PerfilCliente, Usuario, TipoUsuario
from django.contrib.auth.password_validation import validate_password
from google.oauth2 import id_token
from google.auth.transport import requests
from Api.settings import GOOGLE_CLIENT_ID
from django.contrib.auth import login
from django.db.transaction import atomic
from django.contrib.auth import authenticate


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


class GoogleAuthSerializer(serializers.ModelSerializer):
    credential = serializers.CharField(write_only=True)
    tipo_usuario = TipoUsuarioSerializer(many=True, read_only=True)
    id_tipo_usuario = serializers.PrimaryKeyRelatedField(
        queryset=TipoUsuario.objects.all(), write_only=True, source="tipo_usuario"
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
        tipo_usuario = validated_data.pop("tipo_usuario")
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


class PerfilClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilCliente
        fields = [
            "telefono",
        ]


class UsuarioClienteSerializer(serializers.ModelSerializer):
    perfil_cliente = PerfilClienteSerializer()

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
        if hasattr(usuario, "perfil_cliente"):
            raise ValidationError("Ya tienes un perfil de cliente")
        return attrs

    @atomic
    def create(self, validated_data):
        usuario: Usuario = self.context.get("request").user
        dni = validated_data.pop("dni")
        usuario.dni = dni
        perfil_data = validated_data.pop("perfil_cliente")
        perfil = PerfilCliente.objects.create(usuario=usuario, **perfil_data)
        usuario.save()
        return perfil


class OnlyMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
