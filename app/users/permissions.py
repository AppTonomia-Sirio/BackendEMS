from rest_framework import permissions


class NNAListCreatePermission(permissions.BasePermission):
    """Permission to create new NNA users"""

    # If the user is superuser - allow
    # if not - the request must not have fields:
    #   "mentors", "therapist", "autonomy_level", "tutor", "entered_at", "created_at", "status"

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method != 'POST':
            return request.user.is_authenticated

        forbidden_fields = ["mentors", "therapist", "autonomy_level", "tutor", "entered_at", "created_at", "status"]
        if any(field in request.data for field in forbidden_fields):
            return False

        return True


class StaffListCreatePermission(permissions.BasePermission):
    """Permission to create new Staff users"""

    # If the user is superuser - allow
    # if not - deny
    def has_permission(self, request, view):
        return request.user.is_superuser


class NNADetailPermission(permissions.BasePermission):
    """Permission to retrieve, update or delete an NNA"""

    # If the user is superuser - allow
    # if not - the request must not have fields:
    #   "mentors", "therapist", "autonomy_level", "tutor", "entered_at", "created_at", "status"
    # Only user itself can be updated
    # Only superuser can delete
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method == 'DELETE':
            return False

        if request.method == 'GET':
            return request.user.is_authenticated

        forbidden_fields = ["mentors", "therapist", "autonomy_level", "tutor", "entered_at", "created_at", "status"]
        if any(field in request.data for field in forbidden_fields):
            return False

        if request.method == 'PUT' or request.method == 'PATCH':
            return request.user.id == view.kwargs['id']

        return False


class StaffDetailPermission(permissions.BasePermission):
    """Permission to retrieve, update or delete a Staff user"""

    # Only superuser can update or delete
    # To retrieve - user must be authenticated

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method == 'GET':
            return request.user.is_authenticated

        return False


class IsSuperUserToModify(permissions.BasePermission):
    """Permission to modify anything in the database"""
    # Only superuser can modify
    # To retrieve no authentication is required

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method != 'GET':
            return False

        return True

