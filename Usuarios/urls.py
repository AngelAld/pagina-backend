from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WhoAmIView,
    ListaTiposUsuariosView,
    RegistrarUsuarioView,
    LoginEmailView,
    AutenticarUsuarioGoogleView,
    PerfilClienteView,
    PerfilParticularInmueblesView,
    PerfilInmobiliariaView,
    PerfilEmpleadoInmobiliariaView,
    PerfilAgenteHipotecarioView,
    PerfilProfesionalServiciosView,
    ConfirmarEmailView,
    ReenviarEmailView,
    PerfilVistaView,
)
from rest_framework_simplejwt.views import TokenRefreshView

auth = DefaultRouter()
tipos = DefaultRouter()
router = DefaultRouter()
# Auth
auth.register("email", RegistrarUsuarioView, basename="registrar con email")
auth.register("google", AutenticarUsuarioGoogleView, basename="registrar con google")
auth.register("login", LoginEmailView, basename="Iniciar sesión con email")
# Tipos
tipos.register("usuarios", ListaTiposUsuariosView)
router.register("inmobiliaria-empleados", PerfilEmpleadoInmobiliariaView)
router.register("", PerfilVistaView, basename="perfil")
perfiles = [
    path("cliente/", PerfilClienteView.as_view(), name="perfil cliente"),
    path(
        "particular-inmuebles/",
        PerfilParticularInmueblesView.as_view(),
        name="perfil particular inmuebles",
    ),
    path("inmobiliaria/", PerfilInmobiliariaView.as_view(), name="perfil inmobiliaria"),
    path(
        "agente-hipotecario/",
        PerfilAgenteHipotecarioView.as_view(),
        name="perfil agente prestamos",
    ),
    path(
        "profesional-servicios/",
        PerfilProfesionalServiciosView.as_view(),
        name="perfil profesional servicios",
    ),
]


urlpatterns = [
    path("whoami/", WhoAmIView.as_view(), name="whoami"),
    path("auth/", include(auth.urls)),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("tipos/", include(tipos.urls)),
    path("perfil/", include(perfiles)),
    path("perfil/", include(router.urls)),
    path("auth/confirmar-email/", ConfirmarEmailView.as_view(), name="confirmar email"),
    path(
        "auth/reenviar-email-de-verificacion/",
        ReenviarEmailView.as_view(),
        name="reenviar email",
    ),
]
