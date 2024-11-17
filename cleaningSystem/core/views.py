from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from taskTeams.models import Profile
from django.contrib import messages
from django.contrib.auth import logout
from.models import CustomUser

# Create your views here.
def index(request):
    return render(request, 'core/base.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = form.save()  # Save the form and get the user instance
            login(request, user)  # Automatically log in the user after successful signup
            
            # Optionally, add a success message
            messages.success(request, "Account created successfully! Welcome.")
            
            return redirect('/login/')
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {
        'form': form
    })

@receiver(post_save, sender=CustomUser)  # Use CustomUser here
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)  # Use CustomUser here
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def custom_logout(request):
    logout(request)
    return redirect('/')