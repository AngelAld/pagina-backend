from .serializers import (
    RegistrarUsuarioSerializer,
    TipoUsuarioSerializer,
    GoogleAuthSerializer,
    UsuarioClienteSerializer,
    LoginEmailSerializer,
    OnlyMessageSerializer,
)
from .models import Usuario, TipoUsuario
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)


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


class ListaTiposUsuariosView(ModelViewSet):
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get"]


class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlyMessageSerializer

    def get(self, request):
        return Response(
            {
                "message": f"Sesión iniciada como {request.user.email}",
            }
        )


class PerfilClienteView(
    GenericViewSet,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioClienteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Usuario.objects.filter(id=self.request.user.id)
