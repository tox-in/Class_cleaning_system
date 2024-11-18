from django.shortcuts import render
from django.contrib.auth import logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib import messages
from .forms import LoginForm

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
            user.save()

            # Success message and redirect
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            # If form is invalid, print errors for debugging
            print(form.errors)
            messages.error(request, "Error creating account. Please try again.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    
    
    if request.method == 'POST':
        print(request.POST)
        
        form = LoginForm(request.POST)
        
        print("checking validity")
        if form.is_valid():
            print("checked validity")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')  # Redirect to home or wherever you want
            else:
                messages.error(request, "Invalid username or password.")
        else:
            print("validity failed")
            messages.error(request, "Invalid form submission.")
            print(form.errors) 
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')