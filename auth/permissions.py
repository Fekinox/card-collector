from rest_framework import permissions


class IsAdminOrOwningUserOrAnonReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_superuser or
            obj.username == request.user.username
        )
