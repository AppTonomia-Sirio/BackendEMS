from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import *
from .serializers import *
from django_filters import rest_framework as filters
from .permissions import *


#  Create users views


class NNAListCreateView(generics.ListCreateAPIView):
    """Creates a new user"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (NNAListCreatePermission, IsInSameHomePermission)

    def get_queryset(self):
        """Filter by home"""
        user = self.request.user.get_real_instance()
        user_class = self.request.user.get_real_instance_class()
        if user_class == NNAUser:
            return NNAUser.objects.filter(home=user.home)
        elif user_class == StaffUser:
            return NNAUser.objects.filter(home__in=user.homes.all())
        else:
            return NNAUser.objects.all()

    serializer_class = NNAUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "id",
        "email",
        "name",
        "surname",
        "created_at",
        "document",
        "date_of_birth",
        "home",
        "status",
        "gender",
        "educators",
        "therapist",
        "development_level",
        "performance",
        "avatar",
        "description",
        "is_autonomy_tutor",
        "autonomy_tutor",
        "entered_at",
    )


class StaffListView(generics.ListAPIView):
    """Creates a new user"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (StaffListPermission, IsInSameHomePermission)

    def get_queryset(self):
        """Filter by home"""
        user = self.request.user.get_real_instance()
        user_class = self.request.user.get_real_instance_class()
        if user_class == NNAUser:
            return StaffUser.objects.filter(homes__contains=user.home)
        elif user_class == StaffUser:
            return StaffUser.objects.filter(homes__in=user.homes.all())
        else:
            return StaffUser.objects.all()

    serializer_class = StaffUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "id",
        "email",
        "name",
        "surname",
        "password",
        "created_at",
        "homes",
        "roles",
        "is_staff",
    )


# Users retrieve and edits


# Users retrieve and edits
class NNADetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes an NNA"""

    queryset = NNAUser.objects.all()
    serializer_class = NNAUserSerializer
    lookup_field = "id"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (NNADetailPermission, IsInSameHomePermission)


class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes a staff"""

    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer
    lookup_field = "id"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (StaffDetailPermission, IsInSameHomePermission)


class CurrentUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserPolymorphicSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (StaffDetailPermission,)

    def get_object(self):
        return self.request.user.get_real_instance()


# Lists
class HomeListView(generics.ListAPIView):
    """Lists all homes"""

    permission_classes = ()
    authentication_classes = (TokenAuthentication,)
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class RoleListView(generics.ListAPIView):
    """Lists all roles"""

    permission_classes = ()
    authentication_classes = (TokenAuthentication,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class AvatarListView(generics.ListAPIView):
    """Lists all avatars"""

    permission_classes = ()
    authentication_classes = ()
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer


# Minor models data
class AvatarView(generics.RetrieveAPIView):
    """Retrieves an Avatar"""

    permission_classes = ()
    authentication_classes = ()
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    lookup_field = "id"


class HomeView(generics.RetrieveAPIView):
    """Retrieves a home"""

    permission_classes = (IsSuperUserToModify,)
    authentication_classes = (TokenAuthentication,)
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    lookup_field = "id"


class RoleView(generics.RetrieveAPIView):
    """Retrieves a role"""

    permission_classes = (IsSuperUserToModify,)
    authentication_classes = (TokenAuthentication,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = "id"
