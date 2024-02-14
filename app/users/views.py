from rest_framework import generics
from .models import *
from .serializers import *

#Create users views

class NNAListCreateView(generics.ListCreateAPIView):
    """Creates a new user"""

    authentication_classes = ()
    permission_classes = ()
    queryset = NNAUser.objects.all() #TODO add filters
    serializer_class = NNAUserSerializer

class StaffListCreateView(generics.ListCreateAPIView):
    """Creates a new user"""

    authentication_classes = ()
    permission_classes = () 
    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer

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
