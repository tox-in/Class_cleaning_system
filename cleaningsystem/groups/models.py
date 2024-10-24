from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField('accounts.User', limit_choices_to={'role': 'student'})

    def __str__(self):
        return self.name

