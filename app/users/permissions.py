from rest_framework import permissions
from .models import NNA


class IsNNAUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            status = NNA.objects.get(email=request.user.email).status
            return True
        except:
            return False
