from Usuarios.util import UserViewSet
from .serializers import (
    OnlyMessageSerializer,
    TipoUsuarioSerializer,
    RegistrarUsuarioSerializer,
    LoginEmailSerializer,
    GoogleAuthSerializer,
    UsuarioClienteSerializer,
    UsuarioParticularInmueblesSerializer,
    UsuarioInmobiliariaSerializer,
    UsuarioEmpleadoInmobiliariaSerializer,
    UsuarioAgentePrestamosSerializer,
    UsuarioProfesionalServiciosSerializer,
)
from .models import Usuario, TipoUsuario
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

    def get_object(self):
        pass

    def get_queryset(self):
        return Usuario.objects.filter(id=self.request.user.id)


class PerfilParticularInmueblesView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioParticularInmueblesSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(id=self.request.user.id)


class PerfilInmobiliariaView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioInmobiliariaSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(id=self.request.user.id)


class PerfilEmpleadoInmobiliariaView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioEmpleadoInmobiliariaSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(
            perfil_inmobiliaria__id=self.request.user.perfil_inmobiliaria.id
        )


class PerfilAgentePrestamosView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioAgentePrestamosSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(
            perfil_inmobiliaria__id=self.request.user.perfil_inmobiliaria.id
        )


class PerfilProfesionalServiciosView(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioProfesionalServiciosSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(
            perfil_inmobiliaria__id=self.request.user.perfil_inmobiliaria.id
        )
