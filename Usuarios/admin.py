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
    PerfilAgentePrestamos,
    PerfilProfesionalServicios,
)

admin.site.register(Usuario)
admin.site.register(AuthProvider)
admin.site.register(TipoUsuario)
admin.site.register(CodigoUnUso)
admin.site.register(PerfilCliente)
admin.site.register(PerfilParticularInmuebles)
admin.site.register(PerfilInmobiliaria)
admin.site.register(PerfilEmpleadoInmobiliaria)
admin.site.register(PerfilAgentePrestamos)
admin.site.register(PerfilProfesionalServicios)
