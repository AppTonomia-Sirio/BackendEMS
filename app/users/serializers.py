from .models import NNA, Therapist, Location
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class NNASerializer(serializers.ModelSerializer):
    # Serializer for NNA model

    class Meta:
        # Fields to be serialized
        model = NNA
        fields = ('email', 'password', 'name', 'surname', 'location', 'date_of_birth', 'mentor', 'status', 'id')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Check if all required fields are present
        required_fields = ['email', 'password', 'name', 'surname', 'location', 'date_of_birth', 'mentor']
        missing_fields = [field for field in required_fields if field not in data]

        # Raise error if any required field is missing
        if missing_fields:
            raise serializers.ValidationError(f"Missing fields: {', '.join(missing_fields)}")

        return data

    def create(self, validated_data):
        # Create and return a new NNA user
        user = NNA(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            location=validated_data['location'],
            date_of_birth=validated_data['date_of_birth'],
            mentor=validated_data['mentor'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class TherapistSerializer(serializers.ModelSerializer):
    # Serializer for Therapist model
    class Meta:
        model = Therapist
        fields = ('email', 'password', 'name', 'surname', 'id')
        extra_kwargs = {'password': {'write_only': True}}


class UserPolymorphicSerializer(PolymorphicSerializer):
    # Serializer for polymorphic user model,
    # Used to solve isinstance() problem in permissions.py
    model_serializer_mapping = {
        NNA: NNASerializer,
        Therapist: TherapistSerializer
    }


class LocationSerializer(serializers.ModelSerializer):
    # Serializer for Location model
    class Meta:
        model = Location
        fields = ('id', 'name', 'address')
