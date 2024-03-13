from rest_framework import permissions
from .models import *


class NNAListCreatePermission(permissions.BasePermission):
    """Permission to create new NNA users"""

    # If the user is superuser - allow
    # if not - the request must not have fields:
    #   "mentors", "therapist", "autonomy_level", "tutor", "entered_at", "created_at", "status"

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if request.method != "POST":
            return request.user.is_authenticated

        forbidden_fields = [
            "mentors",
            "therapist",
            "autonomy_level",
            "tutor",
            "entered_at",
            "created_at",
            "status",
        ]
        if (
            any(field in request.data for field in forbidden_fields)
            or request.user.is_authenticated
        ):
            return False

        return True


class StaffListPermission(permissions.BasePermission):
    """Permission to view Staff users"""

    # To retrieve - user must be authenticated
    def has_permission(self, request, view):
        return request.user.is_authenticated


class NNADetailPermission(permissions.BasePermission):
    """Permission to retrieve, update or delete an NNA"""

    # If the user is superuser - allow
    # if not - the request must not have fields:
    #   "mentors", "therapist", "autonomy_level", "tutor", "entered_at", "created_at", "status"
    # Only user itself can be updated
    # Only superuser can delete
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if request.method == "DELETE":
            return False

        if request.method == "GET":
            return request.user.is_authenticated

        forbidden_fields = [
            "mentors",
            "therapist",
            "autonomy_level",
            "tutor",
            "entered_at",
            "created_at",
            "status",
        ]
        if any(field in request.data for field in forbidden_fields):
            return False

        if request.method == "PUT" or request.method == "PATCH":
            return request.user.id == view.kwargs["id"]

        return False


class StaffDetailPermission(permissions.BasePermission):
    """Permission to retrieve, update or delete a Staff user"""

    # Only superuser can update or delete
    # To retrieve - user must be authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method == "GET":
            return request.user.is_authenticated

        if request.method == "PUT" or request.method == "PATCH":
            return request.user == obj

        return False


class IsInSameHomePermission(permissions.BasePermission):
    """Permission to limit access to only users in the same home"""

    def has_object_permission(self, request, view, obj):
        user = request.user.get_real_instance()
        requested = obj.get_real_instance()
        user_class = request.user.get_real_instance_class()
        obj_class = obj.get_real_instance_class()

        if user_class == CustomUser:
            return True

        if user_class == StaffUser:
            if obj_class == NNAUser:
                return user.homes.all().contains(requested.home)
            elif obj_class == StaffUser:
                return bool(set(requested.homes.all()).intersection(user.homes.all()))

        if user_class == NNAUser:
            if obj_class == NNAUser:
                return user.home == requested.home
            elif obj_class == StaffUser:
                return requested.homes.all().contains(user.home)


class IsSuperUserToModify(permissions.BasePermission):
    """Permission to modify anything in the database"""

    # Only superuser can modify
    # To retrieve no authentication is required

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method != "GET":
            return False

        return True
