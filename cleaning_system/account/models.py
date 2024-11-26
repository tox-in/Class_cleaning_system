from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Chief', 'Chief'),
        ('Member', 'Member'),
        ('Client', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return f"{self.username} ({self.role})"