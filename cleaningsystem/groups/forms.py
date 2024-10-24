from django import forms
from .models import Group
from accounts.models import User

class GroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='student'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = Group
        fields = ['name', 'members']