from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import LocationSerializer, UserPolymorphicSerializer, NNASerializer, TherapistSerializer
from django.contrib.auth import authenticate
from .models import Location, Therapist, NNA, CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsNNAUser, IsTherapistUser


# Create your views here.


class UserCreate(generics.CreateAPIView):
    """Create a new user, at the moment only NNA users can be created"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = NNASerializer


class LoginView(APIView):
    """Retrieves a token for a user with the given credentials"""
    permission_classes = ()

    def post(
            self,
            request,
    ):
        email = request.data.get("email")
        password = request.data.get("password")
        # Check if credentials are correct
        user = authenticate(email=email, password=password)
        if user:
            # If they are, return token
            return Response({"token": user.auth_token.key}, status=status.HTTP_200_OK)
        else:
            # If not, return error
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class NNAStatus(APIView):
    """Retrieve the status of the current NNA user. User must be authenticated and be an NNA user"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsNNAUser]

    def get(self, request):
        # TODO Find a way to avoid looking up all the users and get user directly from request
        user = NNA.objects.get(email=request.user.email)
        return Response({"status": user.status}, status=status.HTTP_200_OK)


class TherapistList(generics.ListAPIView):
    """Retrieve a list of all therapists"""
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer
    permission_classes = ()


class LocationList(generics.ListAPIView):
    """Retrieve a list of all locations"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = ()


class UserData(APIView):
    """Retrieve user details based on the provided email. User must be authenticated"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, email, *args, **kwargs):
        # Checks if a user with a matching email exists and returns it
        # If not returns a 404
        user = CustomUser.objects.filter(email=email).first()
        if user:
            serialized_user = UserPolymorphicSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_200_OK)

        return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class NNAofTherapist(generics.ListAPIView):
    """Retrieve all NNA assigned to the current therapist"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsTherapistUser]
    serializer_class = NNASerializer

    def get_queryset(self):
        return NNA.objects.filter(mentor=self.request.user.id)
