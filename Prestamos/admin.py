from django.contrib import admin
from .models import (
    EntidadBancaria,
    PerfilPrestatarioPrefab,
    EtapaEvaluacion,
    EstadoEvaluacion,
    DocumentoEvaluacionPrefab,
    PerfilPrestatario,
    EvaluacionCrediticia,
    Comentario,
    Documento,
    PreguntaPerfil,
    RespuestaPerfil,
)


admin.site.register(EntidadBancaria)
admin.site.register(PerfilPrestatarioPrefab)
admin.site.register(EtapaEvaluacion)
admin.site.register(EstadoEvaluacion)
admin.site.register(DocumentoEvaluacionPrefab)
admin.site.register(PerfilPrestatario)
admin.site.register(EvaluacionCrediticia)
admin.site.register(Comentario)
admin.site.register(Documento)
admin.site.register(PreguntaPerfil)
admin.site.register(RespuestaPerfil)
