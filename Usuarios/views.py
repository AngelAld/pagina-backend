from Usuarios.util import UserViewSet, enviar_correo_otp
from .serializers import (
    CodigoUnUsoSerializer,
    OnlyMessageSerializer,
    TipoUsuarioSerializer,
    RegistrarUsuarioSerializer,
    LoginEmailSerializer,
    GoogleAuthSerializer,
    UsuarioClienteSerializer,
    UsuarioParticularInmueblesSerializer,
    UsuarioInmobiliariaSerializer,
    UsuarioEmpleadoInmobiliariaSerializer,
    UsuarioAgenteHipotecarioSerializer,
    UsuarioProfesionalServiciosSerializer,
    PerfilVistaSerializer,
)
from .models import CodigoUnUso, Usuario, TipoUsuario
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q


class RegistrarUsuarioView(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = RegistrarUsuarioSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]


class LoginEmailView(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = LoginEmailSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]


class AutenticarUsuarioGoogleView(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = GoogleAuthSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]


class ListaTiposUsuariosView(
    GenericViewSet,
    ListModelMixin,
):
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get"]


class WhoAmIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlyMessageSerializer

    def get(self, request):
        return Response(
            {
                "message": f"Sesión iniciada como {request.user.email}",
            }
        )


class PerfilClienteView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioClienteSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(id=self.request.user.pk)


class PerfilParticularInmueblesView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioParticularInmueblesSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(pk=self.request.user.pk)


class PerfilInmobiliariaView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioInmobiliariaSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(pk=self.request.user.pk)


class PerfilEmpleadoInmobiliariaView(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioEmpleadoInmobiliariaSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]

    def get_queryset(self):
        return Usuario.objects.filter(
            perfil_empleado__inmobiliaria__pk=self.request.user.perfil_inmobiliaria.pk
        )


class PerfilAgenteHipotecarioView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioAgenteHipotecarioSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(
            perfil_inmobiliaria__pk=self.request.user.perfil_inmobiliaria.pk
        )


class PerfilProfesionalServiciosView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioProfesionalServiciosSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(
            perfil_inmobiliaria__pk=self.request.user.perfil_inmobiliaria.pk
        )


class ConfirmarEmailView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CodigoUnUsoSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            codigo = CodigoUnUso.objects.get(codigo=serializer.validated_data["codigo"])
            usuario = codigo.usuario
            if usuario != request.user:
                return Response(
                    {"message": "Codigo no valido"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not usuario.is_verified:
                usuario.is_verified = True
                usuario.save()
                codigo.delete()
                return Response(
                    {"message": "Email confirmado"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Email ya confirmado"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CodigoUnUso.DoesNotExist:
            return Response(
                {"message": "Codigo no valido"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReenviarEmailView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlyMessageSerializer

    def post(self, request):
        usuario = request.user
        if usuario.is_verified:
            return Response(
                {"message": "Email ya confirmado"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        CodigoUnUso.objects.filter(usuario=usuario).delete()
        enviar_correo_otp(usuario)
        return Response(
            {"message": "Codigo enviado"},
            status=status.HTTP_200_OK,
        )


class PerfilVistaView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PerfilVistaSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        return Usuario.objects.filter(
            Q(perfil_inmobiliaria__isnull=False)
            | Q(perfil_empleado__isnull=False)
            | Q(perfil_particular__isnull=False)
        )
