from rest_framework.viewsets import ModelViewSet
from .models import EntidadBancaria
from .serializers import EntidadBancariaSerializer
from rest_framework.permissions import AllowAny


class EntidadBancariaViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = EntidadBancaria.objects.all()
    serializer_class = EntidadBancariaSerializer
    http_method_names = ["get", "post", "put", "delete"]
