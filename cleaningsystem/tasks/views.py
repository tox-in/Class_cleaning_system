from django.shortcuts import render
from .models import Task
from groups.models import CleaningGroup
from datetime import datetime

# Create your views here.
def assign_task(request, group_id):
    group = CleaningGroup.objects.get(id=group_id)
    task = Task.objects.create(group=group, datetime=datetime.now())
    return render(request, 'tasks/assigned.html', {'task': task})