from django import forms
from .models import Task
from groups.models import CleaningGroup

class TaskForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=CleaningGroup.objects.all())
    
    class Meta:
        model = Task
        fields = ['group', 'date']
        
class TaskCompletionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']