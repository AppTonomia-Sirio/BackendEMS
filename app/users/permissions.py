from rest_framework import permissions


class IsSuperUserToDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read only(GET, HEAD, OPTIONS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write only(POST, PATCH) for all users
        if request.method in ('POST', 'PATCH'):
            return True
        # Delete only for superusers
        return request.user and request.user.is_superuser


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user has role Admin
        return request.user and request.user.roles.filter(name='Admin').exists() or request.user.is_superuser
