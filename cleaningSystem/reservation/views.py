from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from taskTeams.models import Group
from core.models import CustomUser
from .models import Reservation
from .forms import ReservationForm
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
import logging
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger(__name__)

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
    if not hasattr(request.user, 'profile') or request.user.role != 'Client':
        raise PermissionDenied("You must be a Client to create a reservation.")

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            cleaning_type = form.cleaned_data['cleaning_type']
            
            logger.debug(f"Looking for group with specialization: {cleaning_type}")
            
            assigned_group = Group.objects.filter(specialization=cleaning_type).order_by('-rating').first()
            
            logger.debug(f"Found group: {assigned_group}")
            
            if not assigned_group:
                logger.warning(f"No group found for cleaning type: {cleaning_type}")
                return render(request, 'reservations/create_reservation.html', {
                    'form': form,
                    'error': "No group is available for the selected cleaning type."
                })

            reservation = form.save(commit=False)
            reservation.client = request.user 
            reservation.assigned_group = assigned_group
            reservation.price = 50.00
            
            logger.debug(f"Saving reservation with group: {assigned_group.name}, chief: {assigned_group.chief}")
            
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
    # Basic counts
    total_groups = Group.objects.count()
    total_members = CustomUser.objects.filter(role='Member').count()
    total_reservations = Reservation.objects.count()
    total_clients = CustomUser.objects.filter(role='Client').count()

    # Recent reservations
    recent_reservations = Reservation.objects.select_related(
    'client', 'assigned_group'
    ).only('client__username', 'cleaning_type', 'assigned_group__name', 'cleaning_date').order_by('-reservation_date')[:10]


    # Monthly reservations for graph
    monthly_reservations = (
        Reservation.objects
        .annotate(month=TruncMonth('cleaning_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Groups and their ratings
    groups = Group.objects.annotate(
        task_count=Count('reservation'),
        member_count=Count('members')
    ).order_by('-rating')

    # Top performing groups
    top_groups = groups[:5]

    # Clients with most reservations
    top_clients = CustomUser.objects.filter(
        role='Client'
    ).annotate(
        reservation_count=Count('reservations')
    ).order_by('-reservation_count')[:5]

    # Pending approvals
    pending_approvals = Reservation.objects.filter(
        approved_by_admin=False
    ).select_related('client', 'assigned_group')

    # Cleaning type distribution
    cleaning_type_stats = (
        Reservation.objects
        .values('cleaning_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Group members list
    groups_with_members = Group.objects.prefetch_related('members', 'chief')

    # Calculate completion rate
    total_completed = Reservation.objects.filter(approved_by_admin=True).count()
    completion_rate = (total_completed / total_reservations * 100) if total_reservations > 0 else 0

    context = {
        'total_groups': total_groups,
        'total_members': total_members,
        'total_reservations': total_reservations,
        'total_clients': total_clients,
        'recent_reservations': recent_reservations,
        'monthly_reservations': json.dumps(list(monthly_reservations), cls=DjangoJSONEncoder),
        'groups': groups,
        'top_groups': top_groups,
        'top_clients': top_clients,
        'pending_approvals': pending_approvals,
        'cleaning_type_stats': json.dumps(list(cleaning_type_stats)),
        'groups_with_members': groups_with_members,
        'completion_rate': round(completion_rate, 1)
    }

    return render(request, 'dashboard/admin_dashboard.html', context)

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