from django.db import models
from account.models import User
from groups.models import Group

# Create your models here.
class Reservation(models.Model):
    CLEANING_TYPES = [
        ('Salon', 'Salon Cleaning'),
            ('Kitchen', 'Kitchen Cleaning'),
            ('Gardening', 'Gardening Cleaning'),
            ('Backyard', 'Backyard Cleaning'),
            ('Poultry', 'Poultry Cleaning'),
            ('Glasss', 'Glasss Cleaning'),
            ('Loundry', 'Loundry Cleaning'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    cleaning_type = models.CharField(max_length=50, choices=CLEANING_TYPES)
    address = models.TextField()
    house_number = models.CharField(max_length=50)
    cleaning_date = models.DateField()
    reservation_date = models.DateTimeField(auto_now_add=True)
    assigned_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    approved_by_client = models.BooleanField(default=False)
    approved_by_admin = models.BooleanField(default=False)
    
    def __str__(self) :
        return f"Reservation #{self.id} - {self.cleaning_type}"