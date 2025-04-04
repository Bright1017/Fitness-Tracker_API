from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email,password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

     
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Custom user model for potential future extensions
    email = models.EmailField(null=False, blank=False, unique=True)
    username = models.CharField(max_length=50, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('RUN', 'Running'),
        ('CYC', 'Cycling'),
        ('WLK', 'Walking'),
        ('SWM', 'Swimming'),
        ('WL', 'Weightlifting'),
    ]
    DISTANCE_UNITS = [
        ('km', 'Kilometers'),
        ('mi', 'Miles'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=3, choices=ACTIVITY_TYPES)
    duration = models.PositiveIntegerField()  # Minutes
    distance = models.FloatField(null=True, blank=True)
    distance_unit = models.CharField(max_length=2, choices=DISTANCE_UNITS, null=True, blank=True)
    calories = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"