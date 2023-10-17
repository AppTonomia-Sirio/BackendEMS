from rest_framework import permissions
from .models import NNA, Therapist


class IsNNAUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user.get_real_instance(), NNA)
        
class IsTherapistUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user.get_real_instance(), Therapist)