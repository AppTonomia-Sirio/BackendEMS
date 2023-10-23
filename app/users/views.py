from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserSerializer, HomeSerializer
from django.contrib.auth import authenticate
from .models import CustomUser, Home
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.


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
