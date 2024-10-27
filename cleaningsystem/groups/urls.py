from django.urls import path
from . import views

urlpatterns = [
    path('group-list/', views.group_list, name='register'),
]
