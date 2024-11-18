from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'chief', 'rating']
    filter_horizontal = ['members']
