from django.db import models
from account.models import User

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    specialization = models.CharField(
        max_length=50,
        choices=[
            ('Salon', 'Salon Cleaning'),
            ('Kitchen', 'Kitchen Cleaning'),
            ('Gardening', 'Gardening Cleaning'),
            ('Backyard', 'Backyard Cleaning'),
            ('Poultry', 'Poultry Cleaning'),
            ('Glasss', 'Glasss Cleaning'),
            ('Loundry', 'Loundry Cleaning'),
        ]
    )
    chief = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='group_as_chief',
        limit_choices_to={'role': 'Chief'}
    )
    members = models.ManyToManyField(
        User,
        related_name='group_as_member',
        limit_choices_to={'role': 'Member'}
    )
    rating = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        # Ensure no more than 5 members (including the chief)
        if self.members.count() >= 5:
            raise ValueError("A group cannot have more than 5 members.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.specialization})"