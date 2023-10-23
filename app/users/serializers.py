from .models import CustomUser, Home
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # Serializer for NNA model
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'surname', 'document', 'date_of_birth', 'home', 'roles', 'is_active')


class HomeSerializer(serializers.ModelSerializer):
    # Serializer for Location model
    class Meta:
        model = Home
        fields = ('id', 'name', 'address')
