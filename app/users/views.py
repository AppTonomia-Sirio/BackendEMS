from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserSerializer, HomeSerializer, RoleSerializer
from django.contrib.auth import authenticate
from .models import CustomUser, Home, Role
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUserToDelete


# Create your views here.

# LOGIN / REGISTER Views

class LoginView(APIView):
    """Retrieves a token for a user with the given credentials"""
    permission_classes = ()

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                return Response({"token": user.auth_token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
    """Creates a new user"""
    authentication_classes = ()
    permission_classes = ()

    def get_serializer_class(self):
        # Returns a different serializer without 'is_active' field for the creation of a new user
        class CustomUserCreateSerializer(UserSerializer):
            class Meta:
                model = CustomUser
                fields = ('id', 'email', 'name', 'surname', 'document', 'date_of_birth', 'home', 'roles')

        return CustomUserCreateSerializer


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


# Users data

class CurrentUserView(APIView):
    """Retrieves the data of the current user"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    """Lists all users"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes a user"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUserToDelete]


# Home data and role data

class HomeView(generics.RetrieveAPIView):
    """Retrieves, updates or deletes a home"""
    permission_classes = ()
    authentication_classes = ()
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    lookup_field = 'id'


class RoleView(generics.RetrieveAPIView):
    """Retrieves, updates or deletes a role"""
    permission_classes = ()
    authentication_classes = ()
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id'
