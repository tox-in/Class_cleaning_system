from django.db import models

# Create your models here.
class Task(models.Model):
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return f"{self.group.name} - {self.date}"
