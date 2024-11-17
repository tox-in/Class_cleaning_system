from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
