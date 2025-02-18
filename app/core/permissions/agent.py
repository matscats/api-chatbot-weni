from rest_framework import permissions


class IsAgentSelf(permissions.BasePermission):
    """
    Verifica se o agente a ser editado é o próprio usuário da sessão.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj
