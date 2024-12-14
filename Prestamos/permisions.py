from rest_framework import permissions


class IsAgenteOrPrestatario(permissions.BasePermission):
    """
    Solo deja editar al agente, si es el prestatario solo puede ver
    otros usuarios no pueden ver o editar
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, "perfil_agente_hipotecario"):
            return obj.agente == request.user.perfil_agente_hipotecario

        if request.method in permissions.SAFE_METHODS:
            return getattr(request.user, "perfil_prestatario", None) == obj.prestatario

        return False
