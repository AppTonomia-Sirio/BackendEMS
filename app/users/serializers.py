from .models import Student, Therapist, Location
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('email', 'password', 'name', 'surname', 'location', 'date_of_birth', 'mentor', 'status', 'id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Student(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            location=validated_data['location'],
            date_of_birth=validated_data['date_of_birth'],
            mentor=validated_data['mentor'],
        )

        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
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



