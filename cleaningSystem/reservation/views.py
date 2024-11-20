from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from taskTeams.models import Group
from core.models import CustomUser
from .models import Reservation
from .forms import ReservationForm
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                return HttpResponseForbidden("You are not authorized to access this page.")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

# Create your views here.
@login_required
def create_reservation(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        raise PermissionDenied("You must be a Client to create a reservation.")

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            cleaning_type = form.cleaned_data['cleaning_type']

            group = Group.objects.filter(specialization=cleaning_type).order_by('-rating').first()
            
            if not group:
                return render(request, 'reservations/create_reservation.html', {
                    'form': form,
                    'error': "No group is available for the selected cleaning type."
                })

            # Save the reservation
            reservation = form.save(commit=False)
            reservation.client = request.user 
            reservation.group = group
            reservation.price = 50.00
            reservation.save() 
            
            return redirect('client_dashboard')

    else:
        form = ReservationForm()

    return render(request, 'reservations/create_reservation.html', {'form': form})

@login_required
def rate_group(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, client=request.user)
    
    if request.method == 'POST':
        rating = int(request.POST['rating'])
        group = reservation.assigned_group
        group.rating = (group.rating + rating) / 2
        group.save()
        
        return redirect('client_dashboard')
    
    return render(request, 'feedbacks/rate_group.html', {'reservation': reservation})

@login_required
@role_required('Client')
def client_dashboard(request):
    if not isinstance(request.user, CustomUser):
        raise ValueError("The request user is not a valid User instance.")
    reservations = Reservation.objects.filter(client=request.user)
    return render(request, 'dashboard/client_dashboard.html', {'reservations':reservations})

@login_required
@role_required('Admin')
def admin_dashboard(request):
    reservations = Reservation.objects.all()
    return render(request, 'dashboard/admin_dashboard.html', {'reservations': reservations})

@login_required
def chief_dashboard(request):
    reservations = Reservation.objects.filter(assigned_group__chief=request.user)
    return render(request, 'tasks/chief_dashboard.html', {'reservations': reservations})

@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})

@login_required
@role_required('Chief')
def task_list(request):
    reservations = Reservation.objects.filter(assigned_group__chief=request.user)
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})

@login_required
@role_required('Admin')
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not reservation.approved:
        reservation.approved = True
        reservation.save()
    return redirect('admin_dashboard')

def reservation_list(request):
    reservations = Reservation.objects.order_by('cleaning_date', 'priority')
    return render(request, 'reservation_list.html', {'reservations': reservations})