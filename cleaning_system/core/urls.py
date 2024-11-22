from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Default route for the homepage
    path('', include('tasks.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', include('account.urls')),  # Include the signup route
]
