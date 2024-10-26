from django.urls import path
from . import views

urlpatterns = [
    path('', views.assign_task, name='assign_task'),
]
