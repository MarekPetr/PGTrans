from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Transport, User, Vehicle, Request, Reservation

admin.site.register(Vehicle)
admin.site.register(Transport)
admin.site.register(Request)
admin.site.register(Reservation)
admin.site.register(User, UserAdmin)
