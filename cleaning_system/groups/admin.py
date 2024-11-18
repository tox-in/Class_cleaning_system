from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'chief', 'rating']
    filter_horizontal = ['members']

    def save_model(self, request, obj, form, change):
        # Save the group instance first to generate an ID
        obj.save()
        # After saving, handle the members relation
        if obj.members.exists():
            obj.members.set(obj.members.all())  # Reassign members to ensure proper linkage
        super().save_model(request, obj, form, change)
