from .models import EntidadBancaria
from rest_framework.serializers import ModelSerializer


class EntidadBancariaSerializer(ModelSerializer):
    class Meta:
        model = EntidadBancaria
        fields = [
            "id",
            "nombre",
        ]
