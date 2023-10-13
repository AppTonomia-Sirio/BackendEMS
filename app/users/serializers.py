from .models import NNA, Therapist, Location
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class NNASerializer(serializers.ModelSerializer):
    class Meta:
        model = NNA
        fields = ('email', 'password', 'name', 'surname', 'location', 'date_of_birth', 'mentor', 'status', 'id')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        required_fields = ['email', 'password', 'name', 'surname', 'location', 'date_of_birth', 'mentor']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise serializers.ValidationError(f"Missing fields: {', '.join(missing_fields)}")

        return data

    def create(self, validated_data):
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
    class Meta:
        model = Therapist
        fields = ('email', 'password', 'name', 'surname', 'id')
        extra_kwargs = {'password': {'write_only': True}}


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address')







