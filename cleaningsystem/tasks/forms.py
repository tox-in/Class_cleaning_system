from django import forms
from .models import Task
from groups.models import Group

class TaskForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    
    class Meta:
        model = Task
        fields = ['group', 'date']
        
class TaskCompletionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']