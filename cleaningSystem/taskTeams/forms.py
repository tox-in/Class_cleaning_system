from django import forms
from .models import Group
from core.models import CustomUser  # Adjust based on your project structure


class GroupForm(forms.ModelForm):
    chief = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role="Chief"),
        widget=forms.Select(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
        error_messages={'required': 'A chief must be selected.'}, 
        required=True,
        
    )

    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='Member').exclude(group_as_member__isnull=False),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
        error_messages={'required': 'At least one member must be selected.'},
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Team name', 'class': 'w-full py-4 px-6 rounded-xl'}),
        error_messages={'required': 'Team name is required.'}
    )

    rating = forms.DecimalField(
        widget=forms.NumberInput(attrs={'placeholder': 'Rating', 'class': 'w-full py-4 px-6 rounded-xl'}),
        error_messages={'required': 'Rating is required.'}
    )

    class Meta:
        model = Group
        fields = ['name', 'specialization', 'chief', 'members', 'rating']
        widgets = {
            'specialization': forms.Select(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
        }

    def clean_members(self):
        members = self.cleaned_data.get('members')
        if members.count() > 5:
            raise forms.ValidationError("A group cannot have more than 5 members.")
        return members

    def clean_chief(self):
        chief = self.cleaned_data.get('chief')
        print(chief)
        if not chief:
            raise forms.ValidationError("A chief must be selected.")
        return chief
