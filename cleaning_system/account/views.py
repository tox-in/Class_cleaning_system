from django.shortcuts import render
from django.contrib.auth import logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Check if username or email already exists
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            if get_user_model().objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
                return render(request, 'registration/signup.html', {'form': form})
            
            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return render(request, 'registration/signup.html', {'form': form})
            
            # Create the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.role = 'Client'  # This could be dynamic based on your needs
            user.save()

            # Success message and redirect
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            # Error message if form is not valid
            messages.error(request, "Error creating account. Please try again.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')