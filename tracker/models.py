from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    # Custom user model for potential future extensions
    pass

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=3, choices=ACTIVITY_TYPES)
    duration = models.PositiveIntegerField()  # Minutes
    distance = models.FloatField(null=True, blank=True)
    distance_unit = models.CharField(max_length=2, choices=DISTANCE_UNITS, null=True, blank=True)
    calories = models.PositiveIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"