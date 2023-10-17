from rest_framework import permissions
from .models import NNA, Therapist


class IsNNAUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user is NNA
        return isinstance(request.user.get_real_instance(), NNA)


class IsTherapistUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user is Therapist
        return isinstance(request.user.get_real_instance(), Therapist)
