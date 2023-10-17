from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import NNA, Therapist


# Signals

# Token creating for NNA and Therapist type users when they are registered

# Create token when user is created (NNA)
@receiver(post_save, sender=NNA)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)


# Create token when user is created (Therapist)
@receiver(post_save, sender=Therapist)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
