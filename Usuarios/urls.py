from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegistrarUsuarioView,
    ListaTiposUsuariosView,
    AutenticarUsuarioGoogleView,
    CSRFTokenView,
    WhoAmIView,
)

auth = DefaultRouter()
tipos = DefaultRouter()
auth.register("email", RegistrarUsuarioView, basename="registrar con email")
auth.register("google", AutenticarUsuarioGoogleView, basename="registrar con google")
tipos.register("usuarios", ListaTiposUsuariosView)

urlpatterns = [
    path("csrf/", CSRFTokenView.as_view(), name="csrf"),
    path("whoami/", WhoAmIView.as_view(), name="whoami"),
    path("auth/", include(auth.urls)),
    path("tipos/", include(tipos.urls)),
]
