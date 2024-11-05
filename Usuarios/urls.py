from django.urls import path, include
from .views import RegistrarUsuarioView

urlpatterns = [
    path("registrar/", RegistrarUsuarioView.as_view(), name="registrar"),
]
