from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from core.models import CustomUser
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('Chief', 'Chief'),
        ('Member', 'Member'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Group(models.Model):
    ROLE_CHOICES = [
        ('Chief', 'Chief'),
        ('Member', 'Member'),
    ]
    SPECIALIZATION_CHOICES = [
        ('Salon', 'Salon Cleaning'),
        ('Kitchen', 'Kitchen Cleaning'),
        ('Gardening', 'Gardening Cleaning'),
        ('Backyard', 'Backyard Cleaning'),
        ('Poultry', 'Poultry Cleaning'),
        ('Glass', 'Glass Cleaning'),
        ('Laundry', 'Laundry Cleaning'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    chief = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='group_as_chief',
        limit_choices_to={'role': 'Chief'}
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='group_as_member',
        limit_choices_to={'role': 'Member'}
    )
    rating = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures validation is applied
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.specialization})"

