from django.contrib import admin
from .models import (
    Usuario,
    AuthProvider,
    TipoUsuario,
    CodigoUnUso,
    PerfilCliente,
    PerfilParticularInmuebles,
    PerfilInmobiliaria,
    PerfilEmpleadoInmobiliaria,
    PerfilProfesionalServicios,
)
from Prestamos.models import PerfilAgenteHipotecario

admin.site.register(Usuario)
admin.site.register(AuthProvider)
admin.site.register(TipoUsuario)
admin.site.register(CodigoUnUso)
admin.site.register(PerfilCliente)
admin.site.register(PerfilParticularInmuebles)
admin.site.register(PerfilInmobiliaria)
admin.site.register(PerfilEmpleadoInmobiliaria)
admin.site.register(PerfilAgenteHipotecario)
admin.site.register(PerfilProfesionalServicios)
