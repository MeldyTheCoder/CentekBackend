from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRoles(models.IntegerChoices):
    DOCTOR = 1
    SUPERUSER = 2
    USER = 3


class Speciality(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    surname = models.CharField(max_length=100, null=True, blank=True)

    ROLE_CHOICES = [
        (UserRoles.DOCTOR.value, 1),
        (UserRoles.SUPERUSER.value, 2),
        (UserRoles.USER.value, 3)
    ]
    role = models.IntegerField(choices=ROLE_CHOICES, default=UserRoles.USER)
    avatar = models.ImageField(upload_to='users', null=True, blank=True)
    email = models.EmailField(unique=True)
    speciality = models.ForeignKey(to=Speciality, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Passport(models.Model):
    series = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
    issued_by = models.CharField(max_length=100)
    birth_place = models.CharField(max_length=100)
    issued_date = models.DateField()
    patient = models.OneToOneField(to=User, on_delete=models.CASCADE)


class Hospitalization(models.Model):
    code = models.CharField(max_length=100)
    diagnose = models.CharField(max_length=50, null=True, blank=True)
    purpose = models.CharField(max_length=100, null=True, blank=True)
    insurance_company = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    department = models.CharField(blank=True, null=True)
    cancellation_reason = models.CharField(max_length=255, null=True, blank=True)
    patient = models.ForeignKey(to=User, on_delete=models.CASCADE)
    passport = models.ForeignKey(to=Passport, on_delete=models.CASCADE)