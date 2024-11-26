from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from Inmuebles.filters import InmuebleFilterSet
from .models import (
    Caracteristica,
    Favorito,
    TipoAntiguedad,
    TipoInmueble,
    SubTipoInmueble,
    EstadoInmueble,
    TipoOperacion,
    Inmueble,
)
from .serializers import (
    CaracteristicaSerializer,
    FavoritoSerializer,
    InmueblePreviewSerializer,
    TipoAntiguedadSerializer,
    TipoInmuebleSerializer,
    SubTipoInmuebleSerializer,
    EstadoInmuebleSerializer,
    TipoOperacionSerializer,
    InmuebleListSerializer,
    InmuebleDetalleSerializer,
    VisitaSerializer,
    ContactoDueñoSerializer,
    CRUDListaSerializer,
    PublicarInmuebleSerializer,
    InmuebleCrudSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
)
from Usuarios.util import enviar_correo
from rest_framework.permissions import IsAuthenticated


class CaracteristicaViewSet(ModelViewSet):
    queryset = Caracteristica.objects.all()
    serializer_class = CaracteristicaSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    http_method_names = ["get"]
    search_fields = ["nombre", "descripcion"]


class TipoAntiguedadViewSet(ModelViewSet):
    queryset = TipoAntiguedad.objects.all()
    serializer_class = TipoAntiguedadSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    http_method_names = ["get"]
    search_fields = ["nombre", "descripcion"]


class TipoInmuebleViewSet(ModelViewSet):
    queryset = TipoInmueble.objects.all()
    serializer_class = TipoInmuebleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    http_method_names = ["get"]
    search_fields = ["nombre", "descripcion"]


class SubTipoInmuebleViewSet(ModelViewSet):
    queryset = SubTipoInmueble.objects.all()
    serializer_class = SubTipoInmuebleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["tipo_inmueble"]
    http_method_names = ["get"]
    search_fields = ["nombre", "descripcion", "tipo_Inmueble__nombre"]


class EstadoInmuebleViewSet(ModelViewSet):
    queryset = EstadoInmueble.objects.all()
    serializer_class = EstadoInmuebleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    http_method_names = ["get"]
    search_fields = ["nombre", "descripcion"]


class TipoOperacionViewSet(ModelViewSet):
    queryset = TipoOperacion.objects.all()
    serializer_class = TipoOperacionSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    http_method_names = ["get"]
    search_fields = ["nombre", "descripcion"]


class InmuebleListaViewSet(ListModelMixin, GenericViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = InmuebleFilterSet
    lookup_field = "slug"
    search_fields = [
        "slug",
        "titulo",
        "estado__nombre",
        "descripcion",
        "tipo_operacion__nombre",
        "tipo_antiguedad__nombre",
        "subtipo_inmueble__nombre",
        "caracteristicas__nombre",
        "ubicacion__distrito__nombre",
        "ubicacion__distrito__provincia__nombre",
        "ubicacion__distrito__provincia__departamento__nombre",
    ]
    ordering_fields = [
        "fecha_actualizacion",
        "precio_soles",
        "precio_dolares",
    ]
    ordering = ["-fecha_actualizacion"]

    def get_queryset(self):
        return Inmueble.objects.filter(
            estado__nombre="Publicado",
        )


class InmuebleDetalleViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleDetalleSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Inmueble.objects.filter(
            estado__nombre="Publicado",
        )


class InmueblePreViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmueblePreviewSerializer

    def get_queryset(self):
        return Inmueble.objects.filter(
            dueño=self.request.user,
        )


# TODO: vistas para imagenes, planos y ubicaciones
class ContactoDueñoView(GenericAPIView):
    serializer_class = ContactoDueñoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        print(data)

        try:
            inmueble = Inmueble.objects.get(slug=data["slug"])
            enviar_correo(
                asunto="Contacto de interesado",
                mensaje=f"El interesado {data['nombre']} está interesado en su inmueble {inmueble.titulo}. Su correo es {data['email']}, su telefono es {data['telefono']} y su mensaje es {data['mensaje']}",
                destinatario=inmueble.dueño.email,
            )
            return Response(
                {"message": "Correo enviado correctamente"},
                status=status.HTTP_201_CREATED,
            )
        except Inmueble.DoesNotExist:
            return Response(
                {"message": "Inmueble no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )


class CRUDListaViewSet(ListModelMixin, GenericViewSet, DestroyModelMixin):
    queryset = Inmueble.objects.all()
    serializer_class = CRUDListaSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "slug",
        "titulo",
        "estado__nombre",
        "descripcion",
        "tipo_operacion__nombre",
        "tipo_antiguedad__nombre",
        "subtipo_inmueble__nombre",
        "caracteristicas__nombre",
        "ubicacion__distrito__nombre",
        "ubicacion__distrito__provincia__nombre",
        "ubicacion__distrito__provincia__departamento__nombre",
    ]
    ordering_fields = [
        "fecha_actualizacion",
        "precio_soles",
        "precio_dolares",
    ]
    # ordering = ["-fecha_actualizacion"]
    http_method_names = ["get", "delete"]

    def get_queryset(self):
        return Inmueble.objects.filter(
            dueño=self.request.user,
        )


class PublicarInmuebleView(UpdateModelMixin, GenericViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = PublicarInmuebleSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def get_queryset(self):
        return Inmueble.objects.filter(
            dueño=self.request.user,
        )


class CrudInmuebleViewSet(
    UpdateModelMixin, CreateModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleCrudSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        return Inmueble.objects.filter(
            dueño=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(dueño=self.request.user)


class FavoritoViewSet(ModelViewSet):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["inmueble__slug"]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return Favorito.objects.filter(
            usuario=self.request.user,
        )


class VisitaViewSet(UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    lookup_field = "slug"
