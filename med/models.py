from django.db import models
import enum
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


class UserRoles(models.IntegerChoices):
    DOCTOR = 1
    SUPERUSER = 2
    USER = 3


class Speciality(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = [
        (UserRoles.DOCTOR.value, 1),
        (UserRoles.SUPERUSER.value, 2),
        (UserRoles.USER.value, 3)
    ]
    role = models.IntegerField(choices=ROLE_CHOICES, default=UserRoles.USER)
    avatar = models.ImageField(upload_to='users', null=True, blank=True)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Doctor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    description = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    speciality = models.ForeignKey(to=Speciality, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class Consultation(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    from_doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    to_user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class ConsultationMessage(models.Model):
    from_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    consultation = models.ForeignKey(to=Consultation, on_delete=models.CASCADE)
    message = models.TextField()
    attachments = ArrayField(
        models.ImageField(upload_to='message_images')
    )


class Review(models.Model):
    from_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    to_doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    rate = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    message = models.TextField()
    consultation = models.ForeignKey(to=Consultation, on_delete=models.CASCADE, null=True, blank=True)