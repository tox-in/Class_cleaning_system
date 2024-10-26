from django.db import models
from groups.models import CleaningGroup

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    group = models.ForeignKey(CleaningGroup, on_delete=models.CASCADE, related_name="tasks")
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
