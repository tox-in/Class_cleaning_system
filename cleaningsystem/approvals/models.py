from django.db import models

# Create your models here.
class Approval(models.Model):
    task = models.OneToOneField('tasks.Task', on_delete=models.CASCADE)
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'admin'})
    approval_status = models.BooleanField(default=False)  # True if approved, False if rejected
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Approval for {self.task}"
