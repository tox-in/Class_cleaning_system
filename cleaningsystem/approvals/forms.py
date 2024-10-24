from django import forms
from .models import Approval

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = ['approval_status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave remarks here ...'})
        }