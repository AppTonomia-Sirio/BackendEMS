from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .validators import DocumentValidator, PasswordValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.authtoken.models import Token
from django.db import models
from polymorphic.models import PolymorphicModel, PolymorphicManager


class CustomUserManager(BaseUserManager, PolymorphicManager):
    # Custom user manager
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')
        if not surname:
            raise ValueError('The Surname field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, name, surname, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, PolymorphicModel):
    # Custom user model
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, validators=[PasswordValidator()])

    created_at = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'password']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            Token.objects.create(user=self)

    def __str__(self):
        return self.email


class NNAUser(CustomUser):
    class Meta:
        verbose_name = 'NNA'
        verbose_name_plural = 'NNAs'

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Frozen', 'Frozen'),
        ('Locked', 'Locked')
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Undefined', 'Undefined')
    )

    document = models.CharField(max_length=255, blank=True, null=True, validators=[DocumentValidator()])
    date_of_birth = models.DateField()
    home = models.ForeignKey('Home', on_delete=models.PROTECT)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, default='Undefined')
    mentors = models.ManyToManyField('StaffUser', blank=True, related_name='mentors')
    therapist = models.ForeignKey('StaffUser', on_delete=models.PROTECT, blank=True, null=True)
    autonomy_level = models.IntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])
    tutor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    entered_at = models.DateField()

    REQUIRED_FIELDS = ['name', 'surname', 'password', 'date_of_birth', 'home', 'gender']


class StaffUser(CustomUser):
    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'

    homes = models.ManyToManyField("Home")
    roles = models.ManyToManyField("Role")
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['name', 'surname', 'password', 'homes', "roles", "is_admin"]


class Home(models.Model):
    # Location model

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    # Role model

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
