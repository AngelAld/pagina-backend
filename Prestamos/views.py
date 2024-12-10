from rest_framework.viewsets import ModelViewSet
from .models import EntidadBancaria, PerfilPrestatarioPrefab
from .serializers import EntidadBancariaSerializer, PerfilPrestatarioPrefabSerializer
from rest_framework.permissions import AllowAny
from Usuarios.util import UserViewSet, GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class EntidadBancariaViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = EntidadBancaria.objects.all()
    serializer_class = EntidadBancariaSerializer
    http_method_names = ["get", "post", "put", "delete"]


class PerfilPrestatarioPrefabViewSet(ModelViewSet):
    queryset = PerfilPrestatarioPrefab.objects.all()
    serializer_class = PerfilPrestatarioPrefabSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(dueño=self.request.user)
