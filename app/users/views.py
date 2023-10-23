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



