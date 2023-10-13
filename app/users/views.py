from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import NNASerializer, LocationSerializer, TherapistSerializer
from django.contrib.auth import authenticate
from .models import Location, Therapist, NNA
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsNNAUser

# Create your views here.


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = NNASerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            return Response({"token": user.auth_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class NNAStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsNNAUser]

    def get(self, request):
        user = NNA.objects.get(email=request.user.email)
        return Response({"status": user.status}, status=status.HTTP_200_OK)


class TherapistList(generics.ListAPIView):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer
    permission_classes = ()


class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = ()


