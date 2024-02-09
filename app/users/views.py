from rest_framework import generics
from .models import CustomUser
from .serializers import UserPolymorphicSerializer


class UserViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserPolymorphicSerializer
    lookup_field = "id"