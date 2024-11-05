from .serializers import RegistrarUsuarioSerializer
from .models import Usuario
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


class RegistrarUsuarioView(CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistrarUsuarioSerializer
    permission_classes = [AllowAny]
