from rest_framework import permissions
from .models import NNA, Therapist


class IsNNAUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            status = NNA.objects.get(email=request.user.email).status
            return True
        except:
            return False
        
class IsTherapistUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            therapist = Therapist.objects.get(email=request.user.email)
            return True
        except:
            return False