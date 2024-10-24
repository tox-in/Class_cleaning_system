from django.shortcuts import render, get_object_or_404, redirect
from .models import Approval
from tasks.models import Task
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def approve_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        approval_status = request.POST.get('approval_status') == 'true'
        remarks = request.POST.get('remarks', '')
        
        Approval.objects.create(
            task = task,
            approved_by = request.user,
            approval_status = approval_status,
            remarks = remarks
        )
        
        return redirect('approved/approved.html')
    
    return render(request, 'approved/approved.html', {'task': task})