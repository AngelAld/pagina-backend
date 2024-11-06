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
)
from rest_framework_simplejwt.views import TokenRefreshView

auth = DefaultRouter()
tipos = DefaultRouter()
perfiles = DefaultRouter()
# Auth
auth.register("email", RegistrarUsuarioView, basename="registrar con email")
auth.register("google", AutenticarUsuarioGoogleView, basename="registrar con google")
auth.register("login", LoginEmailView, basename="Iniciar sesión con email")
# Tipos
tipos.register("usuarios", ListaTiposUsuariosView)

# Perfiles
perfiles.register("cliente", PerfilClienteView)
perfiles.register(
    "particular-inmuebles",
    PerfilParticularInmueblesView,
    basename="perfil-particular-inmuebles",
)
perfiles.register(
    "inmobiliaria", PerfilInmobiliariaView, basename="perfil-inmobiliaria"
)
perfiles.register(
    "empleado-inmobiliaria",
    PerfilEmpleadoInmobiliariaView,
    basename="perfil-empleado-inmobiliaria",
)

urlpatterns = [
    path("whoami/", WhoAmIView.as_view(), name="whoami"),
    path("auth/", include(auth.urls)),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("tipos/", include(tipos.urls)),
    path("perfiles/", include(perfiles.urls)),
]
