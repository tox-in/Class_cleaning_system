from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from groups.models import Group
from account.models import User
from .models import Reservation
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponseBadRequest


def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email="admin@cleaningsystem.com",
        recipient_list=recipient_list,
    )

def role_required(*roles):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not hasattr(request.user, "role") or request.user.role not in roles:
                return HttpResponseForbidden("You are not authorized to access this page.")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

# Create your views here.
@login_required
def create_reservation(request):
    if request.method == 'POST':
        cleaning_type = request.POST['cleaning_type']
        address = request.POST['address']
        house_number = request.POST['house_number']
        cleaning_date = request.POST['cleaning_date']
        
        if not all([cleaning_type, address, house_number, cleaning_date]):
            return HttpResponseBadRequest("Missing required fields.")
        
        
        group = Group.objects.filter(specialization=cleaning_type).order_by('ratings').first()
        
        if not group:
            return render(request, 'tasks/create_reservation.html', {'error':"No group available for the selected cleaning type."})
        
        price = 50.00
        
        reservation = Reservation.objects.create(
            client=request.user,
            cleaning_type=cleaning_type,
            address=address,
            house_number=house_number,
            cleaning_date=cleaning_date,
            price=price,
            assigned_group=group
        )
        
        send_notification_email(
            subject="Reservation Confirmation",
            message=f"Your reservation for {cleaning_type} has been placed successfully.",
            recipient_list=[request.user.email],
        )

        # Notify group chief
        if group.chief and group.chief.email:
            send_notification_email(
                subject="New Task Assigned",
                message=(
                    f"Your group has been assigned a new task:\n\n"
                    f"Client: {request.user.username}\n"
                    f"Cleaning Type: {cleaning_type}\n"
                    f"Address: {address}, House No: {house_number}\n"
                    f"Date: {cleaning_date}\nPrice: ${price}\n"
                ),
                recipient_list=[group.chief.email],
            )

        return redirect('client_dashboard')

    return render(request, 'tasks/create_reservation.html')


@login_required
def rate_group(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, client=request.user)
    
    if request.method == 'POST':
        rating = int(request.POST['rating'])
        group = reservation.assigned_group
        group.rating = (group.rating + rating) / 2
        group.save()
        
        return redirect('client_dashboard')
    
    return render(request, 'tasks/rate_group.html', {'reservation': reservation})

@login_required
def client_dashboard(request):
    reservations = Reservation.objects.filter(client=request.user)
    return render(request, 'tasks/client_dashboard.html', {'reservations':reservations})

@login_required
@role_required('Admin')
def admin_dashboard(request):
    reservations = Reservation.objects.all()
    return render(request, 'tasks/admin_dashboard.html', {'reservations': reservations})

@login_required
def chief_dashboard(request):
    reservations = Reservation.objects.filter(assigned_group__chief=request.user)
    return render(request, 'tasks/chief_dashboard.html', {'reservations': reservations})

@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'tasks/reservation_detail.html', {'reservation': reservation})

@login_required
@role_required('Chief')
def task_list(request):
    reservations = Reservation.objects.filter(assigned_group__chief=request.user)
    return render(request, 'tasks/task_list.html', {'reservations': reservations})

@login_required
@role_required('Admin')
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not reservation.approved:
        reservation.approved = True
        reservation.save()
    return redirect('admin_dashboard')