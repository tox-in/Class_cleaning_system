from django.urls import path
from . import views

urlpatterns = [
    path('approve/', views.approve_task, name='approve'),
]
