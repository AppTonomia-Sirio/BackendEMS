from .models import *
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from django.utils.translation import gettext as _


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
                errors[field] = _("This field is required")
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
                    errors[field] = _("This field is required")
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
                description=validated_data["description"]
            )
            user.set_password(validated_data["password"])
            user.save()
            return user

    def validate_autonomy_tutor(self, value):
        """Validation for autonomy_tutor field"""
        code = "invalid"
        # Check that autonomy tutor is registered as such
        if not value.is_autonomy_tutor:
            raise ValidationError(
                _("The autonomy tutor must be activated as such before being assigned"),
                code=code,
            )
        # Check that autonomy tutor isn't self
        if value == self.instance:
            raise ValidationError(
                _("The autonomy tutor mustn't be assigned to itself"),
                code=code,
            )
        return value

    def validate_therapist(self, value):
        """Validation for therapist field"""
        code = "invalid"
        # Therapist must have the therapist Role
        if not value.roles.contains(Role.objects.get(name="Terapeuta")):
            raise ValidationError(
                _("The therapist needs to have the Therapist role before being assigned"),
                code=code
            )
        return value

    def validate_educators(self, value):
        """Validation for educator field"""
        code = "invalid"
        if len(value) > 4:
            raise ValidationError(
                _("Educators field cannot contain more than 4 educators."),
                code=code
            )
        return value

    def validate(self, data):
        """Validation for fields that need context"""

        code = "invalid"
        nna_home : Home = data["home"] if data.get("home") else self.instance.home
        role_educador : Role = Role.objects.get(name="Educador Tutor")
        educators = data["educators"] if data.get("educators") else self.instance.educators.all() if self.instance else None
        therapist = data["therapist"] if data.get("therapist") else self.instance.therapist if self.instance else None
        
        #
        # If educator is changed and not empty or if the home changed
        #
        if (data.get("educators") and data["educators"]) or (data.get("home") and educators != None):
            for educator in educators:
                # Check that Educadores Tutores are registered as such
                if not educator.roles.contains(role_educador):
                    raise ValidationError(
                        _(
                            "%(name)s %(surname)s needs to be have the Educator Tutor role before being assigned"
                        )
                        % {"name": educator.name, "surname": educator.surname},
                        code=code,
                    )
                # Check that the educator belongs to the same home
                if not educator.homes.contains(nna_home):
                    raise ValidationError(_(
                            "%(name)s %(surname)s must be assigned to home %(home_name)s before being assigned"
                        ) % {"name": educator.name, "surname": educator.surname, "home_name": nna_home.name},
                        code=code,
                    )
        #
        # If the main_educator changed check if they are in the educators field
        #
        if data.get("main_educator"):
            if data["main_educator"] not in educators:
                raise ValidationError(
                        _(
                            "%(name)s %(surname)s needs to be in the educators field before being assigned as main_educator"
                        )
                        % {"name": data["main_educator"].name, "surname": data["main_educator"].surname},
                        code=code,
                    )
        #
        # If the therapist or home changed check they are on the same home
        #
        if data.get("therapist") or (data.get("home") and therapist != None):
            if not therapist.homes.contains(nna_home):
                raise ValidationError(_(
                    "%(name)s %(surname)s must be assigned to home %(home_name)s before being assigned"
                    ) % {"name": therapist.name, "surname": therapist.surname, "home_name": nna_home.name},
                    code=code,
                )
        return data


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
            "is_staff",
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
                errors[field] = _("This field is required")
        if errors:
            raise serializers.ValidationError(errors)

        user = StaffUser(
            email=validated_data["email"],
            name=validated_data["name"],
            surname=validated_data["surname"],
            is_staff=validated_data["is_staff"],
        )
        user.set_password(validated_data["password"])
        user.save()
        for role in validated_data["roles"]:
            user.roles.add(role)
        for home in validated_data["homes"]:
            user.homes.add(home)
        user.full_clean()
        user.save()
        return user


class UserPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        CustomUser: CustomUserSerializer,
        NNAUser: NNAUserSerializer,
        StaffUser: StaffUserSerializer,
    }


class RestorePasswordSerializer(serializers.ModelSerializer):
    special_code = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "special_code")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        if validated_data.get('special_code') == instance.special_code:
            instance.set_password(validated_data["password"])
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({"special_code": "Invalid special code"})


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
