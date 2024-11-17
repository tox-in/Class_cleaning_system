from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path
from django import forms
from django.http import HttpResponse
from .models import Group
from .forms import GroupForm
from core.models import CustomUser

# Create your views here.
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'groups/group_list.html', {'groups': groups})

def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'groups/group_detail.html', {'group': group})

def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        print(request.POST)
        
        if form.is_valid():
            print("valid form")
            group = form.save(commit=True)
            return redirect('group_list')
        print(form.errors, form.non_field_errors())
    else:
        form = GroupForm()
    return render(request, 'groups/group_form.html', {'form': form})

def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_detail', pk=pk)
    else:
        form = GroupForm(instance=group)
    return render(request, 'groups/group_form.html', {'form': form})

def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, 'groups/group_confirm_delete.html', {'group': group})