from rest_framework import generics
from .models import *
from .serializers import *
from django_filters import rest_framework as filters

#Create users views

class NNAListCreateView(generics.ListCreateAPIView):
    """Creates a new user"""

    authentication_classes = ()
    permission_classes = ()
    queryset = NNAUser.objects.all() #TODO add filters
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
                        "mentors",
                        "therapist",
                        "autonomy_level",
                        "tutor",
                        "entered_at",
                        )

class StaffListCreateView(generics.ListCreateAPIView):
    """Creates a new user"""

    authentication_classes = ()
    permission_classes = () 
    queryset = StaffUser.objects.all()
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
                        "is_admin",
                        )

#Users retrieve and edits
class NNADetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes an NNA"""
    queryset = NNAUser.objects.all()
    serializer_class = NNAUserSerializer
    lookup_field = "id"
    authentication_classes = ()
    permission_classes = ()

class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes a staff"""
    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer
    lookup_field = "id"
    authentication_classes = ()
    permission_classes = ()

# Lists
class HomeListView(generics.ListAPIView):
    """Lists all homes"""

    permission_classes = ()
    authentication_classes = ()
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class RoleListView(generics.ListAPIView):
    """Lists all roles"""

    permission_classes = ()
    authentication_classes = ()
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# Home and Role data


class HomeView(generics.RetrieveAPIView):
    """Retrieves, updates or deletes a home"""

    permission_classes = ()
    authentication_classes = ()
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    lookup_field = "id"


class RoleView(generics.RetrieveAPIView):
    """Retrieves, updates or deletes a role"""

    permission_classes = ()
    authentication_classes = ()
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = "id"
