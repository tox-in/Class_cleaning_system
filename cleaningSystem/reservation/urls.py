from django.urls import path
from . import views

urlpatterns = [
    path('reservation/create/', views.create_reservation, name='create_reservation'),
    path('reservation/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('task_list/',views.task_list, name='task_list'),
    path('approve_reservation/<int:reservation_id>/', views.approve_reservation, name='approve_reservation'),
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('chief/', views.chief_dashboard, name='chief_dashboard'),
]
