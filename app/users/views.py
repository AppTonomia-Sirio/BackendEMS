import random
import string

from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import *
from .serializers import *
from django_filters import rest_framework as filters
from .permissions import *


#  Create users views

class SendCodeView(generics.UpdateAPIView):
    """Sends a special code to the user's email"""

    queryset = NNAUser.objects.all()
    serializer_class = RestorePasswordSerializer
    lookup_field = "email"
    authentication_classes = ()
    permission_classes = ()

    def put(self, request, *args, **kwargs):
        # Generate a special code
        code_characters = string.digits
        special_code = ''.join(random.choice(code_characters) for i in range(6))

        # Get the user
        user = self.get_object()
        if not user:
            return Response({"error": "invalid email"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the special code to the user's model (you need to add a field for this)
        user.special_code = special_code
        user.save()

        # Send the special code to the user's email
        send_mail(
            'Your special code',
            f'Your special code is {special_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "Special code sent"}, status=status.HTTP_200_OK)


class RestorePasswordView(generics.UpdateAPIView):
    """Restores the password of a user"""

    queryset = NNAUser.objects.all()
    serializer_class = RestorePasswordSerializer
    lookup_field = "email"
    authentication_classes = ()
    permission_classes = ()

    def put(self, request, *args, **kwargs):
        # Get the user
        user = self.get_object()
        if not user:
            return Response({"error": "invalid email"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the special code matches
        if request.data.get('special_code') == user.special_code:
            # Generate a random password
            password_characters = string.ascii_letters + string.digits + string.punctuation
            random_password = ''.join(random.choice(password_characters) for i in range(10))

            # Set the new password
            user.set_password(random_password)
            user.save()

            # Send the new password to the user's email
            send_mail(
                'Your new password',
                f'Your new password is {random_password}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "New password sent"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid special code"}, status=status.HTTP_400_BAD_REQUEST)


class NNAListCreateView(generics.ListCreateAPIView):
    """Creates a new user"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (NNAListCreatePermission,)
    queryset = NNAUser.objects.all()  # TODO add filters
    serializer_class = NNAUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "id",
        "email",
        "name",
        "surname",
        "created_at",
        "document",
        "date_of_birth",
        "home",
        "status",
        "gender",
        "educators",
        "therapist",
        "development_level",
        "performance",
        "avatar",
        "description",
        "is_autonomy_tutor",
        "autonomy_tutor",
        "entered_at",
    )


class StaffListView(generics.ListAPIView):
    """Creates a new user"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (StaffListPermission,)
    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
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


# Users retrieve and edits


# Users retrieve and edits
class NNADetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes an NNA"""

    queryset = NNAUser.objects.all()
    serializer_class = NNAUserSerializer
    lookup_field = "id"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (NNADetailPermission,)


class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes a staff"""

    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer
    lookup_field = "id"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (StaffDetailPermission,)


# Lists
class HomeListView(generics.ListAPIView):
    """Lists all homes"""

    permission_classes = ()
    authentication_classes = (TokenAuthentication,)
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class RoleListView(generics.ListAPIView):
    """Lists all roles"""

    permission_classes = ()
    authentication_classes = (TokenAuthentication,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class AvatarListView(generics.ListAPIView):
    """Lists all avatars"""

    permission_classes = ()
    authentication_classes = ()
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer


# Minor models data
class AvatarView(generics.RetrieveAPIView):
    """Retrieves an Avatar"""

    permission_classes = ()
    authentication_classes = ()
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    lookup_field = "id"


class HomeView(generics.RetrieveAPIView):
    """Retrieves a home"""

    permission_classes = (IsSuperUserToModify,)
    authentication_classes = (TokenAuthentication,)
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    lookup_field = "id"


class RoleView(generics.RetrieveAPIView):
    """Retrieves a role"""

    permission_classes = (IsSuperUserToModify,)
    authentication_classes = (TokenAuthentication,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = "id"
