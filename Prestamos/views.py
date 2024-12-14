from rest_framework.viewsets import ModelViewSet
from Prestamos.permisions import IsAgenteOrPrestatario
from Usuarios.models import Usuario
from .models import (
    Documento,
    EntidadBancaria,
    EvaluacionCrediticia,
    PerfilPrestatarioPrefab,
    EtapaEvaluacion,
    PreguntaPerfil,
)
from .serializers import (
    EntidadBancariaSerializer,
    EvaluacionCrediticiaListSerializer,
    NuevoClienteDetalleSerializer,
    PerfilPrestatarioPrefabListSerializer,
    PerfilPrestatarioPrefabSerializer,
    EtapaEvalucionSerializer,
    PreguntaPerfilSerializer,
    NuevosClientesListSerializer,
)

from .serializerEvaluacion import EvaluacionSolicitudSerializer

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


class NuevosClientesListModelViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = NuevosClientesListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get_queryset(self):
        return super().get_queryset().filter(perfil_prestatario__isnull=False)


class NuevosClientesDetalleModelViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = NuevoClienteDetalleSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put"]

    def get_queryset(self):
        return super().get_queryset().filter(perfil_prestatario__isnull=False)


class EvaluacionCrediticiaListViewSet(ModelViewSet):
    queryset = EvaluacionCrediticia.objects.all()
    serializer_class = EvaluacionCrediticiaListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "delete"]

    def get_queryset(self):
        if not hasattr(self.request.user, "perfil_agente_hipotecario"):
            return super().get_queryset().none()
        return (
            super()
            .get_queryset()
            .filter(agente=self.request.user.perfil_agente_hipotecario)
        )


from django.db.models import Prefetch


class EvaluacionSolicitudView(ModelViewSet):
    queryset = EvaluacionCrediticia.objects.prefetch_related(
        Prefetch(
            "documentos", queryset=Documento.objects.filter(etapa__nombre="Solicitud")
        )
    )

    serializer_class = EvaluacionSolicitudSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put"]

    def get_queryset(self):
        if hasattr(self.request.user, "perfil_agente_hipotecario"):
            return (
                super()
                .get_queryset()
                .filter(agente=self.request.user.perfil_agente_hipotecario)
            )
        elif hasattr(self.request.user, "perfil_prestatario"):
            return (
                super()
                .get_queryset()
                .filter(prestatario=self.request.user.perfil_prestatario)
            )
        else:
            return super().get_queryset().none()
