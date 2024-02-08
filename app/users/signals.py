from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import CustomUser, Role, NNAUser, StaffUser


# Signals

# Token creating for NNA and Therapist type users when they are registered


# Creates 3 roles when the app is started
@receiver(post_migrate)
def create_initial_roles(sender, **kwargs):
    if Role.objects.count() == 0:
        Role.objects.get_or_create(name='NNA')
        Role.objects.get_or_create(name='Therapist')
        Role.objects.get_or_create(name='Admin')
