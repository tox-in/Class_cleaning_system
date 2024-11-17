from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['cleaning_type', 'address', 'house_number', 'cleaning_date']
        widgets = {
            'cleaning_date': forms.DateInput(attrs={'type': 'date'})
        }