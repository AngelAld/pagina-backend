from rest_framework.viewsets import ModelViewSet

from Usuarios.models import Usuario
from Usuarios.util import UserViewSet
from .models import (
    EntidadBancaria,
    PerfilPrestatarioPrefab,
    EtapaEvaluacion,
    PreguntaPerfil,
    PerfilPrestatario,
)
from .serializers import (
    EntidadBancariaSerializer,
    PerfilPrestatarioPrefabListSerializer,
    PerfilPrestatarioPrefabSerializer,
    EtapaEvalucionSerializer,
    PerfilPrestatarioUserSerializer,
    PreguntaPerfilSerializer,
    PerfilPrestatarioSerializer,
)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class PreguntaPerfilViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = PreguntaPerfil.objects.all()
    serializer_class = PreguntaPerfilSerializer
    http_method_names = ["get"]


class EtapaEvaluacionViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = EtapaEvaluacion.objects.all()
    serializer_class = EtapaEvalucionSerializer
    http_method_names = ["get"]


class EntidadBancariaViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = EntidadBancaria.objects.all()
    serializer_class = EntidadBancariaSerializer
    http_method_names = ["get", "post", "put", "delete"]


class PerfilPrestatarioPrefabViewSet(ModelViewSet):
    queryset = PerfilPrestatarioPrefab.objects.all()
    serializer_class = PerfilPrestatarioPrefabListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "delete"]

    def get_queryset(self):
        return super().get_queryset().filter(dueño=self.request.user)


class PerfilPrestatarioPrefabDetalleViewSet(ModelViewSet):
    queryset = PerfilPrestatarioPrefab.objects.all()
    serializer_class = PerfilPrestatarioPrefabSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return super().get_queryset().filter(dueño=self.request.user)


class PerfilPrestatarioViewSet(UserViewSet):
    queryset = Usuario.objects.all()
    serializer_class = PerfilPrestatarioUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)
