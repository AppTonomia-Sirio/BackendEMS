from .models import *
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "name",
            "surname",
            "password",
            "is_superuser",
            "created_at",
            "is_staff",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        required_fields = CustomUser.REQUIRED_FIELDS + CustomUser.USERNAME_FIELD
        errors = {}

        for field in required_fields:
            if not validated_data.get(field):
                errors[field] = "This field is required"
        if errors:
            raise serializers.ValidationError(errors)

        user = CustomUser(
            email=validated_data["email"],
            name=validated_data["name"],
            surname=validated_data["surname"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class NNAUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NNAUser
        fields = (
            "id",
            "email",
            "name",
            "surname",
            "password",
            "avatar",
            "created_at",
            "document",
            "date_of_birth",
            "home",
            "status",
            "gender",
            "educators",
            "main_educator",
            "therapist",
            "development_level",
            "performance",
            "is_autonomy_tutor",
            "autonomy_tutor",
            "entered_at",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
        }

        def create(self, validated_data):
            required_fields = NNAUser.REQUIRED_FIELDS + [NNAUser.USERNAME_FIELD]
            errors = {}

            for field in required_fields:
                if not validated_data.get(field):
                    errors[field] = "This field is required"
            if errors:
                raise serializers.ValidationError(errors)

            user = NNAUser(
                email=validated_data["email"],
                name=validated_data["name"],
                surname=validated_data["surname"],
                document=validated_data["document"],
                date_of_birth=validated_data["date_of_birth"],
                home=validated_data["home"],
                gender=validated_data["gender"],
            )
            user.set_password(validated_data["password"])
            user.save()
            return user


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = (
            "id",
            "email",
            "name",
            "surname",
            "password",
            "created_at",
            "homes",
            "roles",
            "is_admin",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        required_fields = StaffUser.REQUIRED_FIELDS + [StaffUser.USERNAME_FIELD]
        errors = {}

        for field in required_fields:
            if not validated_data.get(field):
                errors[field] = "This field is required"
        if errors:
            raise serializers.ValidationError(errors)

        user = StaffUser(
            email=validated_data["email"],
            name=validated_data["name"],
            surname=validated_data["surname"],
            is_admin=validated_data["is_admin"],
        )
        user.set_password(validated_data["password"])
        user.save()
        for role in validated_data["roles"]:
            user.roles.add(role)
            user.save()
        for home in validated_data["homes"]:
            user.homes.add(home)
            user.save()
        return user


class UserPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        CustomUser: CustomUserSerializer,
        NNAUser: NNAUserSerializer,
        StaffUser: StaffUserSerializer,
    }


class HomeSerializer(serializers.ModelSerializer):
    # Serializer for Location model
    class Meta:
        model = Home
        fields = ("id", "name", "address")


class RoleSerializer(serializers.ModelSerializer):
    # Serializer for Role model
    class Meta:
        model = Role
        fields = (
            "id",
            "name",
        )


class AvatarSerializer(serializers.ModelSerializer):
    # Serializer for Avatar model
    class Meta:
        model = Avatar
        fields = ("id",)
