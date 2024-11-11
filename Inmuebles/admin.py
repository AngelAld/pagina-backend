from django.contrib import admin
from .models import (
    Caracteristica,
    TipoAntiguedad,
    TipoInmueble,
    SubTipoInmueble,
    EstadoInmueble,
    TipoOperacion,
    Inmueble,
    ImagenInmueble,
    PlanoInmueble,
    UbicacionInmueble,
    Favorito,
    Visita,
)

admin.site.register(Caracteristica)
admin.site.register(TipoAntiguedad)
admin.site.register(TipoInmueble)
admin.site.register(SubTipoInmueble)
admin.site.register(EstadoInmueble)
admin.site.register(TipoOperacion)
admin.site.register(Inmueble)
admin.site.register(ImagenInmueble)
admin.site.register(PlanoInmueble)
admin.site.register(UbicacionInmueble)
admin.site.register(Favorito)
admin.site.register(Visita)
