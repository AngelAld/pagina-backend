from rest_framework import serializers
from .models import AuthProvider, Usuario, TipoUsuario
from django.contrib.auth.password_validation import validate_password


class TipoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUsuario
        fields = ["id", "nombre"]


class RegistrarUsuarioSerializer(serializers.ModelSerializer):
    tipo_usuario = TipoUsuarioSerializer()
    confirm_password = serializers.CharField(write_only=True)

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
            "tipo_usuario",
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

    def create(self, validated_data):
        tipo_usuario_data = validated_data.pop("tipo_usuario")
        validated_data.pop("confirm_password")
        tipo_usuario = TipoUsuario.objects.get(**tipo_usuario_data)
        provider = AuthProvider.objects.get(nombre="email")
        usuario = Usuario.objects.create(
            tipo_usuario=tipo_usuario,
            is_staff=False,
            is_superuser=False,
            provider=provider,
            is_verified=False**validated_data,
        )
        usuario.set_password(validated_data["password"])
        usuario.save()
        return usuario
