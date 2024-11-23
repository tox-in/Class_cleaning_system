from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['cleaning_type', 'address', 'house_number', 'cleaning_date', 'priority']
        exclude = ['client', 'assigned_group', 'price', 'approved_by_client', 'approved_by_admin']
        
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'w-full py-4 px-6 rounded-xl'}),
            'house_number': forms.NumberInput(attrs={'placeholder': 'House number', 'class': 'w-full py-4 px-6 rounded-xl'}),
            'cleaning_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full py-4 px-6 rounded-xl'}),
            'cleaning_type': forms.Select(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
            'priority': forms.Select(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
        }
        
        error_messages = {
            'address': {'required': 'Address is required.'},
            'house_number': {'required': 'House number is required.'},
            'cleaning_date': {'required': 'Cleaning date is required.'},
        }
