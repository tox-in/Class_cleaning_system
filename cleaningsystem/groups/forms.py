from django import forms
from .models import CleaningGroup
from accounts.models import User

class GroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='student'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = CleaningGroup
        fields = ['name', 'members']