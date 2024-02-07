from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .validators import DocumentValidator, PasswordValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
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

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname','email','password']

    def __str__(self):
        return self.email

class NNAUser(CustomUser):
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
    mentor = models.ManyToManyField('StaffUser', blank = True)
    autonomy_level = models.IntegerField(default = 1, validators = [MaxValueValidator(10), MinValueValidator(1)])
    is_tutor = models.BooleanField(default = False)
    therapist = models.ForeignKey(StaffUser, on_delete=models.PROTECT)
    entered_at = models.DateField()
    
    REQUIRED_FIELDS = ['name', 'surname','email','password','date_of_birth','home','status','gender']


class StaffUser(CustomUser):

    homes = models.ManyToManyField("Home")
    roles = models.ManyToManyField("Role")
    is_admin = models.BooleanField(default = False)
    
    REQUIRED_FIELDS = ['name', 'surname','email','password','homes',"roles", "is_admin"]


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
