from django.contrib import admin
from account.models import User
from tasks.models import Reservation
# Register your models here.

admin.site.register(User)
admin.site.register(Reservation)