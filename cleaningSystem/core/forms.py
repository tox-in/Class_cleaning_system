from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser
import re

class LoginForm(AuthenticationForm):
     username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your username', 'class':'w-full py-4 px-6 rounded-xl'}))
     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your password', 'class':'w-full py-4 px-6 rounded-xl'}))

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Your username', 'class':'w-full py-4 px-6 rounded-xl'}),
        error_messages={'required': 'Username is required.'}
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder':'Your email', 'class':'w-full py-4 px-6 rounded-xl'}),
        error_messages={'required': 'Email is required.'}
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Your password', 'class':'w-full py-4 px-6 rounded-xl'}),
        error_messages={'required': 'Password is required.'}
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Repeat password', 'class':'w-full py-4 px-6 rounded-xl'}),
        error_messages={'required': 'Please confirm your password.'}
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
        error_messages={'required': 'Please select a role.'}
    )
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields must match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.role:
            user.role = 'Member'  # Default role can be 'Member'
        if commit:
            user.save()
        return user
