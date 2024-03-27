from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework.permissions import AllowAny
from .serializers import *
from django_filters import rest_framework as filters
from .permissions import *
from django.utils import timezone
from django.core.cache import cache
from rest_framework.authtoken import views as drf_views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


#  Create users views


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


class CustomAuthToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR')
        failed_attempts = cache.get(ip, 0)

        if failed_attempts >= 5:
            return Response({'detail': 'Too many failed login attempts. Please try again in 5 minutes.'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        response = drf_views.obtain_auth_token(request._request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            cache.delete(ip)  # Reset the failed login attempts
        else:
            failed_attempts += 1
            cache.set(ip, failed_attempts, 60 * 5)  # Store the failed attempts for 5 minutes

        return response


class PasswordResetCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        code = get_random_string(length=6)
        PasswordResetCode.objects.create(user=user, code=code)

        send_mail(
            'Password reset code',
            f'Your password reset code is {code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return Response({'detail': 'Code sent'})


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        reset_code = PasswordResetCode.objects.filter(user=user, code=code).first()
        if not reset_code or timezone.now() - reset_code.created_at > timezone.timedelta(minutes=5):
            return Response({'detail': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = get_random_string(length=10)
        user.set_password(new_password)
        user.save()

        send_mail(
            'New password',
            f'Your new password is {new_password}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return Response({'detail': 'New password sent'})


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
